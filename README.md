<p align="center">
  <img src="assets/cover.webp" alt="CueFleet 币安事件合约策略 Skill" width="900">
</p>

<h1 align="center">币安事件合约策略 Skill</h1>

<p align="center">用 Codex、Claude Code 等编码智能体编写策略，回测想法，再把信号接入 CueFleet 模拟跟单。</p>

<p align="center">
  <a href="docs/quickstart.md"><strong>快速上手</strong></a> ·
  <a href="SKILL.md">Skill 指令</a> ·
  <a href="references/signal-project.md">接口规范</a> ·
  <a href="https://cuefleet.com/">CueFleet 官网</a>
</p>

## 这个仓库有什么

| 任务 | 提供的工具 |
| --- | --- |
| 准备历史行情 | 下载 BTCUSDT / ETHUSDT 的公开分钟 K 线，按时间划分训练和样本外区间 |
| 验证策略 | 生成量化报告、交易明细，以及累计、日度、月度盈亏三联图 |
| 接入信号 | 导出可启动的 Python 工程，或验证已有服务是否兼容 `cuefleet.signal.v1` |

## 先运行一个示例

在安装了 Git 和 Python 3.11+ 的电脑上打开终端。

```sh
git clone https://github.com/CueFleet/event-contract-skill.git
cd event-contract-skill
python scripts/signal_project.py --project examples --include market_momentum.py --strategy market_momentum:predict --symbol BTCUSDT --warmup 2 --name "BTC 双 K 线示例" --output my-btc-signal
```

在 CueFleet Windows 0.5.87 或以上打开「AI 交易 → 信号服务 → 加载策略工程」，选择 `my-btc-signal` 文件夹。启动服务并预览信号，再到「本地跟单 → 我的模拟」创建跟单。[查看完整步骤，包括按地址接入](docs/quickstart.md)

## 用自己的策略

将仓库目录交给你的编码智能体，告诉它标的、周期和策略思路。可以从下面这段提示词开始。

> 阅读 `SKILL.md`。我想研究 BTCUSDT 10 分钟事件合约，单笔模拟 5 USDT，最多同时 5 笔。用已收盘的分钟 K 线实现策略，按时间划分训练与样本外区间，生成回测报告，并导出可在 CueFleet 加载的信号工程。用合成行情校验服务接口。

已有策略服务可按 [信号协议](references/signal-project.md) 提供 `GET /health` 和 `POST /v1/predict`。回测使用的价格、支付率和执行假设会记在报告中。

[MIT 许可证](LICENSE)
