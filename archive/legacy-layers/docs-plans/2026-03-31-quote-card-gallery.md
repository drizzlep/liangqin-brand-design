# Quote Card Gallery Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a visual gallery section to the quote-card documentation page so users can immediately see what different quote-card outputs look like.

**Architecture:** Keep the existing `quote-card-detail.html` page shell and static-site flow, then insert a new examples section built from static HTML preview cards plus scoped CSS in the shared `styles.css`. Reuse the current typography, surface, and spacing language instead of creating a separate microsite.

**Tech Stack:** Static HTML, shared CSS, Python unittest smoke tests

---

### Task 1: Add quote-card examples section to the detail page

**Files:**
- Modify: `quote-card-detail.html`
- Test: `tests/test_quote_card_detail_page.py`

**Step 1: Write the failing test**

Add assertions for:
- `案例预览`
- `正式单品报价卡`
- `儿童房组合报价卡`
- `多品汇总报价卡`

**Step 2: Run test to verify it fails**

Run: `python3 tests/test_quote_card_detail_page.py`
Expected: FAIL because the examples section does not exist yet.

**Step 3: Write minimal implementation**

Update `quote-card-detail.html` to:
- add `#examples` to the page navigation
- insert a new section after the hero
- add three static preview cards with concise labels and supporting copy

**Step 4: Run test to verify it passes**

Run: `python3 tests/test_quote_card_detail_page.py`
Expected: PASS

### Task 2: Add dedicated preview-card styling

**Files:**
- Modify: `styles.css`

**Step 1: Write minimal styling plan**

Create scoped classes for:
- preview grid
- preview card shell
- mini quote-card frame
- label, amount, rows, footer hints

**Step 2: Write minimal implementation**

Add new CSS near the existing product/case detail page styles so the quote previews:
- feel brand-aligned
- are clearly different example types
- read well on desktop and mobile

**Step 3: Verify visually by reading the HTML/CSS**

Run: `rg -n "quote-preview" quote-card-detail.html styles.css`
Expected: all new classes are present in both files.

### Task 3: Validate and keep the static site stable

**Files:**
- Verify: `tests/test_index_manual_homepage.py`
- Verify: `tests/test_quote_card_detail_page.py`
- Verify: `tests/test_liangqin_brand_skill_distribution.py`

**Step 1: Run homepage smoke test**

Run: `python3 tests/test_index_manual_homepage.py`
Expected: PASS

**Step 2: Run quote-card detail smoke test**

Run: `python3 tests/test_quote_card_detail_page.py`
Expected: PASS

**Step 3: Run skill distribution smoke test**

Run: `python3 tests/test_liangqin_brand_skill_distribution.py`
Expected: PASS
