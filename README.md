**中文** | [English](README.en.md)

# deliverable-acceptance —— 通用 Agent 验收标准

> A platform-neutral acceptance standard for agent deliverables. 四层 27 项，不预设平台、不预设交付形态。
>
> 一句话：**它不告诉你"文件在不在"，它告诉你"声明的东西到底会不会生效"，以及"没验的部分不许算通过"。**

---

## 这是什么

一份可以直接当**技能（skill）**装进各种 agent、也可以直接当**人工检查表**用的验收标准。核心是四层：

| 层 | 验什么 | 花模型额度 |
|---|---|---|
| **L1 结构** | 交付物形态、底座组件、扩展点与能力单元是否就位、需求覆盖、凭据、体积、链接范围 | 否 |
| **L2 引用** | **悬空引用**——文件里点名的路径/入口/单元是否真实存在 | 否 |
| **L3 契约** | 声明能不能被**目标平台的真实加载器**接受（不是"正则看起来对"） | 否 |
| **L4 能力** | 运行时可见性、端到端冒烟、行为面 `pass^k` 与"装/不装"对照 | **是（需授权）** |

外加一套判定纪律：五种结论（`pass`/`fail`/`warn`/`skip`/`error`）、**每条必须给实测值与阈值**、`skip` 三类分开写（不适用/本次未执行/无法执行）、`error` 双向归因、**未跑 ≠ 通过**、豁免只走报告且不得沿用。

## 它不做什么

- 不做质量评测：模型对话质量、文风、审美不在判定范围内。
- 不做修复：**只验不改**。
- 不内置任何平台知识：平台相关断言全靠使用者在 §六「平台适配清单」里现场填。

## 目录

```
deliverable-acceptance/
├── SKILL.md
├── README.md     # 使用说明（中文）
├── README.en.md  # 使用说明（English）
├── LICENSE.md    # MIT License
└── .gitattributes      # 标准正文（自包含，184 行）
```

**为什么标准只有一个文件**：标准里所有平台相关的部分都做成了"槽位"，由使用者填写；平台证据不进标准正文，所以 `SKILL.md` 能保持单文件、拷到哪都能用。README 与许可证是给人看的，不影响它作为技能的可用性。

---

## 3 步上手

1. **装**：把 `deliverable-acceptance/` 整个目录拷到你所用的 agent 的技能目录（见下表）。
2. **填**：按 `SKILL.md` §六 的**十二个槽位**填一份你这个平台的适配表（同一份标准在不同平台上填法不同，这是设计而不是缺陷）。
3. **跑**：把你的交付物、能力要求清单、体积上限、额度上限组成一张**验收单**，按 §四 的执行顺序跑 L1→L2→L3（不花额度），再决定要不要授权 L4。

> **没填槽位就不能用**——依赖未填槽位的判据一律记 `error`，**禁止用推测填空**。这是这份标准能保持"通用"的代价，也是它不骗人的地方。

---

## 各家 Agent 的适配操作

### 技能安装位置总表

| Agent | 项目级 | 用户级 | 备注 | 来源 |
|---|---|---|---|---|
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` | 还支持嵌套目录、`<plugin>/skills/`、企业托管目录；**保留名** `synced`、`anthropic-skills` | ✅ [官方文档](https://code.claude.com/docs/zh-CN/skills) |
| **Codex** | `.agents/skills/<name>/`（含各级父目录与仓库根） | `~/.agents/skills/<name>/` | 另有 ADMIN 级 `/etc/codex/skills` 与 SYSTEM 内置；**重名技能不合并**，两个都会出现在选择器里 | ⚠️ 第三方核对（官方站 403）；旧资料另有 `.codex/skills/`、`~/.codex/skills/` 说法，**两说并存，请在装好的版本上实测** |
| **WorkBuddy（腾讯）** | 未取证 | `~/.workbuddy/skills/<name>/SKILL.md` | 目录结构为 `SKILL.md` + `references/` + `scripts/` + `assets/`；调用 `@skill:<name>` 或 `/skills`；有技能市场 SkillHub | ⚠️ 第三方（腾讯云社区文章）+ 一个真实在用的 WorkBuddy 技能仓库佐证（本地目录 junction 到 `~/.workbuddy/skills`） |
| **Cursor** | `.cursor/skills/`、`.agents/skills/` | `~/.cursor/skills/`、`~/.agents/skills/` | 支持**递归子目录**（按类别分组）；为兼容还读 `.claude/skills/`、`.codex/skills/`、`~/.claude/skills/`、`~/.codex/skills/` | ✅ [官方文档](https://cursor.com/docs/skills) |
| **Gemini CLI** | `.gemini/skills/<name>/` | 见官方文档 | 有 `skill-creator` 元技能与"发现层级/别名"机制；注意：官方公告称免费档 / Google One 用户已于 2026-06-18 转向 Antigravity CLI | ✅ [官方文档](https://geminicli.com/docs/cli/creating-skills/) |
| **OpenCode** | `.opencode/skills/<name>/SKILL.md`、`.claude/skills/`、`.agents/skills/` | `~/.config/opencode/skills/`、`~/.claude/skills/`、`~/.agents/skills/` | 对 frontmatter 字段有**明确白名单**，未识别字段忽略；可用 `opencode.json` 的 `permission.skill` 按通配符允许/拒绝/询问 | ✅ [官方文档](https://opencode.ai/docs/en/skills/) |

**两个实务提醒**：

1. **多平台共存时用一个目录**：Cursor 同时读 `.claude/skills/`、`.codex/skills/`、`.agents/skills/`；OpenCode 也读 `.claude/skills/` 与 `.agents/skills/`。所以把技能放在 **`.agents/skills/`** 往往能一次被多个 agent 看到——但**别假设**，装好后按下面的"最小验证"逐家确认。
2. **同名技能的处理规则各家不同**：Codex 明确"**不合并，两个都列出**"；Claude Code 有完整的优先级表（企业 > 个人 > 项目，项目技能可覆盖同名捆绑技能）。这正是标准里 **L1-11** 要 `warn` 的原因——重名不一定出事，但必须有人知道哪一份生效。

---

### 槽位速填（十二槽位 → 各平台）

图例：✅ 官方文档可核实 ｜ ⚠️ 仅第三方来源 ｜ ❓ 未取证，请按 `SKILL.md` §六 自行取证

#### A. 能力单元目录与声明

| 槽位 | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **3 能力单元目录** | `.claude/skills/`、`~/.claude/skills/`、`<plugin>/skills/` | `.agents/skills/`、`~/.agents/skills/`、`/etc/codex/skills` ⚠️ | `~/.workbuddy/skills/` ⚠️ | `.cursor/skills/`、`.agents/skills/`、`~/.cursor/skills/`、`~/.agents/skills/` ✅ | `.gemini/skills/` ✅ | `.opencode/skills/`、`~/.config/opencode/skills/`、`.claude/skills/`、`.agents/skills/` ✅ |
| **入口文件名** | `SKILL.md` ✅ | `SKILL.md` ⚠️ | `SKILL.md` ⚠️ | `SKILL.md` ✅ | `SKILL.md` ✅ | `SKILL.md`（全大写）✅ |
| **可选资源目录** | `scripts/`、`references/`、`assets/`（自定义亦可） | `scripts/`、`references/`、`assets/` + `agents/openai.yaml` ⚠️ | `references/`、`scripts/`、`assets/` ⚠️ | `scripts/`、`references/`、`assets/` ✅ | `scripts/`、`references/`、`assets/` ✅ | 未限定 ✅ |
| **多来源与优先级** | 企业 > 个人 > 项目；项目技能覆盖同名捆绑技能 ✅ | 重名**都保留**，不合并 ⚠️ | ❓ | ❓（嵌套同名待取证） | 有"发现层级 + 别名"机制，细节见官方 ✅ | 重名需**跨所有位置唯一**，否则 troubleshoot ✅ |

#### B. 标识与元数据规则（对应 L3-01 / L3-02 / L3-05）

| 槽位 | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **6 标识符规则** | 未在文档中给出字符集正则；但 `name` 决定 `/` 命令名 ✅ | ❓ | ❓ | ❓ | ❓ | **`^[a-z0-9]+(-[a-z0-9]+)*$`**，1–64 字符、不得以 `-` 起止、不得连续 `--` ✅ |
| **必填元数据字段** | 文档称**所有字段可选**，仅 `description` 推荐（缺省时取正文首个非空行）✅ | **`name` + `description` 必填** ⚠️ | `name`、`description`（`agent_created` 可选）⚠️ | `name` + `description` ✅ | `name` + `description` ✅ | **`name` + `description` 必填**；`license`/`compatibility`/`metadata` 可选；**未知字段忽略** ✅ |
| **标识是否必须等于目录名** | 文档未强制（`name` 缺省取目录名）✅ | ❓ | ❓ | ❓ | ❓ | **强制**："Match the directory name that contains `SKILL.md`" ✅ |
| **`description` 上限** | 列表项合并文本截断于 **1,536 字符**（`description` + `when_to_use`）✅ | ❓ | ❓ | ❓ | ❓ | **1,024 字符** ✅ |
| **平台扩展字段**（标准里属 L3-05 非阻塞档） | `when_to_use`（注意是**下划线**）、`disable-model-invocation`、`user-invocable`、`allowed-tools`、`disallowed-tools`、`argument-hint`、`arguments`、`model`、`effort`、`context: fork`、`agent`、`background`、`hooks`、`paths`、`shell`、`metadata`、`license`、`compatibility` ✅ | `agents/openai.yaml`（图标、品牌色、`policy.allow_implicit_invocation`）⚠️ | `agent_created` ⚠️ | ❓ | ❓ | 只认 `name`/`description`/`license`/`compatibility`/`metadata` ✅ |

> **重要差异（会直接改变 L3-01 的"失败表现"一栏）**：
> **OpenCode** 白名单外字段静默忽略；**Claude Code** 官方明说"**frontmatter YAML 解析失败时仍会加载正文，但元数据为空**"——也就是**技能不会消失，只是永远匹配不上**。
> 这跟"整条技能被静默丢弃"是**两种完全不同的故障表现**。所以 L3-01 里"失败会怎样"的描述**必须按你实际用的平台实测后改写**，不能照抄。

#### C. 验证与冒烟手段（对应 L3-01 的"真实解析器"槽位、L4-02、L4-03）

| 槽位 | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **5 真实解析器 / 校验命令** | `claude plugin validate <skills 目录>`（v2.1.233+）✅；`--debug` 看解析错误 ✅ | ❓（`$skill-creator` 内置创建器会校验）⚠️ | `@skill:skill-creator` ⚠️ | 内置 `/create-skill` ✅ | 内置 `skill-creator` ✅ | ❓ |
| **9 隔离实例 / 冒烟** | 用 `--add-dir` 单独加载技能目录，不污染项目 ✅ | ❓ | ❓ | Cloud Agents **不读**未同步的用户级技能 ✅（可用来验证"项目级才有"） | ❓ | ❓ |
| **10 运行时可见性观测** | `What skills are available?`、`/skills`、`/context`、`/skill-doctor`；`--debug` 日志 ✅ | `/skills`、输入 `$`；**技能变更需重启** ⚠️ | `/skills` ⚠️ | `/` 菜单搜索技能名；**部分构建才暴露技能列表** ⚠️ | 见"发现层级"官方文档 ✅ | `skill` 工具的 `<available_skills>` XML ✅ |
| **12 前端扩展字段** | 不适用（技能无前端半） | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 |

> **L4-01（工具面探针）与 L4-04（行为面对照）各家都有现成抓手**：
> Claude Code 有 `claude plugin eval`（在隔离会话里跑"有插件 / 无插件"两遍，低于阈值**非零退出**，可挂 CI）+ `skill-creator` 插件的 `evals/evals.json` 循环——这正好就是标准里 L4-04 要的"**装 / 不装对照**"。见 [官方文档](https://code.claude.com/docs/zh-CN/skills) 的"评估和迭代技能"一节。

---

### 其余槽位（验收具体交付物时才需要）

槽位 1（交付物形态）、2（根锚点与必需组件）、10（链接扫描范围）、11（禁止声明清单）与"你要验的那份交付物"强相关，与 agent 平台弱相关，**这里给不出通用值**。填法示例（抽象示例，非任何真实产品）：

```yaml
# 你的适配表（示例片段）
slot1_deliverable: "一个自包含目录：1 个入口可执行体 + runtime/ 底座 + extensions/ 扩展目录"
slot2_anchor: "环境变量 APP_HOME；包根 = $APP_HOME/..；禁止写死盘符"
slot10_link_scope: ["runtime/profiles", "runtime/home"]   # 只扫这两棵子树
slot11_forbidden: ["shell-exec", "background-jobs", "network-egress"]
```

---

## 阴性对照：证明你的槽位填对了

标准的 §六 要求：**没有做过阴性对照的槽位，其判据按 `error` 处理**。
做法是造**故意做坏**的样本，确认平台**确实会拒绝**它——否则你填的规则只是"文档上这么写"，不是"实际这样"。

四个通用坏样本（改完记得改回来）：

| # | 坏样本 | 期望的失败表现 |
|---|---|---|
| 1 | 文件开头插入 **UTF-8 BOM** | 首行不再是 `---` → frontmatter 不被识别（OpenCode/Claude Code 官方都强调"首行必须是 `---`"） |
| 2 | `name` 改**大写**或加下划线 | 依赖平台字符集规则（OpenCode 明确拒绝） |
| 3 | `name` 与**目录名不一致** | OpenCode 会拒绝；其它平台可能接受——**这正是你要实测出来的差异** |
| 4 | **删掉 `description`** | 必填平台不加载；选填平台（Claude Code）退回取正文首行 |

每个平台跑一遍，把结果写进你的适配表。**一致性检查**：同一个坏样本在不同平台上表现不同 → 说明你的"目标平台"定义得不够窄，或者你其实需要两份适配表。

---

## 自检清单（发布 / 交付前）

- [ ] 十二个槽位都已填，或明确标注 `未取证`（未取证的判据必须记 `error`）
- [ ] 每个槽位都跑过至少一个**阴性对照**，并记下实际的失败表现
- [ ] 验收单齐备：交付物位置、能力要求清单、体积上限、额度上限、是否允许冒烟
- [ ] 报告里 `不适用` / `本次未执行` / `无法执行` **三类分开列**
- [ ] 报告里每条都有**实测值 + 阈值**（拿不出来的按"未检查"处理）
- [ ] 所有"没测"的项都写进了**未做项清单**，没有混进通过项
- [ ] 豁免项逐条写了理由与影响面，且**本次重新实测过**（没有沿用历史豁免）

---

## 已知限制（标准正文 §五 有完整列表）

1. **平台知识不在标准里**——槽位填错，标准自己发现不了。缓解：阴性对照 + 第二人复核槽位表。
2. **平台升级后 L3 必须重新取证**——L3 绑的是"目标平台的加载器实现"，平台一变，判据可能从"判对"变成**静默判错**。
3. **行为面结论只在小范围内成立**——L4-04 的结果不能外推成"这个 agent 会干活"。
4. **视觉与审美**不判，只判"能不能装"。
5. **目标机环境差异**覆盖不到（换机后的路径、权限、杀软、端口）。

---

## 开源说明

### 本仓库的许可：MIT

见 [`LICENSE.md`](LICENSE.md)。原文取自 SPDX 许可清单（`licenseId: MIT`，`isOsiApproved: true`），**正文逐字未改**，只有版权行是填的。

**它是 OSI 认可的开源许可**：任何人可以自由使用、修改、分发、**商用**、再许可；唯一义务是**保留版权声明与本许可全文**（在副本或实质性部分中）。GitHub 会把它识别为 **MIT license**，仓库归类为开源。

**署名（推送前必须处理）**：MIT 要求署名，格式 `Copyright (c) <年> <版权人>`。当前文件里是占位符：

```
Copyright (c) 2026 <COPYRIGHT HOLDER>
```

> 这个占位符**我故意没替你编**——名字或组织名是你的决定。告诉我之后我一条命令替换掉；**在它被清掉之前我不会提交**（提交步骤里有一道闸门会检查并直接失败）。

### 发布前请确认

- 这份标准**不含任何平台或产品的私有约定**（已做零耦合扫描，见下）。
- 如果你另有一份"绑定了具体平台/产品"的专用版本，**不要一起发布**——那类文件里通常含目录契约、内部路径与实现细节。
- 本文引用了若干第三方产品的文档链接，均为**事实性引用与摘要**，未复制其文档正文。请保持这个做法：**引用可以，抄正文不行。**

### 来源与致谢

| 来源 | 用途 |
|---|---|
| [Agent Skills 官方规范](https://agentskills.io/specification) | 能力单元格式、渐进披露预算 |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | 质量维度命名（只借维度名） |
| τ-bench（[论文](https://arxiv.org/html/2406.12045v1)） | `pass^k` 可靠性度量 |
| SkillsBench | with/without 对照 + 先跑 oracle 自证验收脚本 |
| [MCP Conformance](https://github.com/modelcontextprotocol/conformance) | 冻结需求集、逐项豁免、`not_scored` 三分类、失效豁免反查 |
| [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) | 供应链字段结构（**只借结构，不抄文本**；该文档为 CC BY-SA 4.0，有传染性） |

平台事实来源见上文各表的"来源"列。**取证日期：2026-09-29。**

---

## 更新这个标准

- 判据改动请递增版本号（正文末尾有"本版说明"），并在改动处写明**驱动原因**——未来的验收员需要知道每条为什么这么定，才不会随手放宽。
- 新增平台适配：只改本 README 的表格 + 填一份该平台的槽位表，**不必改 `SKILL.md`**（这正是槽位设计的目的）。

---

## English summary

A platform-neutral, four-layer (structure / references / contract / capability) acceptance standard for agent deliverables, with 27 criteria and an explicit verdict discipline. It ships **no platform knowledge**: all platform-specific assertions live in a 12-slot adaptation checklist you fill in per platform. Unfilled slots make the dependent criteria `error`, never `pass`. Includes per-platform setup notes for Claude Code, Codex, WorkBuddy, Cursor, Gemini CLI and OpenCode, plus a negative-control procedure to prove your slot values are real.
