---
name: cuefleet-vibe-trading
description: Develop and backtest Binance event-contract strategies for CueFleet, turn a trading hypothesis into testable rules, report out-of-sample performance, package or validate a signal service, and plan integration with the authorized local trading API.
---

# CueFleet 事件合约策略

根据用户的目标选择研究、回测、服务部署或实盘接入。先确认标的、事件到期周期、策略输入、交易金额与同时在途上限。用 [真实行情案例](docs/btc-volume-breakout.md) 查看同一份策略从历史回放到信号服务的完整实现。

研究交付包括 `report.md`、`performance.png`、`report.json`、分段交易明细及数据切分清单 `split-manifest.json`。数据目录由用户选择，大规模下载和报告输出放在源码及技能目录之外。

## 历史数据、回测和报告

先确定标的、到期周期、单笔金额和同时在途上限，再选数据区间。可下载 1、3 或 5 年完整历史。用 `market_data.py split --mode train-test --train-percent 80` 按时间顺序划分训练和样本外区间，训练比例可选 60、70、80、90。两段模式的 `report.md` 呈现样本外结果，`development-report.md` 记录训练、样本外结果及回测条件，共用图表。需要单独调参区间时使用训练、验证、测试三段模式。

需要 Python 3.11+。下载与切片使用标准库，生成图表需安装 `matplotlib`。在自己的数据目录运行以下命令，将 `$SKILL` 设为技能目录的绝对路径。切分和报告的输出目录使用新的路径。

```sh
python "$SKILL/scripts/market_data.py" download --symbol BTCUSDT --years 5 --output data/btc.csv
python "$SKILL/scripts/market_data.py" split --input data/btc.csv --output-dir runs/btc-splits --train-percent 60 --validation-percent 20
python "$SKILL/scripts/report.py" --split-dir runs/btc-splits --signals runs/btc-signals.csv --strategy-name MA-Cross --strategy-revision v1 --symbol BTCUSDT --duration-minutes 10 --stake 5 --payout-ratio 0.8 --max-concurrent 1 --output-dir runs/btc-v1
```

- 下载 Binance 公开归档的 BTCUSDT 或 ETHUSDT USDⓈ-M 成交 K 线，粒度为 1 分钟。默认以 UTC 当天为结束边界，往前取五年。用 `--end YYYY-MM-DD` 固定结束时间，或配合 `--start YYYY-MM-DD` 指定短区间。归档缺漏会中止。若最新日包尚未发布，可将 `--end` 调至已覆盖的日期。成交价是事件合约回测的代理价，报告标记数据口径。[Binance Public Data](https://github.com/binance/binance-public-data)
- 已有本地分钟数据时，直接从切片开始。CSV 表头为 `open_time,open,high,low,close,volume`，开盘时间为 UTC Unix 毫秒。生成报告时用 `--price-source` 指明实际来源。
- 事件合约的到期周期为 `10m`、`30m`、`1h`、`1d`。回测和报告的 `--duration-minutes` 对应填 `10`、`30`、`60`、`1440`。分钟 K 线的粒度用来读取行情。[币安事件合约到期时间](https://www.binance.com/zh-CN/support/faq/detail/172247f1c4b8401ab106fb63900f3825)
- 将自然语言转成可检查的策略，记录触发条件、参数、历史预热和决策时间。按时间顺序切分，训练选规则，验证选参数，冻结版本后再使用样本外区间。历史预热可读取决策前已完成的 K 线。价格、赔率、数据粒度和执行假设必须写进报告。
- 把策略产生的信号按时间顺序保存为 `signal_time,direction` CSV，UTC Unix 毫秒，方向只接受 `LONG` 或 `SHORT`。时间戳表示能作出决定的时点。使用一根分钟 K 线的收盘价时，信号时间至少是该 K 线开盘时间加 60 秒。引擎使用决策时点之后的下一分钟开盘价入场，按固定期限、固定单笔投入和指定盈利支付率结算。到期报价缺失会记录为未结算。
- 分段报告使用同一组执行参数，保留跳过与未结算原因。用 `--hypothesis` 写清实验目标，用 `--strategy-file` 记录策略代码或规则快照的校验和。`scripts/backtest.py` 也可单独回放单个区间。
- 交付时说明样本外结算笔数、盈亏、最大回撤及数据覆盖。保留失败结果与空样本，切换模型或调参时写入新版本及新报告目录。

## 实时行情与特征

为信号服务定义实时行情需求、预热窗口或训练与推理的特征口径时，阅读 [实时行情与策略特征](references/realtime-market-data.md)。在客户端预览或模拟时核对已收盘窗口和预热要求。自行部署的实盘执行程序负责准备行情窗口，并与离线研究使用一致的数据口径。

## 导出项目或接入已有信号服务

使用 [信号项目与服务规范](references/signal-project.md) 处理本机项目和外部信号。用 `scripts/signal_project.py` 导出可启动的 Python 工程，保留策略代码、依赖锁和所需模型文件。已有服务可以保留自己的语言和目录，按 `cuefleet.signal.v1` 暴露 `GET /health` 与 `POST /v1/predict`。推送式信号源需要适配器提供这两个接口。

向用户交付时给出可直接选择的工程根目录。根目录包含 `cuefleet_signal/signal.json`、启动脚本、依赖锁，以及推理所需的代码和权重。「信号服务 → 加载策略工程」先检查文件，再由用户启动服务。旧版入口为「我的信号」。参见 [快速上手和可运行示例](README.md)。

用 `scripts/check_signal_service.py` 验证健康检查、行情声明、预测方向和观测时间。加载工程或添加地址后，可在客户端预览信号，也可用模拟任务对照执行记录。

## 实盘接入

按 [实盘接入指南](docs/quickstart.md#实盘接入) 对接已授权的 CueFleet 本机交易 API。用户的执行程序读取策略信号和当前市场条件，在同一台机器上提交订单并管理回执。策略进程只接触行情和信号，交易密钥、账号、金额由执行程序保存和配置。

先用「仅查询」验证账号和市场参数。生成执行程序时，保留行情新鲜度检查、无信号跳过、单笔和在途限制，以及每笔意图的 UUID。结果未知时核对原回执和交易所订单。切换「允许下单」或发送实盘订单需要操作人明确授权。

维护已有的独立参考程序时，阅读 [本地 Runtime v1](references/runtime.md) 的兼容条件。
