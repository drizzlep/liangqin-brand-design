# Index Homepage Elegance Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the style guide homepage into a more elegant, editorial brand entry while preserving information clarity and adding a three-state theme switcher.

**Architecture:** Keep the existing static HTML structure and JavaScript boot flow, but reorganize the homepage content into clearer visual tiers and extend the stylesheet with a homepage-specific surface hierarchy plus light/dark/system theme variables. Add a small client-side theme controller in the existing `app.js` so the switcher works without introducing new tooling.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, Vercel static hosting

---

### Task 1: Restructure the homepage hero and key content hierarchy

**Files:**
- Modify: `index.html`

**Step 1: Update the overview section to a two-column editorial intro**

- Replace the current uniform overview cards with:
  - a left editorial introduction block
  - a right high-priority system-entry block
  - a smaller supporting principles block

**Step 2: Reduce repeated “equal-weight card” layouts in key homepage sections**

- Rework selected homepage sections so they read as:
  - major exhibit
  - supporting guidance
  - lighter reference content

**Step 3: Add homepage theme switcher markup**

- Insert a three-state control near the homepage sidebar or editorial hero
- States:
  - `system`
  - `light`
  - `dark`

**Step 4: Review section ids and navigation compatibility**

- Ensure all updated homepage sections still match existing scroll-spy links

### Task 2: Build a homepage-specific visual hierarchy system

**Files:**
- Modify: `styles.css`

**Step 1: Add homepage-specific theme tokens**

- Define homepage variables for:
  - background layers
  - editorial panel
  - exhibit panel
  - reference panel
  - borders
  - text tones

**Step 2: Redesign the homepage hero and editorial intro layout**

- Create stronger typographic hierarchy
- Increase asymmetry and breathing room
- Make entry surfaces feel like curated system gateways rather than standard cards

**Step 3: Differentiate panel weights**

- Create separate styling for:
  - editorial panels
  - exhibit surfaces
  - reference grids

**Step 4: Reduce average-card feeling across homepage sections**

- Rebalance grid ratios
- Use larger primary blocks and lighter secondary blocks
- Lower the appendix visual weight

**Step 5: Add responsive behavior for the new hierarchy**

- Ensure the homepage remains intentional on tablet and mobile
- Preserve section rhythm after stacking

### Task 3: Add theme switching behavior to the existing JavaScript boot flow

**Files:**
- Modify: `app.js`

**Step 1: Add theme preference constants and helpers**

- Support stored values:
  - `system`
  - `light`
  - `dark`

**Step 2: Apply theme mode to the document root**

- Use a stable attribute such as `data-theme`
- Fall back to system when there is no explicit user choice

**Step 3: Wire the homepage switcher controls**

- Clicking a theme option updates:
  - stored preference
  - active button state
  - current document theme

**Step 4: Keep system mode reactive**

- When the OS theme changes and the saved mode is `system`, update the page automatically

### Task 4: Verify homepage behavior and theme states

**Files:**
- Verify: `index.html`
- Verify: `styles.css`
- Verify: `app.js`

**Step 1: Run a fast static smoke check**

Run: `python3 -m http.server 4173`
Expected: local static server starts successfully

**Step 2: Verify markup loads without console-breaking script issues**

Run: open the homepage in a browser or a quick HTTP fetch
Expected: page returns 200 and includes new homepage hero structure

**Step 3: Verify theme switcher states**

- Confirm `system`, `light`, `dark` all render
- Confirm explicit choice persists across reloads

**Step 4: Verify responsive rhythm**

- Confirm the new homepage layout still reads clearly on narrower widths

**Step 5: Review resulting file diffs**

Run: `git diff -- index.html styles.css app.js`
Expected: focused homepage-only changes plus theme logic
