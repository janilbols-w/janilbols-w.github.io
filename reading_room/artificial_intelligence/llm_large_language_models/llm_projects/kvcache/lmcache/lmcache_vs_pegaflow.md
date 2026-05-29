# LMCache vs PegaFlow: 细粒度分层对比

> 对比对象
- LMCache: https://github.com/LMCache/LMCache
- PegaFlow: https://github.com/novitalabs/pegaflow/tree/master

> 说明
- 本文基于两仓库公开文档/示例代码做静态对比，不等价于同环境下的 head-to-head benchmark。
- 性能数字仅代表各自公开测试场景，不能直接横比；可用于判断方向和工程取舍。

## 0. 对齐口径（先统一再比较）

为和 `kvcache_architecture.md`、`kvcache_arena.md` 保持一致，本文采用统一分类口径：

1. U（用户主目标）
- U1 首 token 更快
- U2 生成更稳
- U3 吞吐更高
- U4 平台更可管

2. E（主作用阶段）
- E0-E6 中只选择一个主作用阶段。

3. L（主层级）
- A/B/C/D 只允许唯一归属。

本文中的 LMCache 与 PegaFlow 同属 C 层，不做跨层比较，只做 C 层内部次级分类比较。

---

## 1. 一句话结论

- `PD disagg`：两者都支持。
- `XpYd`：LMCache 明确提供并文档化（x prefillers + y decoders）；PegaFlow 从路由与启动脚本看支持 `num-p/num-d` 拓扑，但命名不叫 XpYd。
- `存储 service 独立部署`：PegaFlow 的“独立服务化”更强（pegaflow-server + metaserver + router 体系）；LMCache 更偏“库 + 连接器 + 可选服务/后端”的形态。
- `性能侧重点`：LMCache 强调缓存复用带来的 TTFT/吞吐收益与多介质缓存；PegaFlow 强调 RDMA-first、尾延迟稳定性与独立数据平面的可控性。

补充（按 U/E/L 口径）：
- LMCache：主目标偏 U1/U3，主作用阶段偏 E5，主层级 C，次级分类 C-1。
- PegaFlow：主目标偏 U2/U4，主作用阶段偏 E5，主层级 C，次级分类 C-2。

## 2. 同层前提（C 层）

本节只给出 C 层定位，不再重复跨层映射。

1. C 层定义
- 引擎外 KV 服务层：通过 connector/sidecar/service 形成独立 KV 能力。

2. C 层次级分类
- C-1 复用能力优先型：LMCache
- C-2 服务化治理优先型：PegaFlow

3. C 层内对比原则
- 只比较同层能力差异：复用路径、服务化程度、控制面显式程度、传输栈与运维复杂度。

## 3. C 层能力对比（LMCache vs PegaFlow）

### 3.1 用户目标与执行阶段对照

| 项目 | 用户主目标（U） | 主作用阶段（E） | 主层级（L） | 次级分类 |
|---|---|---|---|---|
| LMCache | U1/U3 | E5 | C | C-1 复用能力优先型 |
| PegaFlow | U2/U4 | E5 | C | C-2 服务化治理优先型 |

### 3.2 同层差异（只比较 C 层内部）

1. LMCache（C-1）
- 偏“复用收益与接入效率”导向。
- 强项：connector + 多层缓存复用路径清晰，快速接入收益明显。
- 适配场景：优先追求 U1/U3（TTFT 与吞吐）。

2. PegaFlow（C-2）
- 偏“服务化与治理能力”导向。
- 强项：独立数据平面与控制面延展更明确，尾延迟与可运维性叙事更强。
- 适配场景：优先追求 U2/U4（稳定性与平台治理）。

## 4. PD disagg / XpYd 能力对比

## 4.1 是否支持 PD disagg

- `LMCache`：支持。文档存在完整 `disaggregated prefill` quickstart，且有 1p1d 与多实例示例。
- `PegaFlow`：支持。`docs/pd.md` 给出 P/D 设计与流程，`PdConnector` 标注为 experimental 但可运行。

## 4.2 是否支持 XpYd

- `LMCache`：明确支持，且直接以 `XpYd` 命名（x prefillers + y decoders），并提供 2p2d 示例、端口/GPU/代理配置。
- `PegaFlow`：从 `examples/run_vllm_pd_with_pega.py` 的 `--num-p` / `--num-d` 能看到可扩展到多 P 多 D；语义上等价于 XpYd，但文档术语是 P/D disaggregation，不强调 XpYd 名称。

## 4.3 调度与控制流差异

- `LMCache`
    - 常见模式：Proxy 先发 prefill（常配 `max_tokens=1`）再交 decode。
    - XpYd 场景下使用轮询分发，强调 prefiller/decoder 水平扩展。
- `PegaFlow`
    - 文档强调“生产语义里 Router 只请求 D，D 再向 P 发 prefill 请求”，Proxy 可作为调试工具。
    - 该模式让 D 端成为更强的会话控制点，便于与 D 端资源/延迟约束对齐。

## 5. 存储 service 部署架构对比（C 层内差异）

## 4.1 LMCache

- 更偏“缓存层库 + 引擎内连接器 + 可选后端/通道”架构。
- 优势是接入快、路径短，适合先在现有 vLLM/SGLang 流水线上加能力。
- 有 MP 与 operator 等形态，但核心叙事仍是缓存复用与传输加速本身。

## 4.2 PegaFlow

- 更偏“独立数据平面服务”架构：
    - `pegaflow-server`：KV 存储/读写/远端取回核心服务。
    - `pegaflow-metaserver`：跨节点 block 元数据注册和发现。
    - `router`：P/D 流编排。
- 这种拆分更像“专门的 KV 基础设施层”，便于独立扩缩容与故障域隔离。

## 4.3 差异总结

- 若你关心“存储服务是否可独立演进、独立运维”：PegaFlow 更明显。
- 若你关心“尽快在推理框架里获得缓存收益”：LMCache 路径通常更直接。

## 6. 性能与可扩展性对比（谨慎解读）

## 6.1 LMCache（公开表述）

- README 级别表述：在多种场景可获得显著 TTFT/吞吐改善（常见 3-10x 量级叙事）。
- XpYd 文档示例强调：
    - 多 prefiller 可提升吞吐；
    - 更好的 TTFT（排队更少）；
    - 更高设备利用率。
- 主要收益来源：缓存复用 + 多层存储 + 分离式 prefill 的并行化。

## 6.2 PegaFlow（公开表述）

- README 给出 warm/cold 对比（同项目场景）显示 warm 路径 TTFT 明显下降。
- `docs/pd.md` 的 P/D benchmark 显示：
    - TTFT 可能高于 baseline；
    - 但 TPOT p99/ITL p99 更稳定（尾延迟显著改善）。
- 主要收益来源：RDMA-first 数据路径、拓扑亲和、独立数据平面带来的可控性。

## 6.3 对你决策最有用的解读

- 追求“整体吞吐和缓存命中收益”且希望快速落地：LMCache 往往更顺手。
- 追求“跨节点、可运维、尾延迟可控的数据平面”并愿意投入工程化：PegaFlow 更有吸引力。

## 7. 功能矩阵（细粒度）

| 维度 | LMCache（C-1） | PegaFlow（C-2） |
|---|---|---|
| vLLM 集成 | 强（主路径） | 强（主路径） |
| SGLang 集成 | 有 | 有（文档/代码路径） |
| PD disagg | 有（1p1d/xpyd） | 有（P/D router + PdConnector） |
| XpYd 命名/示例 | 明确有 XpYd | 语义支持多 P 多 D，但不主打 XpYd 名称 |
| 主要传输栈 | NIXL（PD 语境显式） | RDMA-first（另有 NIXL 对照脚本） |
| 存储层形态 | 库/连接器驱动，多介质后端 | 独立服务化更强（server + metaserver） |
| 多节点元数据 | 有能力但中心化元数据服务不是唯一主路径 | metaserver 明确承担跨节点元数据协调 |
| 观测/运维 | 具备基础能力 | Prometheus/OTLP + 服务化运维路径更完整 |
| 生产成熟度（PD） | 可用示例较完整 | PD Connector 文档明确 experimental |

## 8. 风险与局限

## 8.1 LMCache

- PD 的最强路径与 NIXL 绑定明显，对网络/硬件拓扑有要求。
- 功能面很广，配置组合多，落地时要避免“全开功能”导致调优复杂。

## 8.2 PegaFlow

- PD Connector 仍有实验属性，版本演进快，需要跟踪变更。
- 服务拆分更多，部署和排障复杂度高于单库式方案。

## 9. 选型建议（按场景）

1. 你要快速验证 PD + 缓存复用收益：优先 LMCache（先 1p1d，再 XpYd）。
2. 你要建设长期的 KV 数据平面（跨节点、独立扩缩容、可观测）：优先 PegaFlow。
3. 混合策略：
     - 短期用 LMCache 快速跑通业务收益；
     - 中长期在核心集群评估 PegaFlow 的独立数据平面与尾延迟优势。

## 10. 建议的同场景对比实验（避免误判）

要公平比较，建议统一：

- 同模型（如 Qwen3-8B）
- 同硬件（GPU 型号、NVLink/RDMA、NIC 绑定）
- 同负载（输入长度分布、请求率、并发、冷热比例）
- 同指标：TTFT mean/p95/p99、TPOT mean/p99、ITL p99、吞吐、GPU 利用率、RDMA 带宽、命中率

最小实验矩阵：

1. `1P1D`：验证基本链路与稳定性。
2. `2P2D`：观察扩展效率与负载均衡。
3. `长前缀高复用` vs `低复用随机`：区分缓存系统真正收益区间。

---

如果你愿意，我下一步可以直接补一节「你当前集群的部署建议」（按单机 NVLink / 跨机 RDMA 两套拓扑，给出 LMCache 与 PegaFlow 的最小可运行配置清单）。