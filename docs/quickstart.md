# 搭建自己的策略信号

由策略服务输出信号，自建执行程序读取信号并通过 CueFleet 本机交易 API 接入实盘。

## 实盘接入

1. 在客户端页眉打开「API 设置 → 接口文档」。准备已授权交易的币安连接账号，以及有效的 CueFleet API 权限（VIP 或注册后 15 天试用期）。
2. 在「API 设置」配置授权账号、单笔上限和本机 API 密钥。保存并启动服务。先保持「仅查询」，由和 CueFleet 运行在同一台机器的策略执行程序读取 `GET /v1/status`、`GET /v1/accounts` 及 `GET /v1/accounts/{accountId}/market`，确认账号、交易限制和当前支付率。
3. 审阅、验证执行程序后，由操作者切换「允许下单」并保存。你的执行程序按客户端「接口文档」将有效方向交给 `POST /v1/orders`。每笔意图使用一个 `Idempotency-Key`，结果未知时沿用原编号查询 `GET /v1/requests/{requestId}`。启用后会使用真实资金，提交时无逐笔弹窗。

本机服务默认监听 `http://127.0.0.1:17687`，实际地址以客户端为准。执行程序使用 CueFleet 本机 API 密钥，策略模型只需读取行情并返回方向。了解 [官网 API 交易流程](https://cuefleet.com/#api)。

当前 Windows 0.5.87 的「AI 交易 → 信号服务」和「本地跟单」用于信号预览与模拟。实盘请按客户端的本机交易 API 契约自行对接。仓库的 `scripts/runtime.cjs` 参考实现要求控制台提供显式 `executionMode`，现行正式 API 未提供这个字段。[Runtime 兼容说明](../references/runtime.md#控制台对接条件)

## 模拟快速上手

### 1. 生成工程

安装 Git 和 Python 3.11+，然后在终端运行以下命令。

```sh
git clone https://github.com/CueFleet/event-contract-skill.git
cd event-contract-skill
python scripts/signal_project.py --project examples --include market_momentum.py --strategy market_momentum:predict --symbol BTCUSDT --warmup 2 --name "BTC 双 K 线示例" --output my-btc-signal
```

生成的 `my-btc-signal/` 就是可加载的工程目录。再次导出时请换一个输出目录。系统将 Python 命令命名为 `python3` 时，将命令里的 `python` 换成 `python3`。

### 2. 接入 CueFleet

**Windows 0.5.87 或以上**

1. 进入「AI 交易 → 信号服务 → 加载策略工程」，选择整个 `my-btc-signal` 文件夹。
2. 在信号卡片点击「启动服务」，然后点「预览信号」。

**按地址接入（已有服务、Linux WebUI 0.5.86 或使用 0.5.86 的 Windows）**

在运行客户端执行器的机器上，从仓库根目录启动示例。

```sh
python my-btc-signal/cuefleet_signal/start.py --port 18781
```

保持服务运行，在 CueFleet 的「AI 交易」中添加 `http://127.0.0.1:18781`，测试连接后保存。策略运行在另一台机器时，用它的 HTTPS 服务地址和可选的访问密钥。[外部服务接口](../references/signal-project.md#外部服务接口)

如需用合成行情检查两个端点，在仓库根目录另开终端运行以下命令。看到 `"ok": true` 即通过。

```sh
python scripts/check_signal_service.py --url http://127.0.0.1:18781 --symbol BTCUSDT --period 10m
```

### 3. 创建模拟任务

Windows 0.5.87 或以上进入「AI 交易 → 本地跟单 → 我的模拟」，新建任务，选择示例服务、BTCUSDT 和 10 分钟，到卡片启动并查看记录。0.5.86 支持在信号卡片启动模拟，按该版本的权限提示操作。

## 换成自己的策略

- 打开仓库目录，让 Codex、Claude Code 等阅读 [SKILL.md](../SKILL.md)。给出标的、周期、金额、同时在途数和策略思路，请它用时间切片回测并导出工程。
- 使用自己的 Python 模型时，按 [示例](../examples/market_momentum.py) 实现 `predict(request)`，将模型文件、特征处理和带哈希的依赖锁一起导出。
- 已有信号服务可实现 [`cuefleet.signal.v1`](../references/signal-project.md) 两个端点，在客户端添加根地址。行情与预热格式见 [实时行情](../references/realtime-market-data.md)。

策略工程会在客户端执行器所在机器上运行，请加载自己编写或已审阅的代码。
