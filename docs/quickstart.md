# 搭建自己的策略信号

先用示例验证服务，再换上自己的策略。用两根已收盘 K 线判断方向的示例只需 Python 标准库，便于检查接入流程。

## 1. 生成工程

安装 Git 和 Python 3.11+，然后在终端运行以下命令。

```sh
git clone https://github.com/CueFleet/event-contract-skill.git
cd event-contract-skill
python scripts/signal_project.py --project examples --include market_momentum.py --strategy market_momentum:predict --symbol BTCUSDT --warmup 2 --name "BTC 双 K 线示例" --output my-btc-signal
```

生成的 `my-btc-signal/` 就是可加载的工程目录。再次导出时请换一个输出目录。系统将 Python 命令命名为 `python3` 时，将命令里的 `python` 换成 `python3`。

## 2. 接入 CueFleet

**Windows 0.5.87 或以上**

1. 进入「AI 交易 → 信号服务 → 加载策略工程」，选择整个 `my-btc-signal` 文件夹。
2. 在信号卡片点击「启动服务」，然后点「预览信号」。

**按地址接入（已有服务、Linux WebUI 0.5.86 或使用 0.5.86 的 Windows）**

在运行客户端执行器的机器上，从仓库根目录启动示例。

```sh
python my-btc-signal/cuefleet_signal/start.py --port 18781
```

保持服务运行，在 CueFleet 的「AI 交易」中添加 `http://127.0.0.1:18781`，测试连接后保存。策略运行在另一台机器时，用它的 HTTPS 服务地址和可选的访问密钥。[外部服务接口](../references/signal-project.md#外部服务接口)

如需确认两个端点都能响应，在仓库根目录另开终端运行检查命令。

```sh
python scripts/check_signal_service.py --url http://127.0.0.1:18781 --symbol BTCUSDT --period 10m
```

看到 `"ok": true` 即通过合成行情检查。预览可能返回 `NO_SIGNAL`，表示当前条件下没有方向。

## 3. 在模拟里验证

Windows 0.5.87 或以上进入「AI 交易 → 本地跟单 → 我的模拟」，新建任务，选择示例服务、BTCUSDT 和 10 分钟，到卡片启动并查看记录。0.5.86 支持在信号卡片启动模拟，按该版本的权限提示操作。

## 换成自己的策略

- **用编码智能体生成**。打开仓库目录，让 Codex、Claude Code 等阅读 [SKILL.md](../SKILL.md)。给出标的、周期、金额、同时在途数和策略思路，请它用时间切片回测，生成报告并导出工程根目录。
- **已有 Python 模型**。参考 [示例策略](../examples/market_momentum.py) 的 `predict(request)` 入口，将模型文件、特征处理和带哈希的依赖锁一起导出。正式运行前可以用相同的检查命令校验接口。
- **已有信号服务**。实现 [`cuefleet.signal.v1`](../references/signal-project.md) 两个端点，在客户端添加根地址。行情输入和预热格式见 [实时行情](../references/realtime-market-data.md)。

策略工程会在客户端执行器所在机器上运行，请加载自己编写或已审阅的代码。
