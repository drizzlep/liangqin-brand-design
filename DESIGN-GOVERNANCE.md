# DESIGN Governance

> Generated from `miten-foundation-dna-zh-cn-v2` (`v2.0.0`) as the agent-facing control protocol for Liangqin Ji Mu design inputs.

## Protocol

- Truth: `foundation-dna/design-dna.zh-CN.json`
- Default input: `DESIGN.md`
- Neutral token export: `foundation-dna/tokens.semantic.json`
- Read `design-packs/*.json` only when style variation is needed
- Read `artifact-surfaces/*.json` only when a concrete artifact is needed
- Read `examples / real cases` only for acceptance or calibration
- Run the delivery gates in order: Context → Surface → Variation → Material → Runtime → Verification → Handoff
- Categories change content facts and emphasis only; they must not redefine brand style
- Channels change delivery constraints and density only; they must not become style switches
- `skills/public/liangqin-brand-openclaw/` is an adapter that consumes this standard; it is not the source of truth

## Delivery Gates

- Context Gate: confirm the brief, product facts, reference material, design assets and target fidelity before choosing an output level.
- Surface Gate: identify the delivery surface before layout; do not turn decks, quote cards, H5 flows, motion artifacts or design canvases into generic web pages.
- Variation Gate: use `design-packs/` as controlled tweaks only; expose options when exploration is requested, not as uncontrolled style drift.
- Material Gate: if logo, imagery, icon, quote or product facts are missing, degrade to structured spec, placeholder or a missing-input list instead of faking finish.
- Runtime Gate: follow the selected artifact surface's canvas, interaction and export contract when the output must open, scale, print, present or be shared.
- Verification Gate: check structure, runtime behavior, brand fit and final delivery format before treating the artifact as ready.
- Handoff Gate: state whether the output is a spec, prototype, visual draft, final artifact or blocked pending assets.

## Conflict Resolution

`Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`

## Change Map

- Change Foundation DNA to alter brand rules or core tokens
- Change `DESIGN.md` to alter AI-facing design language
- Change `design-packs/` to open controlled variation without replacing the brand constitution
- Change `artifact-surfaces/` to validate concrete deliverables and delivery constraints, not redefine brand aesthetics
- Change `skills/public/liangqin-brand-openclaw/` only to adapt this package for OpenClaw consumption
- Change `evaluation/` to record delivery failures, AI slop, data slop, context gaps and regression questions
