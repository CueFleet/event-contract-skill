# BTC 放量突破案例

用一份规则走完真实历史回测、信号服务导出，再核对实盘接口。案例使用 BTCUSDT 永续合约一分钟 K 线，交易场景为 10 分钟到期的事件合约。

## 研究和回测

最新一根已收盘 K 线的收盘价突破前 30 根最高价或最低价，且成交量至少是前 30 根中位数的 1.5 倍时，输出 `LONG` 或 `SHORT`。其他情况输出 `NO_SIGNAL`。回测与服务共用 [同一份策略代码](../examples/btc_volume_breakout.py)，决策只使用当时已收盘的行情。

在仓库根目录运行。需要 Python 3.11+，绘图需要 `matplotlib`。

```sh
python -m pip install matplotlib
python scripts/market_data.py download --symbol BTCUSDT --start 2025-05-01 --end 2025-06-01 --output runs/btc-1m.csv
python examples/btc_volume_breakout.py --candles runs/btc-1m.csv --signals runs/btc-signals.csv
python scripts/market_data.py split --input runs/btc-1m.csv --mode train-test --train-percent 70 --output-dir runs/btc-splits
python scripts/report.py --split-dir runs/btc-splits --signals runs/btc-signals.csv --strategy-name "BTC Volume Breakout" --strategy-revision 1 --strategy-file examples/btc_volume_breakout.py --hypothesis "Evaluate the fixed volume breakout rule on an unseen period." --symbol BTCUSDT --duration-minutes 10 --stake 5 --payout-ratio 0.8 --max-concurrent 1 --output-dir runs/btc-report
```

这段历史包含 44,640 根 K 线。在固定 5 USDT、盈利支付率 80%、最多同时一笔持仓的假设下，样本外结算 461 笔，盈亏 −424.00 USDT。回测使用永续成交 K 线作为代理价。报告按日期保留样本外区间、跳单原因和逐笔记录，便于判断策略是否值得继续研究。

[查看这次回测的三联图](../assets/btc-volume-breakout-report.png) · 本地报告见 `runs/btc-report/report.md`。

## 导出和部署信号服务

```sh
python scripts/signal_project.py --project examples --include btc_volume_breakout.py --strategy btc_volume_breakout:predict --symbol BTCUSDT --warmup 31 --name "BTC Volume Breakout" --output runs/btc-signal
python runs/btc-signal/cuefleet_signal/start.py --port 18781
```

在另一个终端校验服务。校验工具使用合成行情检查健康状态、行情声明、预测格式和时间戳。

```sh
python scripts/check_signal_service.py --url http://127.0.0.1:18781 --symbol BTCUSDT --period 10m
```

## 接入实盘

由运行在 CueFleet 同一台机器上的执行程序读取可靠的已收盘行情，调用信号服务 `POST /v1/predict`。程序核对信号和行情时间后，从 CueFleet 本机 API 查询授权账号、当前支付率和限额，再按用户配置提交下单请求并核对原回执。实际运行所需的行情源、账号、金额和运行权限由部署者配置。

[看实盘配置和接口对照](quickstart.md#实盘接入)
