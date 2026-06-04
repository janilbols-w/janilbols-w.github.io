---
title: Token API 定价方法（参考 Artificial Analysis）
---

# Token API 定价方法（参考 Artificial Analysis）

> 适用范围：只做纯 Token API（不含训练、微调、复杂应用层）。
>
> 目标：在保证可用性与体验的前提下，给出可持续盈利的 token 价格。
>
> 最后更新：2026-06-04

---

## 1. 定价核心结论

单纯 Token API 的定价，不应只看“每百万 token 成本”，而应同时看三维：

1. 质量（Intelligence）
2. 性能（Output Speed / Latency / End-to-End）
3. 价格（Cache / Input / Output）

这与 Artificial Analysis 的核心框架一致：能力、速度、价格联动评估，而不是单指标最优。

---

## 2. 从 Artificial Analysis 提炼出的定价启发

结合 `artificialanalysis.ai` 的公开结构，Token API 定价时建议直接吸收以下做法：

1. 分拆价格维度：将价格拆成 `cache hit`、`input`、`output`，而不是一个统一单价。
2. 保留 blended 视图：用固定权重给出“综合单价”，便于对外沟通与横向比较。
3. 关联质量与性能：同样价格下，输出速度更高、延迟更低、质量更好的模型可以定更高价。
4. 保留供应商差异：同一模型在不同 provider 的速度与价格差异很大，路由策略会直接影响毛利。
5. 注意缓存口径：不同提供商缓存计费规则不同（仅 hit / 含 write / 含 storage），需要显式披露。

---

## 3. 计价单位建议（对外）

对外建议统一使用 `USD / 1M tokens`（或 CNY / 百万 token），并分三项：

1. Cache Hit Price
2. Input Price
3. Output Price

同时提供一个 Blended Price（综合价），默认可采用 7:2:1 权重（cache:input:output）进行展示。

---

## 4. Blended 定价公式（参考 AA 展示逻辑）

定义：

- `P_cache`：缓存命中单价（每 1M token）
- `P_input`：输入单价（每 1M token）
- `P_output`：输出单价（每 1M token）
- `w_cache, w_input, w_output`：三类 token 的流量占比，且和为 1

综合单价：

$$
P_{blended} = w_{cache} \cdot P_{cache} + w_{input} \cdot P_{input} + w_{output} \cdot P_{output}
$$

若默认使用 7:2:1：

$$
P_{blended}^{(7:2:1)} = 0.7P_{cache} + 0.2P_{input} + 0.1P_{output}
$$

注意：你的真实业务分布往往不是 7:2:1。上线后应按真实日志动态更新权重。

---

## 5. 成本到售价的换算

### 5.1 请求级成本分摊

建议把每个请求的成本拆分为：

1. 推理算力成本（GPU/CPU）
2. 网关与网络成本
3. 日志与观测成本
4. 合规与运维摊销

然后折算成三类 token 成本：`C_cache`、`C_input`、`C_output`。

### 5.2 目标毛利定价

设目标毛利率为 `m`，则：

$$
P_{x} = \frac{C_{x}}{1 - m}, \quad x \in \{cache, input, output\}
$$

再根据上面的 blended 公式计算 `P_blended`。

---

## 6. 为什么 Output 通常应更贵

在纯 Token API 服务中，输出 token 常常对应更高的增量算力占用与时延风险，因此建议：

1. `P_output >= P_input` 作为默认策略。
2. 推理模型（高 reasoning）可加收输出侧溢价。
3. 对超长输出（如 >4k output tokens）设置阶梯价，覆盖尾延迟风险。

---

## 7. 性能与质量如何影响价格（AA 风格）

定价不能只看成本，还要看“单位体验价值”：

1. 质量更高（Intelligence 更高）：可支持更高报价。
2. 输出更快（tokens/s 更高）：可支持实时场景溢价。
3. 延迟更低（TTFT 更低）：可支持交互场景溢价。
4. 端到端更快（500 tokens 总时长更短）：可支持企业 SLA 溢价。

可用一个简单的价值系数法：

$$
P_{blended}^{final} = P_{blended}^{cost} \times K_{quality} \times K_{latency} \times K_{reliability}
$$

其中各系数可在 0.9-1.3 范围内按产品策略调节。

---

## 8. 三档 Token API 价格模板（建议）

| 档位 | 适配模型 | Cache/Input/Output | 目标毛利 | 备注 |
|---|---|---|---:|---|
| Economy | 低成本高吞吐模型 | 低/中/中 | 35%-45% | 追求成本效率 |
| Standard | 均衡模型 | 中/中/中高 | 45%-60% | 默认推荐档 |
| Premium | 高质量/推理模型 | 中/高/高 | 60%-75% | 强调质量与 SLA |

说明：

1. 对外可先展示 blended 价，再展开三项明细。
2. 企业客户可改为“保底 + 超额”计费，降低采购不确定性。

---

## 9. 实际落地时最容易踩坑的 8 个点

1. 只报一个统一单价，导致高输出场景亏损。
2. 忽略缓存写入和存储成本（尤其长上下文业务）。
3. 使用静态权重，长期不更新 blended 权重。
4. 未分模型档位，导致高质量模型被低价透支。
5. 未区分首 token 延迟与总响应时长，SLA 成本估计失真。
6. 把峰值利用率当平均利用率，低估单位成本。
7. 没有请求级成本归因，无法解释毛利波动。
8. 未设置降级和路由兜底，流量波动时成本失控。

---

## 10. 你可以直接照抄的报价流程

1. 采样 7-14 天真实流量，得到 cache/input/output 占比。
2. 计算每类 token 的真实成本（含算力、网关、运维、合规摊销）。
3. 按毛利目标得到三项基础售价。
4. 根据质量与性能设价值系数，形成最终报价。
5. 给出两套对外展示：
	- 明细价：cache/input/output
	- 综合价：blended（标注权重）
6. 每月复盘一次：模型性能变化、供应商价格变化、流量结构变化。

---

## 11. 推荐在文档中长期维护的指标面板

1. 单位成本：`C_cache / C_input / C_output`
2. 单位售价：`P_cache / P_input / P_output`
3. Blended 毛利率
4. P50/P95 TTFT
5. Output tokens/s
6. End-to-End 响应时长（固定输出 token）
7. 失败率与限流触发率
8. 路由命中率（低价模型 / 高价模型）

---

## 12. 结论

如果只是做单纯 Token API，最稳妥的定价方法是：

1. 价格结构化：`cache/input/output` 三段计价。
2. 展示标准化：同时给出 blended 价格并标注权重。
3. 决策多维化：定价同时参考质量、速度、延迟与可靠性。
4. 运营动态化：按真实流量和模型变化持续调价，而不是一次定死。

---

## 13. 扩展阅读

如果你希望把同一套硬件下、不同并发负载的 benchmark 结果直接换算成 Token API 价格、毛利率和最优生产并发，可以看这篇独立文档：

- [从本地 Benchmark 到 Token 定价]({{ '/reading_room/artificial_intelligence/llm_large_language_models/llm_projects/maas/maas_pricing/benchmark_to_pricing/' | relative_url }})

这篇文档单独整理了：

1. benchmark 指标采集口径
2. SLA 过滤与 goodput 计算
3. 从小时成本推导 `Cost_1M`
4. 毛利率、支付费率、坏账、税费的定价公式
5. 最优生产并发点的利润选择方法

