[中文](README.md) | **English**

# deliverable-acceptance — a platform-neutral acceptance standard for agent deliverables

[![validate](https://github.com/ershicat/deliverable-acceptance/actions/workflows/validate.yml/badge.svg)](https://github.com/ershicat/deliverable-acceptance/actions/workflows/validate.yml)

> Four layers, 27 criteria, no platform assumptions, no deliverable-shape assumptions.
>
> In one line: **it does not tell you whether the files are there — it tells you whether the declared things actually take effect, and it refuses to count "not verified" as "passed".**

---

## What this is

An acceptance standard you can install as a **skill** into various agents, or use directly as a **human checklist**. It has four layers:

| Layer | What it verifies | Model budget |
|---|---|---|
| **L1 Structure** | Deliverable shape, runtime base components, extensions and capability units in place, requirement coverage, credentials, size, link scope | No |
| **L2 References** | **Dangling references** — do the paths, entry points and units named inside files actually exist | No |
| **L3 Contract** | Can the declarations be accepted by the **target platform's real loader** (not "looks right to a regex") | No |
| **L4 Capability** | Runtime visibility, end-to-end smoke, behavioural `pass^k` and with/without comparison | **Yes (needs authorization)** |

Plus a verdict discipline: five verdicts (`pass`/`fail`/`warn`/`skip`/`error`), **measured value + threshold required for every item**, `skip` split three ways (not applicable / not executed / cannot execute), `error` attributed in both directions, **not-run ≠ passed**, and exemptions that only ever live in the report and may never be inherited from a previous run.

## What it does not do

- No quality evaluation: conversational quality, tone, aesthetics are out of scope.
- No repair: **verify only, never modify**.
- No built-in platform knowledge: every platform-specific assertion comes from the 12-slot adaptation checklist you fill in.

## Layout

```
deliverable-acceptance/
├── SKILL.md                        # the standard itself (self-contained, 184 lines)
├── README.md / README.en.md        # usage guide (Chinese / English)
├── LICENSE.md                      # MIT License
├── .editorconfig                   # editor-level text rules: UTF-8 without BOM, LF, no trailing whitespace
├── .prettierignore                 # keeps Prettier away from SKILL.md
├── .gitattributes                  # force LF
├── .gitignore
├── .githooks/pre-commit            # optional pre-commit check
├── .github/workflows/validate.yml  # CI check (server-side backstop)
└── scripts/check_skill.py          # the checker itself
```

**Why a single standard file**: everything platform-specific was turned into a *slot* that the user fills in. Platform evidence never enters the standard, so it stays a single portable file.

---

## Three steps to use it

1. **Install** — copy the `deliverable-acceptance/` directory into your agent's skill directory (see the table below).
2. **Fill in** — complete the **twelve slots** in `SKILL.md` §6 for your platform. The same standard is filled in differently per platform; that is the design, not a defect.
3. **Run** — assemble a **work order** (deliverable location, capability requirement list, size limit, budget limit), then run L1→L2→L3 (free of model cost) and decide whether to authorize L4.

> **Unfilled slots make the standard unusable** — any criterion depending on an unfilled slot is recorded as `error`, and **guessing is forbidden**. That is the price of staying platform-neutral, and it is also why this standard does not lie to you.

---

## Per-agent setup

### Where skills live

| Agent | Project level | User level | Notes | Source |
|---|---|---|---|---|
| **Claude Code** | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` | Also nested directories, `<plugin>/skills/`, enterprise-managed dirs; **reserved names** `synced`, `anthropic-skills` | ✅ [official docs](https://code.claude.com/docs/en/skills) |
| **Codex** | `.agents/skills/<name>/` (walking up to the repo root) | `~/.agents/skills/<name>/` | Also ADMIN scope `/etc/codex/skills` and SYSTEM built-ins; **duplicate names are not merged** — both appear in the picker | ⚠️ third-party verification (official site returned 403); older references also mention `.codex/skills/` and `~/.codex/skills/` — **both claims are live, test on your installed version** |
| **WorkBuddy (Tencent)** | not verified | `~/.workbuddy/skills/<name>/SKILL.md` | Layout: `SKILL.md` + `references/` + `scripts/` + `assets/`; invoke with `@skill:<name>` or `/skills`; has a skill marketplace (SkillHub) | ⚠️ third-party (Tencent Cloud community article) + corroborated by a real-world WorkBuddy skill repository (its local dir is a junction to `~/.workbuddy/skills`) |
| **Cursor** | `.cursor/skills/`, `.agents/skills/` | `~/.cursor/skills/`, `~/.agents/skills/` | Supports **recursive subdirectories** (group by category); for compatibility it also reads `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, `~/.codex/skills/` | ✅ [official docs](https://cursor.com/docs/skills) |
| **Gemini CLI** | `.gemini/skills/<name>/` | see official docs | Has a `skill-creator` meta-skill and a discovery-tier/alias mechanism; note: official announcement says free-tier / Google One users moved to Antigravity CLI on 2026-06-18 | ✅ [official docs](https://geminicli.com/docs/cli/creating-skills/) |
| **OpenCode** | `.opencode/skills/<name>/SKILL.md`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | Has an explicit frontmatter **field allowlist** (unknown fields ignored); `permission.skill` in `opencode.json` allows/denies/asks by wildcard | ✅ [official docs](https://opencode.ai/docs/en/skills/) |

**Two practical notes:**

1. **For multi-platform setups, pick one directory.** Cursor reads `.claude/skills/`, `.codex/skills/` and `.agents/skills/`; OpenCode also reads `.claude/skills/` and `.agents/skills/`. Putting skills in **`.agents/skills/`** often gets you several agents at once — but **do not assume it**; confirm per agent with the negative controls below.
2. **Duplicate-name handling differs.** Codex explicitly keeps both and does **not** merge; Claude Code has a full precedence table (enterprise > personal > project, project skills override same-named bundled skills). That is exactly why **L1-11** emits a `warn`: a duplicate is not necessarily harmful, but somebody must know which copy wins.

---

### Slot values per platform

Legend: ✅ verifiable in official docs ｜ ⚠️ third-party source only ｜ ❓ not verified — run the §6 procedure yourself

#### A. Capability unit directories and declarations

| Slot | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **3 Unit directories** | `.claude/skills/`, `~/.claude/skills/`, `<plugin>/skills/` | `.agents/skills/`, `~/.agents/skills/`, `/etc/codex/skills` ⚠️ | `~/.workbuddy/skills/` ⚠️ | `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`, `~/.agents/skills/` ✅ | `.gemini/skills/` ✅ | `.opencode/skills/`, `~/.config/opencode/skills/`, `.claude/skills/`, `.agents/skills/` ✅ |
| **Entry file name** | `SKILL.md` ✅ | `SKILL.md` ⚠️ | `SKILL.md` ⚠️ | `SKILL.md` ✅ | `SKILL.md` ✅ | `SKILL.md` (all caps required) ✅ |
| **Optional resource dirs** | `scripts/`, `references/`, `assets/` (custom allowed) | `scripts/`, `references/`, `assets/` + `agents/openai.yaml` ⚠️ | `references/`, `scripts/`, `assets/` ⚠️ | `scripts/`, `references/`, `assets/` ✅ | `scripts/`, `references/`, `assets/` ✅ | unconstrained ✅ |
| **Multiple sources / precedence** | enterprise > personal > project; project skill overrides same-named bundled skill ✅ | duplicates **kept, not merged** ⚠️ | ❓ | ❓ (nested same-name behaviour unverified) | has a "discovery tiers + aliases" mechanism; see official docs ✅ | names must be **unique across all locations** (per troubleshooting guide) ✅ |

#### B. Identifier and metadata rules (L3-01 / L3-02 / L3-05)

| Slot | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **6 Identifier rules** | no charset regex published; `name` becomes the `/` command name ✅ | ❓ | ❓ | ❓ | ❓ | **`^[a-z0-9]+(-[a-z0-9]+)*$`**, 1–64 chars, no leading/trailing `-`, no consecutive `--` ✅ |
| **Required metadata** | docs state **all fields optional**; only `description` is recommended (falls back to first non-empty body line) ✅ | **`name` + `description` required** ⚠️ | `name`, `description` (`agent_created` optional) ⚠️ | `name` + `description` ✅ | `name` + `description` ✅ | **`name` + `description` required**; `license`/`compatibility`/`metadata` optional; **unknown fields ignored** ✅ |
| **Must name equal directory name?** | not enforced per docs (`name` defaults to the directory name) ✅ | ❓ | ❓ | ❓ | ❓ | **enforced** — "Match the directory name that contains `SKILL.md`" ✅ |
| **`description` limit** | combined `description` + `when_to_use` truncated at **1,536 chars** in the skill list ✅ | ❓ | ❓ | ❓ | ❓ | **1,024 chars** ✅ |
| **Platform extension fields** (non-blocking tier in L3-05) | `when_to_use` (note: **underscore**), `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `argument-hint`, `arguments`, `model`, `effort`, `context: fork`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` ✅ | `agents/openai.yaml` (icon, brand colour, `policy.allow_implicit_invocation`) ⚠️ | `agent_created` ⚠️ | ❓ | ❓ | only `name`/`description`/`license`/`compatibility`/`metadata` ✅ |

> **Important divergence — it changes L3-01's "what happens on failure" column.**
> **OpenCode** silently ignores fields outside its allowlist. **Claude Code** explicitly documents that when the frontmatter YAML fails to parse, **the skill body still loads but the metadata is empty** — the skill does not disappear, it simply never matches.
> That is a **completely different failure mode** from "the whole skill is silently dropped". So the failure description in L3-01 **must be rewritten after you test it on your actual platform** — never copied.

#### C. Verification and smoke-testing means (slot 5 real parser, L4-02, L4-03)

| Slot | Claude Code | Codex | WorkBuddy | Cursor | Gemini CLI | OpenCode |
|---|---|---|---|---|---|---|
| **5 Real parser / validation command** | `claude plugin validate <skills dir>` (v2.1.233+); `--debug` shows parse errors ✅ | ❓ (the built-in `$skill-creator` validates) ⚠️ | `@skill:skill-creator` ⚠️ | built-in `/create-skill` ✅ | built-in `skill-creator` ✅ | ❓ |
| **9 Isolated instance / smoke** | Use `--add-dir` to load a skills directory without touching the project ✅ | ❓ | ❓ | Cloud Agents **do not** read unsynced user-level skills ✅ (useful to prove "project-level only") | ❓ | ❓ |
| **10 Runtime visibility** | `What skills are available?`, `/skills`, `/context`, `/skill-doctor`; `--debug` logs ✅ | `/skills`, type `$`; **skill changes require a restart** ⚠️ | `/skills` ⚠️ | `/` menu search by skill name; some builds expose the skill list ⚠️ | see the official "discovery tiers" docs ✅ | the `skill` tool's `<available_skills>` XML ✅ |
| **12 Front-end extension fields** | N/A (skills have no UI half) | N/A | N/A | N/A | N/A | N/A |

> **L4-01 (capability-plane probe) and L4-04 (behavioural with/without)** have ready-made handles:
> Claude Code ships `claude plugin eval`, which runs each prompt in an isolated session **with and without the plugin**, scores it, and **exits non-zero below a threshold** so you can gate CI — plus the `skill-creator` plugin's `evals/evals.json` loop. That is exactly the "with / without comparison" L4-04 asks for. See the "evaluate and iterate" section of the [official docs](https://code.claude.com/docs/en/skills).

---

### Remaining slots

Slots 1 (deliverable shape), 2 (root anchor and required components), 10 (link scan scope) and 11 (forbidden declarations) are strongly tied to *the deliverable you are accepting* and only weakly to the agent platform, so **no universal value exists**. Example fill-in (abstract, not any real product):

```yaml
# excerpt from your adaptation table
slot1_deliverable: "a self-contained directory: 1 entry executable + runtime/ base + extensions/"
slot2_anchor: "env var APP_HOME; package root = $APP_HOME/..; never hardcode a drive letter"
slot10_link_scope: ["runtime/profiles", "runtime/home"]   # scan only these two subtrees
slot11_forbidden: ["shell-exec", "background-jobs", "network-egress"]
```

---

## Negative controls: prove your slot values are real

§6 of the standard requires it: **a slot without a negative control makes its criteria `error`.**
Build **deliberately broken** samples and confirm the platform actually rejects them — otherwise your rule is "what the docs say", not "what actually happens".

Four universal broken samples (revert after each):

| # | Broken sample | Expected failure |
|---|---|---|
| 1 | Insert a **UTF-8 BOM** at the file start | First line is no longer `---` → frontmatter not recognised (OpenCode and Claude Code both stress "the opening `---` must be the first line") |
| 2 | Make `name` **uppercase** or add an underscore | Depends on the platform's charset rule (OpenCode rejects it explicitly) |
| 3 | Make `name` **differ from the directory name** | OpenCode rejects it; other platforms may accept — **this divergence is precisely what you are measuring** |
| 4 | **Delete `description`** | Required-field platforms refuse to load; optional-field platforms (Claude Code) fall back to the first body line |

Run all four per platform and record the outcome in your adaptation table. **Consistency check**: if the same broken sample behaves differently across platforms, either your "target platform" is defined too broadly, or you actually need two adaptation tables.

---

## Pre-release checklist

- [ ] All twelve slots filled, or explicitly marked `not verified` (their criteria must be `error`)
- [ ] Every slot has had at least one **negative control**, with the observed failure recorded
- [ ] Work order complete: deliverable location, capability requirement list, size limit, budget limit, smoke authorization
- [ ] Report lists `not applicable` / `not executed` / `cannot execute` **separately**
- [ ] Every report item has a **measured value + threshold** (missing ones count as "not checked")
- [ ] Everything unmeasured appears in the **not-done list**, never mixed into the passes
- [ ] Exemptions are itemised with reason and blast radius, and were **re-measured this run** (no inherited exemptions)

---

## Known limitations (full list in §5 of the standard)

1. **Platform knowledge is not in the standard** — a mis-filled slot is invisible to the standard itself. Mitigation: negative controls plus a second person reviewing the slot table.
2. **L3 must be re-verified after a platform upgrade** — L3 is bound to the platform's loader implementation, so a platform change can turn "judged correctly" into **silently judging wrong**.
3. **Behavioural results are narrow** — L4-04's outcome cannot be extrapolated into "this agent can do the job".
4. **Visuals and aesthetics are not judged** — only "does it install".
5. **Target-machine environment differences** are out of reach (paths, permissions, antivirus, ports).

---

## Repository validation: keeping the skill from being "formatted" to death

The artifact of this repository is a **skill**, and the most fragile part of a skill is the top of `SKILL.md`: the first line of the frontmatter must be exactly `---`.
A Markdown formatter once rewrote it, escaping the delimiters to `\---` and padding the line endings with spaces. **Every file-level check still passed, but the skill could no longer load** -- the platform just logs one warning and ignores the file. That is the hardest class of defect to diagnose, so the repository carries four layers of protection:

| Protection | Level | What it does |
|---|---|---|
| `.editorconfig` | editor | forces UTF-8 without BOM, LF, trimmed trailing whitespace, final newline |
| `.prettierignore` | tooling | keeps Prettier away from `SKILL.md` |
| `scripts/check_skill.py` | script | BOM / CRLF / trailing whitespace / first line exactly `---` / frontmatter closed and actually parsed / `\---` escaping / `name` charset / `name` equals the directory name / README and LICENSE present |
| `.github/workflows/validate.yml` | server-side | runs that script on every push and pull request -- cloners need to configure nothing |

Run it locally:

```bash
python scripts/check_skill.py
```

To have it run before every commit (**once per clone**):

```bash
git config core.hooksPath .githooks
```

> **Contributors:** do not run a Markdown formatter (or an editor's format-on-save) over `SKILL.md`. Its top is **machine-read YAML frontmatter**, not human-facing layout. The checker catches this class of change, but catching it before a commit is cheaper than catching it in CI.

---

## License

This repository is released under the **[MIT License](LICENSE.md)**.

The license text is taken verbatim from the SPDX license registry (`licenseId: MIT`, `isOsiApproved: true`); only the copyright line is filled in by the author.

**MIT is an OSI-approved open-source license.** Anyone may use, modify, distribute, sublicense and **sell** the software; the only obligation is to **keep the copyright notice and the license text** in copies or substantial portions. GitHub detects it and labels the repository as MIT (open source).

**Attribution (must be handled before pushing):** MIT requires a copyright line in the form `Copyright (c) <year> <holder>`. The file currently holds a placeholder:

```
Copyright (c) 2026 <COPYRIGHT HOLDER>
```

> The placeholder was deliberately left for the author to fill in. The commit step refuses to run while it is still present.

**Publishing checklist**

- The standard contains **no platform- or product-private conventions** (verified by a coupling scan).
- If you also keep a specialised version bound to a specific platform or product, **do not publish it alongside** — such files usually contain directory contracts, internal paths and implementation details.
- Third-party product docs are referenced **factually and summarised**; no document body was copied. Keep it that way: **cite, don't copy.**

### Sources and credits

| Source | Used for |
|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | capability unit format, progressive-disclosure budget |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | quality dimension naming (names only) |
| τ-bench ([paper](https://arxiv.org/html/2406.12045v1)) | `pass^k` reliability metric |
| SkillsBench | with/without comparison + running the oracle first to prove the checker |
| [MCP Conformance](https://github.com/modelcontextprotocol/conformance) | frozen requirement sets, per-check exemptions, `not_scored` triage, stale-exemption detection |
| [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) | supply-chain field structure (**structure only, no text copied**; that document is CC BY-SA 4.0 and share-alike) |

Platform facts are sourced in the "Source" column of each table above. **Verification date: 2026-09-29.**

---

## Changing this standard

- Bump the version when criteria change (see "about this version" at the end of `SKILL.md`) and record the **driving reason** at the change site — future reviewers need to know why each criterion exists so they do not loosen it casually.
- Adding a platform only touches the tables in this README plus one slot table for that platform; **`SKILL.md` does not change** (that is what the slot design is for).
