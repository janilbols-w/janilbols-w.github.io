---
title: 从本地 Benchmark 到 Token 定价
---

# 从本地 Benchmark 到 Token 定价

> 目标：在同一套硬件上，基于不同并发负载 benchmark 结果，直接推导 Token API 的定价、毛利率与生产并发选择。
>
> 最后更新：2026-06-04

---

## 1. 核心思路

如果你已经在同一套硬件上，跑出了不同并发负载下的 benchmark 结果，那么可以把 benchmark 数据直接转成定价结果。

核心思路不是看“裸吞吐”，而是看满足 SLA 之后的 `goodput`，也就是可售卖吞吐。

配套工具：

- Python 计算脚本：`benchmark_pricing_calculator.py`
- 交互式页面：[Benchmark To Pricing Calculator]({{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/maas/maas_pricing/benchmark_pricing_calculator.html' | relative_url }})

---

## 2. 每个并发点需要采集哪些指标

设并发档位为 `c`，建议至少记录以下字段：

- `R_c`：完成请求吞吐，单位 `req/s`
- `I_c`：平均输入 token / 请求
- `O_c`：平均输出 token / 请求
- `TTFT95_c`：P95 首 token 延迟
- `E2E95_c`：P95 端到端延迟
- `ERR_c`：错误率
- `TPSout_c`：输出 token/s
- `CacheHit_c`：缓存命中 token 占比（如支持缓存）

如果你只做纯 Token API，最关键的是：`R_c`、`I_c`、`O_c`、`TTFT95_c`、`E2E95_c`、`ERR_c`。

---

## 3. 先定义 SLA 约束

假设对外 SLA 为：

- `TTFT95 <= T_sla`
- `E2E95 <= E_sla`
- `ERR <= e_sla`

可定义一个 SLA 可行函数：

$$
F_c =
\begin{cases}
1, & \text{if } TTFT95_c \le T_{sla},\ E2E95_c \le E_{sla},\ ERR_c \le e_{sla} \\
0, & \text{otherwise}
\end{cases}
$$

若 `F_c = 0`，则该并发点不适合作为正式报价依据。

如果你希望更细，可以定义 `S_c \in [0,1]`，表示在该并发点下真正满足 SLA 的请求比例。

---

## 4. 从吞吐到可售卖吞吐

每个并发点的可售卖请求吞吐为：

$$
G_c = R_c \times S_c
$$

若只用硬阈值筛选，也可以写成：

$$
G_c = R_c \times F_c
$$

然后换算成每小时可售卖 token 数：

$$
T_c = 3600 \times G_c \times (I_c + O_c)
$$

如需拆分输入与输出：

$$
T^{in}_c = 3600 \times G_c \times I_c
$$

$$
T^{out}_c = 3600 \times G_c \times O_c
$$

如果有缓存命中率 `h_c`：

$$
T^{cache}_c = h_c \times T^{in}_c
$$

$$
T^{billable\_input}_c = (1 - h_c) \times T^{in}_c
$$

---

## 5. 每小时总成本

对固定硬件配置，先汇总每小时总成本：

$$
C^{hour} = C^{gpu} + C^{cpu} + C^{mem} + C^{storage} + C^{network} + C^{gateway} + C^{obs} + C^{ops} + C^{risk}
$$

其中：

- `C_gpu`：GPU 成本
- `C_cpu / C_mem / C_storage / C_network`：基础设施成本
- `C_gateway`：API 网关与鉴权成本
- `C_obs`：日志、监控、追踪成本
- `C_ops`：运维与工程人力摊销
- `C_risk`：SLA 赔付与风险准备金

---

## 6. 换算成每百万 Token 成本

对并发点 `c`：

$$
Cost_{1M}(c) = \frac{C^{hour}}{T_c} \times 10^6
$$

这表示：在并发 `c` 下、满足 SLA 后的真实每百万 token 成本。

---

## 7. 加入毛利率与收入侧损耗

设：

- `m`：目标毛利率
- `f_pay`：支付通道费率
- `f_bad`：坏账/促销损耗率
- `f_tax`：税费或其他收入侧损耗率

则最低可持续售价：

$$
Price_{1M}(c) = \frac{Cost_{1M}(c)}{1 - m - f_{pay} - f_{bad} - f_{tax}}
$$

这是最直接的 benchmark 到定价映射公式。

---

## 8. 三段计价拆分

如果要继续拆成 `cache/input/output` 三段价格，设：

- `P_cache = \alpha P_{in}`
- `P_out = \beta P_{in}`

其中：

- `\alpha`：缓存价格相对输入价格的折扣系数，通常 `0 \le \alpha \le 1`
- `\beta`：输出价格相对输入价格的溢价系数，通常 `\beta \ge 1`

设真实流量结构权重为：

$$
w_{cache} + w_{in} + w_{out} = 1
$$

则 blended 售价：

$$
P_{blend} = w_{cache}P_{cache} + w_{in}P_{in} + w_{out}P_{out}
$$

代入后可得：

$$
P_{in} = \frac{P_{blend}}{\alpha w_{cache} + w_{in} + \beta w_{out}}
$$

进一步得到：

$$
P_{cache} = \alpha P_{in}, \quad P_{out} = \beta P_{in}
$$

---

## 9. 把 SLA 系数显式加进价格

benchmark 中不同并发点，即使成本相近，SLA 风险也不同。可在售价上引入 SLA 系数：

$$
Price^{final}_{1M}(c) = Price_{1M}(c) \times K_{lat} \times K_{rel} \times K_{reserve}
$$

其中：

- `K_lat`：低延迟溢价系数
- `K_rel`：高可靠性溢价系数
- `K_reserve`：容量预留溢价系数

经验上可按以下方式设置：

- 标准 SLA：`K_lat = 1.00`
- 低延迟 SLA：`K_lat = 1.10 ~ 1.30`
- 高可靠性：`K_rel = 1.05 ~ 1.20`
- 强预留能力：`K_reserve = 1.05 ~ 1.15`

---

## 10. 如何选择最适合生产的并发点

不要直接选 benchmark 吞吐最高的并发点，而要选“利润最大且 SLA 可持续”的并发点。

每小时收入：

$$
Revenue^{hour}_c = \frac{P_{blend}(c)}{10^6} \times T_c
$$

每小时利润：

$$
Profit^{hour}_c = Revenue^{hour}_c - C^{hour}
$$

然后在满足 SLA 的并发集合中选择：

$$
c^* = \arg\max_{c \in \mathcal{S}} Profit^{hour}_c
$$

其中：

$$
\mathcal{S} = \{ c \mid TTFT95_c \le T_{sla},\ E2E95_c \le E_{sla},\ ERR_c \le e_{sla} \}
$$

---

## 11. 可直接填写的计算模板

| 并发 `c` | `R_c(req/s)` | `I_c` | `O_c` | `TTFT95_c` | `E2E95_c` | `ERR_c` | `S_c` | `T_c(tokens/h)` | `Cost_1M(c)` | `Price_1M(c)` | `Profit/h` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |
| 2 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |
| 4 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |
| 8 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |
| 16 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |
| 32 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 | 待填 |

其中：

$$
T_c = 3600 \times R_c \times S_c \times (I_c + O_c)
$$

$$
Cost_{1M}(c) = \frac{C^{hour}}{T_c} \times 10^6
$$

$$
Price_{1M}(c) = \frac{Cost_{1M}(c)}{1 - m - f_{pay} - f_{bad} - f_{tax}}
$$

$$
Profit^{hour}_c = \frac{Price_{1M}(c)}{10^6} \times T_c - C^{hour}
$$

---

## 12. 结论

如果你要把 benchmark 结果直接转成定价，最关键的四步是：

1. 用 benchmark 数据求出满足 SLA 的可售卖吞吐 `T_c`。
2. 用每小时总成本换算 `Cost_1M(c)`。
3. 用毛利率与收入侧损耗反推 `Price_1M(c)`。
4. 在满足 SLA 的并发点里，选择利润最大的那个作为生产配置。
