# Model Fit v0.2：借鉴什么，不搬什么

研究日期：2026-09-09。对照的是所提供的 v0.1.0-preview 实际源文件，而非只看前次讨论。以下项目是设计参考，不是对其成熟度、效果或节省比例的背书。链接指向当时检查的上游页面；不把星数或提交量当作运行质量证明。

## 筛选标准

只有能改善「推荐是否可用、总消耗、误操作、交接或安装」且不增加普通用户日常配置负担的内容，才进入本次升级。v0.1 已经有校准、确认、分段、验收与修正上限；本次不把已有功能重新包装为新增。

## 真正吸收的内容

| 参考 | 值得借鉴 | v0.2 的落地 | 类型 |
|---|---|---|---|
| `gitguffaw/codex-router` 的当前模型/档位发现；官方 `model/list` | 名单来自当前运行环境，不来自写死的旗舰排行榜 | 明确当前客户端与账号；隐藏选项、档位、分页、默认值与正在使用值分别处理；无授权接口时走一次截图校准 | 强化已有校准，不声称新增全自动探测器 |
| `paulpas/agent-skill-router` 的 `ai-model-selector` | 能力要求、成本、上下文要求分开判断 | 先过滤不满足要求的配置，再用少量定性因素比较；没有大矩阵、权重表或虚构分数 | 强化选档规则 |
| `scottconverse/multi-model-routing-skill` 的私有本机配置与安装保护 | 产品更新不应覆盖用户的本地事实 | 可选安装器默认预览；备份在扫描目录外；不碰校准；合法 v0.1 配置可继续使用 | 新增安装工具，保留既有存储设计 |
| 同项目对机械执行与判断任务的区分 | 能不能可靠检查，比任务“看上去简单”更重要 | 简短高风险请求不能机械降档；大量已定义转换不因数量直接最高档；验收规则沿用 v0.1 | 强化策略而非新增复杂流程 |
| `RouteLLM` 的质量/成本权衡与评估意识 | 省的是完成任务的总代价，不是固定追求最低单价 | 允许保持当前配置或只降档；不知道相对成本就不称最便宜；不为分段而分段 | 强化总消耗判断 |
| 官方用量/速度文档 | 速度设置也可能增加消耗，与推理档位不同 | 只有已知当前开启、存在更经济的可选速度且任务不要求快时，补一行提醒；不加默认第三个调参栏目 | 新增条件提醒 |
| 上游工程测试与官方渐进加载 | 用户流程简单，测试和维护在后台 | 加离线测试、CI、安装失败回滚；校准按需读，四份核心规则继续由同一套源生成 | 新增工程检查；保留轻量运行 |

## 有意不采用

**不接入跨供应商自动委派。**它会改变本产品“当前平台、用户手动选、明确确认”的定位，还会引入其他登录、账单和上下文传递。

**不把模型缓存当作账号可用清单。**上游缓存读取脚本明确读取本地历史文件，部分缺失/过期提示还建议真实模型调用刷新。这里不采用收费试调用或扫描账号文件的方式。官方接口未暴露时，人工校准是正常降级，不是故障。

**不采用关键字分档与固定省钱算式。**`model-hierarchy-skill` 的测试文件包含关键词分类器、固定模型与价格，以及假定任务比例下的成本计算；这些测试不等于真实 agent 对每项任务的路由质量。不给 Model Fit 搬入“看到 code 就中档”“失败就最高档”或固定节省十倍的说法。

**不采用 ai-model-selector 的强制跨平台三候选、加权打分矩阵和完整后备架构。**只吸收约束优先的思路。普通用户不应为了一个任务填写预算/延迟/权重表。

**不运行常驻服务、自动评测、排行榜轮询或模型自我竞赛。**这些可能让预判本身成为额外开销。明确任务无额外调查，跟进任务只评估变化。

**不增加自动升级、付费建议、日志上传或真实节省仪表盘。**本次没有可靠的计费观测与因果对照，不伪造百分比，也不采集用户任务。

## 用户实际看到的变化

四个入口不变，仍然是「调用＋任务」→「简短推荐」→「手动选择」→「确认开始」。建议更有可能直接说“保持当前配置”“当前模型降一档即可”“没有有意义的备选”。不知道的事实只在影响决策时说明。

分段结束后，给一个保留关键决定和结果位置的短交接，以及下一条可复制调用。交接不是自动启动下一阶段，也不承诺减少既有聊天历史。

## 当前实现边界

这是本地源文件升级包，没有在用户电脑安装，没有发布到 GitHub。离线测试是真实运行的文件与安装检查；52 个模型行为场景仍是待执行规格。客户端切换后能否持续遵守规则、选档质量和实际省量，必须用真实任务验证，不能由 CI 静态检查代替。

## 核查来源

- https://github.com/gitguffaw/codex-router
- https://github.com/scottconverse/multi-model-routing-skill
- https://github.com/scottconverse/multi-model-routing-skill/blob/main/install.py
- https://raw.githubusercontent.com/scottconverse/multi-model-routing-skill/main/scripts/codex_models.sh
- https://github.com/paulpas/agent-skill-router/blob/main/skills/agent/ai-model-selector/SKILL.md
- https://github.com/lm-sys/RouteLLM
- https://github.com/zscole/model-hierarchy-skill
- https://raw.githubusercontent.com/zscole/model-hierarchy-skill/main/tests/test_classification.py
- https://developers.openai.com/codex/app-server/
- https://developers.openai.com/codex/skills/
- https://developers.openai.com/codex/pricing/

实现未复制或打包上游代码；这些来源支持设计取舍，不证明 Model Fit 的运行结果。[检查记录](../VALIDATION.md)
