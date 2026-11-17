<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/cuefleet-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/cuefleet-logo-light.svg">
    <img src="assets/cuefleet-logo-light.svg" alt="CueFleet" width="144">
  </picture>
</p>

<h1 align="center">币安事件合约策略 Skill</h1>

<p align="center">用 AI 把 BTC、ETH 事件合约交易思路变成可回测的策略，部署信号服务，再通过 CueFleet 接入实盘。</p>

<p align="center">
  <a href="docs/quickstart.md#实盘接入"><strong>实盘接入指南</strong></a> ·
  <a href="docs/btc-volume-breakout.md">跑一遍真实行情案例</a> ·
  <a href="SKILL.md">给 AI 的 Skill</a>
</p>

<p align="center">
  <img src="assets/research-to-live.webp" alt="从研究到实盘。用 Codex、Claude Code、Grok 或 Gemini 编写和验证策略，部署信号服务，再由同机执行程序通过 CueFleet 本机交易 API 接入币安实盘。" width="1024">
</p>

## Skill 能交付什么

- **可复现的研究报告**。准备 BTC、ETH 公开历史行情，按时间切分样本，输出逐笔记录、样本外表现和盈亏三联图。
- **可部署的信号工程**。打包 Python 策略、依赖和模型文件，检查行情预热、预测方向和时间戳。已有服务可按 [信号协议](references/signal-project.md) 接入。
- **实盘接入配置**。把账号、金额和限额交给同机执行程序，由该程序读取策略信号，调用 CueFleet 本机交易 API 下单并查询原回执。

## 真实行情案例

**BTC 放量突破**使用一个月的 44,640 根公开分钟 K 线。同一份规则用于历史回放和实时预测，样本外结果如实记录。

[复现案例](docs/btc-volume-breakout.md) · [查看盈亏三联图](assets/btc-volume-breakout-report.png) · [查看策略代码](examples/btc_volume_breakout.py)

## 从你的交易思路开始

把仓库交给支持读取项目文件的 AI 工具，也可以贴入 [Skill 指令](SKILL.md) 和相关接口说明。用这段话开始，再换成你自己的策略条件。

> 阅读 `SKILL.md`。我想研究 BTCUSDT 10 分钟事件合约的放量突破。用真实历史行情做样本外验证，给我一份报告、一个可部署的信号工程，以及 CueFleet 实盘接入所需的配置清单。

---

[Telegram @lazyer_trading](https://t.me/lazyer_trading) · [CueFleet 官网](https://cuefleet.com/) · [MIT 许可证](LICENSE)
