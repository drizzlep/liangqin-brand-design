# Single DESIGN.md Governance Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor the brand-governance assets so every generated output, regardless of category or channel, is controlled first by a single `DESIGN.md`, with channels only affecting delivery constraints instead of brand style.

**Architecture:** Keep `foundation-dna/` as the truth source, strengthen `DESIGN.md` into the default brand constitution, add a model-facing execution checklist, and update the OpenClaw skill plus manual rubric so generation and review both enforce the same non-negotiable rules. Do not add new channel-specific design packs as the primary control layer.

**Tech Stack:** Markdown governance docs, JSON/Markdown skill assets, existing Python validation scripts, unittest-based repo checks

---

### Task 1: Rewrite `DESIGN.md` as the primary brand constitution

**Files:**
- Modify: `DESIGN.md`
- Reference: `foundation-dna/design-dna.zh-CN.json`
- Reference: `DESIGN-GOVERNANCE.md`

**Step 1: Reorder `DESIGN.md` so hard rules appear before visual detail**

- Move the non-negotiable brand rules to the top of the document.
- Introduce a short “brand constitution” section that states:
  - all outputs must remain warm, restrained, trustworthy
  - channels do not define style
  - categories do not redefine brand expression

**Step 2: Add an explicit “不可协商规则” section**

- Include:
  - brand tone
  - Chinese-first readability
  - CTA voice
  - photography/material-first priority
  - prohibition against promo/e-commerce drift

**Step 3: Promote iconography from buried token detail to primary rule**

- Bring the icon constraints into the main body:
  - thin geometric outline
  - restrained endpoints
  - consistent stroke weight
  - degrade to fewer/no icons when fidelity cannot be guaranteed

**Step 4: Add an explicit “允许变化范围” section**

- Clarify that allowed variation is limited to:
  - density
  - section order within bounds
  - content emphasis
  - delivery compression
- Clarify that it does not include switching the brand style itself.

**Step 5: Add a generator-facing reminder section**

- Include short prompts such as:
  - “先保品牌，再做适配”
  - “先像成品，再像规范”
  - “如图标工艺无法保证，优先降级而不是乱生成”

### Task 2: Tighten governance so supplementary assets cannot rewrite the brand

**Files:**
- Modify: `DESIGN-GOVERNANCE.md`
- Reference: `README.md`

**Step 1: Narrow the governance document to reading order and conflict resolution**

- Keep only:
  - truth source
  - default control surface
  - allowed supplementary layers
  - conflict resolution

**Step 2: Add explicit statements for category/channel handling**

- State that:
  - channels define delivery constraints only
  - categories define content facts only
  - neither may override brand constitution

**Step 3: Clarify the role of `artifact-surfaces/`**

- Update language so artifact surfaces are described as:
  - delivery validation references
  - not aesthetic control sources

### Task 3: Add a generator execution checklist

**Files:**
- Create: `EXECUTION-CHECKLIST.md`
- Reference: `DESIGN.md`
- Reference: `skills/public/liangqin-brand-openclaw/protocols/brand-boundaries.zh-CN.json`

**Step 1: Add pre-generation checks**

- Questions should include:
  - Have I read `DESIGN.md` first?
  - Am I treating this as a brand task rather than a style exploration?
  - Am I missing product facts and trying to compensate with decorative output?

**Step 2: Add in-generation checks**

- Questions should include:
  - Does this still look like 良禽佳木?
  - Is Chinese readability still primary?
  - Have I introduced system-facing English labels or meta copy?
  - Are icons helping clarity or becoming low-quality decoration?

**Step 3: Add post-generation checks**

- Questions should include:
  - Does this look like a publishable artifact?
  - Are `Pack`, `Page Goal`, `Design Preview`, or similar terms leaking into the output?
  - If the images disappear, do structure and language still hold?

### Task 4: Update the OpenClaw skill to enforce the new governance flow

**Files:**
- Modify: `skills/public/liangqin-brand-openclaw/SKILL.md`
- Modify: `skills/public/liangqin-brand-openclaw/README.md`

**Step 1: Update the skill positioning**

- Emphasize that the skill is a brand-governance executor, not a style router.

**Step 2: Replace loose reading guidance with a mandatory execution order**

- Required order:
  - read `DESIGN.md`
  - read boundary protocol
  - read module recipes
  - generate
  - self-check with `EXECUTION-CHECKLIST.md`

**Step 3: Add explicit fallback behavior**

- If a channel cannot support refined icon/detail fidelity:
  - reduce complexity
  - simplify hierarchy
  - reduce icon usage
  - never invent a new style family

### Task 5: Update manual review to catch the current failure modes

**Files:**
- Modify: `skills/public/liangqin-brand-openclaw/evaluation/manual-rubric.zh-CN.md`
- Reference: `skills/public/liangqin-brand-openclaw/evaluation/human-review-protocol.zh-CN.md`

**Step 1: Add “成品感” checks**

- Require reviewers to confirm the output feels like a deliverable, not a system card or spec sheet.

**Step 2: Add “元信息泄漏” checks**

- Explicitly fail outputs containing internal terms such as:
  - Pack
  - Page Goal
  - Preview
  - Design system explanation copy

**Step 3: Add “图标工艺” and “中文一致性” checks**

- Review whether:
  - icon style is unified and restrained
  - icon fidelity is high enough to keep
  - Chinese UI remains complete and natural

### Task 6: Validate the document and skill changes

**Files:**
- Verify: `DESIGN.md`
- Verify: `DESIGN-GOVERNANCE.md`
- Verify: `EXECUTION-CHECKLIST.md`
- Verify: `skills/public/liangqin-brand-openclaw/SKILL.md`
- Verify: `skills/public/liangqin-brand-openclaw/evaluation/manual-rubric.zh-CN.md`

**Step 1: Run the repo validation script**

Run: `python3 skills/public/liangqin-brand-openclaw/scripts/validate_skill_assets.py`
Expected: no missing required sections or skill-asset errors

**Step 2: Run the focused tests that exercise design/export assumptions**

Run: `python3 -m unittest tests/test_liangqin_brand_skill_assets.py tests/test_design_md_adapter.py -v`
Expected: PASS for all relevant governance and export checks

**Step 3: Review the diff for scope discipline**

Run: `git diff -- DESIGN.md DESIGN-GOVERNANCE.md EXECUTION-CHECKLIST.md skills/public/liangqin-brand-openclaw/SKILL.md skills/public/liangqin-brand-openclaw/README.md skills/public/liangqin-brand-openclaw/evaluation/manual-rubric.zh-CN.md`
Expected: focused governance-only edits with no unrelated visual/output churn

### Task 7: Optional follow-up after governance is stable

**Files:**
- Optional future work only

**Step 1: Audit artifact surfaces against the new rules**

- Remove or isolate system-facing explanatory copy from artifact outputs.

**Step 2: Decide whether a fixed icon asset library is needed**

- If generation still degrades icon quality, provide a controlled SVG source instead of allowing free icon invention.

**Step 3: Re-test a previously weak channel**

- Re-run a DingTalk-style single-image output after governance changes and compare against the updated rubric.
