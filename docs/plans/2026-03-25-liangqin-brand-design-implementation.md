# Liangqin Brand Design Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a standalone OpenClaw-installable Liangqin brand design skill repository with reusable references, packaging scripts, and install docs.

**Architecture:** Create a repo-level delivery shell around a publishable skill directory. Keep `SKILL.md` lightweight, move reusable design knowledge into `references/`, and use small Python/Zsh utilities to publish into OpenClaw skill stores and generate distributable artifacts.

**Tech Stack:** Markdown, Python 3 standard library, zsh, zip/base64 packaging

---

### Task 1: Create repository skeleton

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `docs/plans/2026-03-25-liangqin-brand-design-skill-design.md`
- Create: `docs/plans/2026-03-25-liangqin-brand-design-implementation.md`

**Step 1: Write the repository docs and ignore rules**
Create the repo-level overview, install guidance, and ignore rules.

**Step 2: Verify the files exist**
Run: `find . -maxdepth 3 -type f | sort`
Expected: repo docs and plan files are listed.

### Task 2: Create the skill payload

**Files:**
- Create: `skill/liangqin-brand-design/SKILL.md`
- Create: `skill/liangqin-brand-design/README.md`
- Create: `skill/liangqin-brand-design/references/brand-dna.md`
- Create: `skill/liangqin-brand-design/references/execution-rules.md`
- Create: `skill/liangqin-brand-design/references/review-checklist.md`
- Create: `skill/liangqin-brand-design/references/anti-patterns.md`
- Create: `skill/liangqin-brand-design/references/page-and-poster-patterns.md`

**Step 1: Write the light SKILL entrypoint**
Keep triggers and routing in `SKILL.md`, and move depth into references.

**Step 2: Write the reference files**
Encode brand DNA, execution rules, review checklist, anti-patterns, and common layout patterns.

**Step 3: Verify the frontmatter and references**
Run: `python3 skill/liangqin-brand-design/scripts/publish_skill.py --source skill/liangqin-brand-design --dest /tmp/liangqin-brand-design-test --workspace-dest /tmp/liangqin-brand-design-workspace`
Expected: both destinations publish successfully.

### Task 3: Add delivery scripts and docs

**Files:**
- Create: `skill/liangqin-brand-design/scripts/publish_skill.py`
- Create: `skill/liangqin-brand-design/scripts/refresh_and_test.py`
- Create: `scripts/package_openclaw_skill.sh`
- Create: `scripts/build_single_file_installer.sh`
- Create: `docs/openclaw-skill-local-install.md`
- Create: `docs/openclaw-single-file-installer.md`

**Step 1: Implement publish and smoke-test helpers**
Use Python stdlib only; validate frontmatter and mirror the skill into OpenClaw destinations.

**Step 2: Implement packaging scripts**
Build a zip and a single-file installer from the skill payload.

**Step 3: Verify packaging commands**
Run: `bash scripts/package_openclaw_skill.sh` and `bash scripts/build_single_file_installer.sh`
Expected: `dist/` contains a zip and an installer script.

### Task 4: Run final verification

**Files:**
- Modify: `README.md` if verification exposes mismatches

**Step 1: Run lightweight verification**
Run:
- `python3 skill/liangqin-brand-design/scripts/publish_skill.py --source skill/liangqin-brand-design --dest /tmp/liangqin-brand-design-test --workspace-dest /tmp/liangqin-brand-design-workspace`
- `bash scripts/package_openclaw_skill.sh`
- `bash scripts/build_single_file_installer.sh`

**Step 2: Inspect the generated installer help path by reading the script header**
Run: `sed -n '1,220p' dist/liangqin-brand-design-installer-$(date +%Y%m%d).sh`
Expected: install destination, sync logic, and optional smoke test are present.

**Step 3: Commit**
```bash
git add .
git commit -m "feat: add liangqin brand design skill repo"
```
