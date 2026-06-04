#!/usr/bin/env python3

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


EXAMPLE_CONFIG = {
    "hourly_costs": {
        "gpu": 6.5,
        "cpu": 0.7,
        "mem": 0.3,
        "storage": 0.1,
        "network": 0.15,
        "gateway": 0.2,
        "obs": 0.25,
        "ops": 0.8,
        "risk": 0.2,
    },
    "pricing": {
        "margin": 0.55,
        "payment_fee": 0.03,
        "bad_debt": 0.01,
        "tax": 0.01,
        "alpha": 0.25,
        "beta": 1.8,
        "weights": {
            "cache": 0.7,
            "input": 0.2,
            "output": 0.1,
        },
        "coefficients": {
            "latency": 1.1,
            "reliability": 1.05,
            "reserve": 1.05,
        },
    },
    "sla": {
        "ttft95": 2.0,
        "e2e95": 12.0,
        "err": 0.01,
    },
    "rows": [
        {
            "concurrency": 1,
            "req_per_sec": 0.9,
            "input_tokens": 1500,
            "output_tokens": 600,
            "ttft95": 0.8,
            "e2e95": 5.1,
            "err": 0.001,
            "cache_hit": 0.15,
        },
        {
            "concurrency": 4,
            "req_per_sec": 2.9,
            "input_tokens": 1500,
            "output_tokens": 600,
            "ttft95": 1.1,
            "e2e95": 6.8,
            "err": 0.004,
            "cache_hit": 0.15,
        },
        {
            "concurrency": 8,
            "req_per_sec": 4.6,
            "input_tokens": 1500,
            "output_tokens": 600,
            "ttft95": 1.9,
            "e2e95": 10.4,
            "err": 0.008,
            "cache_hit": 0.15,
        },
        {
            "concurrency": 16,
            "req_per_sec": 5.7,
            "input_tokens": 1500,
            "output_tokens": 600,
            "ttft95": 2.5,
            "e2e95": 14.1,
            "err": 0.018,
            "cache_hit": 0.15,
        },
    ],
}


def load_config(path: Optional[str]) -> Dict[str, Any]:
    if path is None:
        return EXAMPLE_CONFIG
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def positive_sum(values: Dict[str, float]) -> float:
    return sum(max(0.0, float(value or 0.0)) for value in values.values())


def normalize_weights(weights: Dict[str, Any]) -> Dict[str, float]:
    numeric = {
        "cache": float(weights.get("cache", 0.0) or 0.0),
        "input": float(weights.get("input", 0.0) or 0.0),
        "output": float(weights.get("output", 0.0) or 0.0),
    }
    total = positive_sum(numeric)
    if total <= 0:
        raise ValueError("pricing.weights must sum to a positive value")
    return {key: value / total for key, value in numeric.items()}


def compute_row(row: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    sla = config["sla"]
    pricing = config["pricing"]
    weights = normalize_weights(pricing["weights"])
    coeffs = pricing["coefficients"]
    hourly_cost = positive_sum(config["hourly_costs"])

    req_per_sec = float(row.get("req_per_sec", 0.0) or 0.0)
    input_tokens = float(row.get("input_tokens", 0.0) or 0.0)
    output_tokens = float(row.get("output_tokens", 0.0) or 0.0)
    ttft95 = float(row.get("ttft95", 0.0) or 0.0)
    e2e95 = float(row.get("e2e95", 0.0) or 0.0)
    err = float(row.get("err", 0.0) or 0.0)
    cache_hit = min(1.0, max(0.0, float(row.get("cache_hit", 0.0) or 0.0)))

    sla_pass = (
        ttft95 <= float(sla["ttft95"])
        and e2e95 <= float(sla["e2e95"])
        and err <= float(sla["err"])
    )

    sla_ratio = row.get("sla_ratio")
    if sla_ratio is None or sla_ratio == "":
        sellable_ratio = 1.0 if sla_pass else 0.0
    else:
        sellable_ratio = min(1.0, max(0.0, float(sla_ratio)))

    goodput_rps = req_per_sec * sellable_ratio
    total_tokens_per_hour = 3600.0 * goodput_rps * (input_tokens + output_tokens)
    input_tokens_per_hour = 3600.0 * goodput_rps * input_tokens
    output_tokens_per_hour = 3600.0 * goodput_rps * output_tokens
    cache_tokens_per_hour = cache_hit * input_tokens_per_hour
    billable_input_tokens_per_hour = (1.0 - cache_hit) * input_tokens_per_hour

    if total_tokens_per_hour <= 0:
        cost_per_million = math.inf
    else:
        cost_per_million = hourly_cost / total_tokens_per_hour * 1_000_000.0

    margin = float(pricing["margin"])
    payment_fee = float(pricing["payment_fee"])
    bad_debt = float(pricing["bad_debt"])
    tax = float(pricing["tax"])
    net_ratio = 1.0 - margin - payment_fee - bad_debt - tax
    if net_ratio <= 0:
        raise ValueError("margin + fees must be less than 1.0")

    blended_price = cost_per_million / net_ratio
    final_price = blended_price * float(coeffs["latency"]) * float(coeffs["reliability"]) * float(coeffs["reserve"])

    alpha = float(pricing["alpha"])
    beta = float(pricing["beta"])
    denom = alpha * weights["cache"] + weights["input"] + beta * weights["output"]
    if denom <= 0:
        raise ValueError("invalid alpha/beta/weights combination")

    input_price = final_price / denom
    cache_price = alpha * input_price
    output_price = beta * input_price
    revenue_per_hour = final_price / 1_000_000.0 * total_tokens_per_hour if math.isfinite(final_price) else 0.0
    profit_per_hour = revenue_per_hour - hourly_cost

    result = dict(row)
    result.update(
        {
            "sla_pass": sla_pass,
            "sellable_ratio": sellable_ratio,
            "goodput_rps": goodput_rps,
            "hourly_cost": hourly_cost,
            "tokens_per_hour": total_tokens_per_hour,
            "input_tokens_per_hour": input_tokens_per_hour,
            "output_tokens_per_hour": output_tokens_per_hour,
            "cache_tokens_per_hour": cache_tokens_per_hour,
            "billable_input_tokens_per_hour": billable_input_tokens_per_hour,
            "cost_per_million": cost_per_million,
            "blended_price_per_million": blended_price,
            "final_price_per_million": final_price,
            "cache_price_per_million": cache_price,
            "input_price_per_million": input_price,
            "output_price_per_million": output_price,
            "revenue_per_hour": revenue_per_hour,
            "profit_per_hour": profit_per_hour,
        }
    )
    return result


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    viable = [row for row in results if row["sla_pass"] and math.isfinite(row["profit_per_hour"])]
    best = max(viable, key=lambda row: row["profit_per_hour"], default=None)
    return {
        "rows": results,
        "best_concurrency": None if best is None else best.get("concurrency"),
        "best_row": best,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark to pricing calculator")
    parser.add_argument("--input", help="Path to input JSON config")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--example", action="store_true", help="Print example input JSON and exit")
    args = parser.parse_args()

    if args.example:
        json.dump(EXAMPLE_CONFIG, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    config = load_config(args.input)
    results = [compute_row(row, config) for row in config.get("rows", [])]
    payload = summarize(results)
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())