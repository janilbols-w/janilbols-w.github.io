# Price Calculator

## 1. 项目简介

这个目录用于基于昇腾压测数据计算不同 deployment 的定价结果（pricing）。
核心流程在 Notebook 中完成：
- 读取 evalscope CSV 压测结果
- 构建多个 deployment
- 基于 SLA 规则做分级
- 使用 ProfitModel 计算成本与价格
- 汇总并导出 Excel

## 2. 目录结构

- pricing_calculator.ipynb: 主计算 Notebook
- data/昇腾token工厂测试清单-evalscope.csv: 输入压测数据
- data/pricing_results.xlsx: 导出的结果文件（运行后生成）

## 3. 依赖

建议在 Notebook 内核中安装以下包：
- pandas
- openpyxl

说明：
- pandas 用于表格展示与数据汇总
- openpyxl 用于写出 xlsx 文件

## 4. 使用方法

打开 pricing_calculator.ipynb 后，按顺序运行：

1. 第 2 个单元
   - 定义硬件、deployment、SLA 数据结构
   - 定义 CSV 解析函数 load_deployments_from_evalscope_csv

2. 第 3 个单元
   - 定义 ProfitModel

3. 第 4 个单元
   - 调用 run_pricing_for_all_deployments 批量计算所有 deployment
   - 展示 summary 和每个 deployment 的 detail
   - 调用 export_pricing_results_to_excel 导出 Excel

## 5. 输入数据说明

默认输入文件：
- data/昇腾token工厂测试清单-evalscope.csv

当前逻辑会从 CSV 中提取并转换以下信息：
- input-len
- output-len
- Conc
- latency / ttft / tpot 统计值
- throughput completion

并自动完成：
- deployment 分组
- 重名 deployment 后缀去重
- 从 hardware_spec 推导 num_devices

## 6. 输出结果说明

运行后会得到两类结果：

1. Notebook 内展示
- summary 汇总表（每个 deployment 一行）
- 每个 deployment 的 detail 表（全部打印，不是 sample）

2. Excel 文件
- 导出路径: data/pricing_results.xlsx
- sheet 说明:
  - summary: 汇总结果
  - 其他 sheet: 每个 deployment 的明细

## 7. 可调参数

在第 4 个单元中可调整：

- target_sla_level
- ProfitModel 参数
  - margin
  - fee_total
  - alpha
  - beta
  - weight_cache
  - weight_input
  - weight_output
  - premium
  - billing_days_per_month

## 8. 常见问题

1. 无法导出 Excel
- 现象: 提示需要 openpyxl 或 xlsxwriter
- 处理: 在 Notebook 内核安装 openpyxl 后重跑第 2-4 个单元

2. 输出中大量 inf
- 这通常表示该行没有通过 target_sla_level，导致 sellable_ratio 为 0
- 可尝试调低 target_sla_level 或使用 manual_sellable_ratio 做敏感性测试

3. 部署名称重复
- 代码会自动追加后缀，例如 __2，避免覆盖
