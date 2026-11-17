# 自研策略实盘接入

策略服务根据已收盘行情输出方向。运行在 CueFleet 同一台机器上的执行程序读取信号，通过 CueFleet 本机交易 API 向已授权的币安账号下单，并核对订单回执。

## 实盘接入

1. 在 CueFleet 连接币安账号，在页眉打开「API 设置 → 接口文档」。使用已授权交易的账号和有效的 CueFleet API 权限（VIP 或注册后 15 天试用期）。配置账号、单笔上限和本机 API 密钥，保存并启动服务。
2. 在「仅查询」模式跑通执行程序。按客户端显示的本机地址连接，默认是 `http://127.0.0.1:17687`。读取 `GET /v1/status`、`GET /v1/accounts` 和 `GET /v1/accounts/{accountId}/market`，确认账户、标的周期、支付率和交易限额。
3. 执行程序审阅和验收完成后，由操作者切换「允许下单」并保存。通过 `POST /v1/orders` 发送符合配置的方向信号。允许下单后，CueFleet 按已授权的账户和规则提交真实订单，提交时无逐笔确认弹窗。

交易请求里的账号、金额和周期来自部署时的配置，`payoutRatio` 来自对应账号、标的、周期及方向的最新市场数据。每笔交易意图保存一个 UUID 作为 `Idempotency-Key`。结果未知时，用原编号查 `GET /v1/requests/{requestId}`，再对照交易所记录。执行程序单独保管 CueFleet 本机 API 密钥。

| 一次执行 | 对应接口 |
| --- | --- |
| 取策略方向和观测时间 | 信号服务 `POST /v1/predict` |
| 核对账户与交易条件 | CueFleet `GET /v1/accounts/{accountId}/market` |
| 提交并核对原订单 | CueFleet `POST /v1/orders`、`GET /v1/requests/{requestId}` |

订单字段与响应以客户端「接口文档」和本机 `GET /v1/openapi.json` 为准。[官网 API 交易说明](https://cuefleet.com/#api)

## 从策略到信号服务

- **从头开发**。把 [SKILL.md](../SKILL.md) 和仓库目录交给编码智能体。说明标的、到期周期、交易金额、同时在途数和你的策略思路，让它交付可复现报告、信号工程和执行程序所需的配置清单。[真实行情案例](btc-volume-breakout.md)
- **已有 Python 策略**。保持现有模型和特征代码，提供 `predict(request)`，将依赖锁、代码和权重一起导出。信号服务输出 `LONG`、`SHORT` 或 `NO_SIGNAL`。[信号工程规范](../references/signal-project.md)
- **已有服务**。实现 `cuefleet.signal.v1` 的 `GET /health`、`POST /v1/predict`，由执行程序按你的部署地址调用。[信号协议与行情结构](../references/realtime-market-data.md)

## 上线前验证

运行 [案例的服务校验](btc-volume-breakout.md#导出和部署信号服务)，确认健康检查、行情字段和预测输出。对执行程序，可先用「仅查询」校验账户和市场参数。Windows 0.5.87 或以上还可从「AI 交易 → 信号服务」加载工程或添加服务地址，预览信号并在「本地跟单」创建模拟任务。策略工程以部署机器上的用户身份运行，请先审阅要加载的代码。

若维护仓库里的 `scripts/runtime.cjs` 参考程序，先阅读 [Runtime 兼容说明](../references/runtime.md#控制台对接条件)。目前公开本机 API 的实盘接入方式以上文为准。

## 联系方式

[Telegram @lazyer_trading](https://t.me/lazyer_trading)
