#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
DNA_PATH = ROOT / "foundation-dna" / "design-dna.zh-CN.json"
PACKS_DIR = ROOT / "design-packs"
ARTIFACT_SURFACES_DIR = ROOT / "artifact-surfaces"

PACK_REQUIRED_FIELDS = [
    "slug",
    "sort_order",
    "title",
    "summary",
    "preview_variant",
    "mood",
    "density",
    "imagery",
    "cta_tone",
    "zh_readability",
    "best_for_pages",
    "derived_from",
    "governance_role",
    "layout_focus",
    "component_focus",
    "recommended_modules",
    "notes",
    "variation_scope",
    "preview_tokens",
    "preview_content",
]

PACK_REQUIRED_TOKEN_FIELDS = [
    "background",
    "surface",
    "elevated",
    "accent",
    "line",
    "hero_glow",
    "panel_tint",
    "chip_tint",
]

PACK_REQUIRED_CONTENT_FIELDS = [
    "hero_title",
    "hero_lead",
    "hero_note",
    "primary_cta",
    "secondary_cta",
    "feature_label",
    "feature_body",
    "quote",
]

PACK_REQUIRED_MODULE_FIELDS = [
    "name",
    "purpose",
    "layout_hint",
]

ALLOWED_PACK_GOVERNANCE_ROLES = {
    "controlled_variation_layer",
}

ALLOWED_ARTIFACT_SURFACE_TYPES = {
    "web",
    "mobile_h5",
    "quote_card",
}

ARTIFACT_REQUIRED_FIELDS = [
    "slug",
    "title",
    "surface_type",
    "source_pack",
    "primary_use_case",
    "governance_role",
    "recommended_modules",
    "layout_rules",
    "failure_modes",
    "preview_content",
]

ARTIFACT_REQUIRED_CONTENT_FIELDS = [
    "eyebrow",
    "hero_title",
    "hero_lead",
    "page_goal",
    "primary_cta",
    "secondary_cta",
]

REQUIRED_QUOTE_SAMPLE_FIELDS = [
    "quote_type",
    "badge",
    "eyebrow",
    "product_name",
    "subtitle",
    "total_price",
    "tags",
    "scenario",
    "sections",
    "note",
]

REQUIRED_QUOTE_SECTION_FIELDS = [
    "label",
    "lines",
]

REQUIRED_QUOTE_LINE_FIELDS = [
    "label",
    "value",
]

ALLOWED_ARTIFACT_GOVERNANCE_ROLES = {
    "artifact_validation_layer",
}

FEATURED_PREVIEW_PACK_SLUGS = [
    "warm-gallery",
    "liangqin-apple",
    "consultation-trust",
    "product-spec-premium",
]


def generate_design_md(dna: dict) -> str:
    meta = dna["meta"]
    principles = dna["brand_principles"]
    design_system = dna["design_system"]
    design_style = dna["design_style"]
    effects = dna["visual_effects"]

    colors = design_system["color"]
    typography = design_system["typography"]
    type_scale = typography["type_scale"]
    spacing = design_system["spacing"]
    layout = design_system["layout"]
    shape = design_system["shape"]
    elevation = design_system["elevation"]
    motion = design_system["motion"]
    components = design_system["components"]
    responsive = design_system["responsive"]
    accessibility = design_system["accessibility"]

    prompt = dedent(
        """
        Build a Chinese premium home furnishing page for Liangqin Ji Mu.
        Use a calm, tactile, editorial visual language with generous whitespace,
        warm neutral surfaces, serif-led headlines, and restrained interactions.
        Keep copy polite and trustworthy. Prefer “查看 / 了解 / 预约 / 咨询”
        style CTAs. Avoid e-commerce promo styling, loud gradients, glassmorphism,
        particle effects, and experimental motion that harms readability.
        """
    ).strip()

    lines = [
        "# DESIGN.md: Liangqin Ji Mu",
        "",
        "> Source of truth: `foundation-dna/design-dna.zh-CN.json`",
        ">",
        f"> Generated from `{meta['name']}` (`v{meta['version']}`) as the default AI-facing design brief.",
        "",
        "## 1. Visual Theme & Atmosphere",
        "",
        f"良禽佳木的界面气质应围绕“{' / '.join(design_style['aesthetic']['adjectives'])}”展开。先建立信任与审美判断，再承接咨询或产品理解。锚点句：**{principles['anchor_sentence']}**",
        "",
        f"视觉隐喻：{design_style['aesthetic']['visual_metaphor']}",
        "",
        "品牌不可妥协项：",
        "- 中文优先，允许完整导航、按钮与标签表达",
        "- CTA 必须礼貌、稳妥、非强刺激推销口吻",
        "- 材质、摄影、留白和信息秩序优先于装饰性表现",
        "- 不能滑向电商促销页、通用 SaaS 模板或欧美极简冷感语气",
        "",
        "设计风格：",
        f"- Mood: {', '.join(design_style['aesthetic']['mood'])}",
        f"- Genre / Personality: {design_style['aesthetic']['genre']} / {', '.join(design_style['aesthetic']['personality_traits'])}",
        f"- Texture / Whitespace: {design_style['visual_language']['texture_usage']} / {design_style['visual_language']['whitespace_usage']}",
        "",
        "## 2. Color Palette & Roles",
        "",
        "### Primary",
        "",
        f"- **Primary Ink** (`{colors['primary']['hex']}`): {colors['primary']['role']}",
        f"- **Background** (`{colors['surface']['background']}`): 页面主背景",
        f"- **Surface** (`{colors['surface']['card']}`): 卡片 / 次级背景",
        f"- **Elevated Surface** (`{colors['surface']['elevated']}`): 浮层 / 强调区块",
        f"- **Accent** (`{colors['accent']['hex']}`): {colors['accent']['role']}",
        f"- **Brand Asset** (`{colors['brand_asset']['hex']}`): {colors['brand_asset']['role']}",
        "",
        "### Neutral Scale",
        "",
        "| Level | Value |",
        "|---|---|",
    ]
    for level, value in colors["neutral"]["scale"].items():
        lines.append(f"| {level} | `{value}` |")

    lines.extend(
        [
            "",
            "### Semantic",
            "",
        ]
    )
    for name, value in colors["semantic"].items():
        lines.append(f"- **{name.title()}** (`{value}`)")

    lines.extend(
        [
            "",
            "配色策略：",
            f"- Palette / Contrast: {colors['palette_type']} / {colors['contrast_strategy']}",
            f"- Accent / Neutral usage: {colors['accent_strategy']} / {colors['neutral']['usage']}",
            "",
            "## 3. Typography Rules",
            "",
            "字体策略：",
            f"- **Heading**: `{typography['font_families']['heading']}`",
            f"- **Body**: `{typography['font_families']['body']}`",
            f"- **Mono**: `{typography['font_families']['mono']}`",
            f"- Notes: {typography['font_style_notes']}",
            "",
            "| Role | Size | Weight | Line Height | Tracking | Font Family | Usage |",
            "|---|---:|---:|---:|---:|---|---|",
            f"| Display | {type_scale['display']['size']} | {type_scale['display']['weight']} | {type_scale['display']['line_height']} | {type_scale['display']['tracking']} | {typography['font_families']['heading']} | 首屏主标题 |",
            f"| Heading 1 | {type_scale['heading_1']['size']} | {type_scale['heading_1']['weight']} | {type_scale['heading_1']['line_height']} | {type_scale['heading_1']['tracking']} | {typography['font_families']['heading']} | 一级标题 |",
            f"| Heading 2 | {type_scale['heading_2']['size']} | {type_scale['heading_2']['weight']} | {type_scale['heading_2']['line_height']} | {type_scale['heading_2']['tracking']} | {typography['font_families']['heading']} | 二级标题 |",
            f"| Heading 3 | {type_scale['heading_3']['size']} | {type_scale['heading_3']['weight']} | {type_scale['heading_3']['line_height']} | {type_scale['heading_3']['tracking']} | {typography['font_families']['heading']} | 三级标题 |",
            f"| Body | {type_scale['body']['size']} | {type_scale['body']['weight']} | {type_scale['body']['line_height']} | {type_scale['body']['tracking']} | {typography['font_families']['body']} | 正文与摘要 |",
            f"| Body Small | {type_scale['body_small']['size']} | {type_scale['body_small']['weight']} | {type_scale['body_small']['line_height']} | {type_scale['body_small']['tracking']} | {typography['font_families']['body']} | 次正文与表单说明 |",
            f"| Caption | {type_scale['caption']['size']} | {type_scale['caption']['weight']} | {type_scale['caption']['line_height']} | {type_scale['caption']['tracking']} | {typography['font_families']['body']} | 注释与元信息 |",
            f"| Overline | {type_scale['overline']['size']} | {type_scale['overline']['weight']} | {type_scale['overline']['line_height']} | {type_scale['overline']['tracking']} | {typography['font_families']['body']} | 标签与分组标题 |",
            "",
            "中文排版默认规则：",
            f"- 标题：{typography['chinese_typesetting']['headline_rule']}",
            f"- 正文：{typography['chinese_typesetting']['body_rule']}",
            f"- 标签：{typography['chinese_typesetting']['label_rule']}",
            f"- 回退：{typography['chinese_typesetting']['fallback_rule']}",
            "",
            "## 4. Component Stylings",
            "",
            f"- **Buttons**: {components['button_style']}",
            f"- **Inputs**: {components['input_style']}",
            f"- **Cards**: {components['card_style']}",
            f"- **Navigation**: {components['navigation_pattern']}",
            f"- **Modal / Drawer**: {components['modal_style']}",
            f"- **Lists**: {components['list_style']}",
            f"- **Component rule**: {components['component_notes']}",
            "",
            "## 5. Layout Principles",
            "",
            f"- Base unit: `{spacing['base_unit']}`",
            f"- Spacing scale: `{', '.join(spacing['scale'])}`",
            f"- Section rhythm: {spacing['section_rhythm']}",
            f"- Grid: `{layout['grid_system']}`",
            f"- Max content width: `{layout['max_content_width']}`",
            f"- Columns: desktop `{layout['columns']['desktop']}` / tablet `{layout['columns']['tablet']}` / mobile `{layout['columns']['mobile']}`",
            f"- Gutters: desktop `{layout['gutter']['desktop']}` / tablet `{layout['gutter']['tablet']}` / mobile `{layout['gutter']['mobile']}`",
            f"- Alignment / Balance: {layout['alignment_tendency']} / {design_style['composition']['balance_type']}",
            f"- Negative space role: {design_style['composition']['negative_space_role']}",
            "",
            "Shape system：",
            f"- Radius: small `{shape['border_radius']['small']}` / medium `{shape['border_radius']['medium']}` / large `{shape['border_radius']['large']}` / pill `{shape['border_radius']['pill']}`",
            f"- Border / Divider: {shape['border_usage']} / {shape['divider_style']}",
            "",
            "## 6. Depth & Elevation",
            "",
            "| Level | Value | Usage |",
            "|---|---|---|",
            f"| Low | `{elevation['levels']['low']}` | 轻层级卡片与弱强调区 |",
            f"| Medium | `{elevation['levels']['medium']}` | 浮层与重点信息块 |",
            f"| High | `{elevation['levels']['high']}` | 强强调层与高优先级内容 |",
            "",
            "深度与动效规则：",
            f"- Shadow style: {elevation['shadow_style']}",
            f"- Depth cues: {elevation['depth_cues']}",
            f"- Easing: `{motion['easing']}`",
            f"- Duration scale: micro `{motion['duration_scale']['micro']}` / normal `{motion['duration_scale']['normal']}` / macro `{motion['duration_scale']['macro']}`",
            f"- Entrance: {motion['entrance_pattern']}",
            f"- Exit: {motion['exit_pattern']}",
            f"- Composite / Image / Background: {effects['composite_notes']} / {effects['image_effects']['description']} / {effects['background_effects']['description']}",
            "",
            "## 7. Do's and Don'ts",
            "",
            "### Do",
            "",
        ]
    )
    for item in principles["principles"]:
        lines.append(f"- {item['label']}：{item['description']}")
    lines.extend(
        [
            f"- {accessibility['target_size']}",
            f"- 所有动效遵守 `{motion['philosophy']}`，并支持 reduced motion 降级",
            "- 把摄影、材质、留白和结构层级放在所有视觉修饰之前",
            "",
            "### Don't",
            "",
        ]
    )
    for item in principles["avoid"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "- 不使用粒子系统、shader 扭曲、默认 3D 语言或自定义鼠标特效",
            "- 不为了“高级感”牺牲中文可读性、路径理解和表单说明",
            "- 不让 accent 长时间、大面积占据视觉中心",
            "",
            "## 8. Responsive Behavior",
            "",
            "| Breakpoint | Range / Strategy |",
            "|---|---|",
            f"| Mobile | `{layout['breakpoints']['mobile']}` / {responsive['mobile_strategy']} |",
            f"| Tablet | `{layout['breakpoints']['tablet']}` / {responsive['tablet_strategy']} |",
            f"| Desktop | `{layout['breakpoints']['desktop']}` / {responsive['desktop_strategy']} |",
            "",
            "响应式要求：",
            f"- Navigation: {responsive['navigation_behavior']}",
            f"- Section density: {responsive['section_density_rule']}",
            f"- Contrast / Focus visibility: {accessibility['contrast_policy']} / {accessibility['focus_visibility']}",
            f"- Motion safety / Content clarity: {accessibility['motion_safety']} / {accessibility['content_clarity']}",
            "",
            "## 9. Agent Prompt Guide",
            "",
            "Use this DESIGN.md to lock the non-negotiable brand feel before exploring layout or style variation.",
            "",
            "Prompt checklist:",
            "- 优先中文，导航、按钮、标签允许完整表达",
            "- 先用摄影、材质说明、留白和结构建立信任，再谈装饰",
            f"- CTA 语气使用 `{design_style['brand_voice_in_ui']['cta_style']}`，避免命令式压迫感",
            f"- 交互反馈保持 `{design_style['interaction_feel']['feedback_style']}`，hover 只做微弱变化",
            f"- 如果与品牌边界冲突，永远回到 `{DNA_PATH.relative_to(ROOT)}` 里的规则",
            "",
            "Suggested prompt:",
            "",
            "```text",
            prompt,
            "```",
        ]
    )

    return "\n".join(lines) + "\n"


def generate_design_governance_md(dna: dict) -> str:
    meta = dna["meta"]

    lines = [
        "# DESIGN Governance",
        "",
        f"> Generated from `{meta['name']}` (`v{meta['version']}`) as the agent-facing control protocol for Liangqin Ji Mu design inputs.",
        "",
        "## Protocol",
        "",
        "- Truth: `foundation-dna/design-dna.zh-CN.json`",
        "- Default input: `DESIGN.md`",
        "- Read `design-packs/*.json` only when style variation is needed",
        "- Read `artifact-surfaces/*.json` only when a concrete artifact is needed",
        "- Read `examples / real cases` only for acceptance or calibration",
        "",
        "## Conflict Resolution",
        "",
        "`Foundation DNA > DESIGN.md > artifact-surfaces > design-packs > examples`",
        "",
        "## Change Map",
        "",
        "- Change Foundation DNA to alter brand rules or core tokens",
        "- Change `DESIGN.md` to alter AI-facing design language",
        "- Change `design-packs/` to open controlled variation",
        "- Change `artifact-surfaces/` to validate concrete deliverables",
    ]

    return "\n".join(lines) + "\n"


def ordered_unique(values):
    seen = set()
    ordered = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def require_fields(payload: dict, required_fields, context: str) -> None:
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValueError(f"{context} missing fields: {', '.join(missing)}")


def ensure_non_empty_string(value, context: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string")


def ensure_string_list(values, context: str) -> None:
    if not isinstance(values, list) or not values:
        raise ValueError(f"{context} must be a non-empty list")
    for index, value in enumerate(values):
        ensure_non_empty_string(value, f"{context}[{index}]")


def ensure_module_list(values, context: str) -> None:
    if not isinstance(values, list) or len(values) < 3:
        raise ValueError(f"{context} must be a list with at least 3 modules")

    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise ValueError(f"{context}[{index}] must be an object")
        require_fields(value, PACK_REQUIRED_MODULE_FIELDS, f"{context}[{index}]")
        for field_name in PACK_REQUIRED_MODULE_FIELDS:
            ensure_non_empty_string(
                value[field_name],
                f"{context}[{index}].{field_name}",
            )


def ensure_quote_samples(values, context: str) -> None:
    if not isinstance(values, list) or len(values) < 3:
        raise ValueError(f"{context} must contain at least 3 quote samples")

    for sample_index, sample in enumerate(values):
        sample_context = f"{context}[{sample_index}]"
        if not isinstance(sample, dict):
            raise ValueError(f"{sample_context} must be an object")
        require_fields(sample, REQUIRED_QUOTE_SAMPLE_FIELDS, sample_context)

        for field_name in [
            "quote_type",
            "badge",
            "eyebrow",
            "product_name",
            "subtitle",
            "total_price",
            "scenario",
            "note",
        ]:
            ensure_non_empty_string(sample[field_name], f"{sample_context}.{field_name}")

        ensure_string_list(sample["tags"], f"{sample_context}.tags")

        sections = sample["sections"]
        if not isinstance(sections, list) or not sections:
            raise ValueError(f"{sample_context}.sections must be a non-empty list")

        for section_index, section in enumerate(sections):
            section_context = f"{sample_context}.sections[{section_index}]"
            if not isinstance(section, dict):
                raise ValueError(f"{section_context} must be an object")
            require_fields(section, REQUIRED_QUOTE_SECTION_FIELDS, section_context)
            ensure_non_empty_string(section["label"], f"{section_context}.label")

            lines = section["lines"]
            if not isinstance(lines, list) or not lines:
                raise ValueError(f"{section_context}.lines must be a non-empty list")
            for line_index, line in enumerate(lines):
                line_context = f"{section_context}.lines[{line_index}]"
                if not isinstance(line, dict):
                    raise ValueError(f"{line_context} must be an object")
                require_fields(line, REQUIRED_QUOTE_LINE_FIELDS, line_context)
                ensure_non_empty_string(line["label"], f"{line_context}.label")
                ensure_non_empty_string(line["value"], f"{line_context}.value")


def validate_design_pack(pack: dict, path: Path) -> None:
    require_fields(pack, PACK_REQUIRED_FIELDS, path.name)

    ensure_non_empty_string(pack["slug"], f"{path.name}.slug")
    ensure_non_empty_string(pack["title"], f"{path.name}.title")
    ensure_non_empty_string(pack["summary"], f"{path.name}.summary")
    ensure_non_empty_string(pack["preview_variant"], f"{path.name}.preview_variant")
    ensure_non_empty_string(pack["density"], f"{path.name}.density")
    ensure_non_empty_string(pack["imagery"], f"{path.name}.imagery")
    ensure_non_empty_string(pack["cta_tone"], f"{path.name}.cta_tone")
    ensure_non_empty_string(pack["zh_readability"], f"{path.name}.zh_readability")
    ensure_non_empty_string(pack["derived_from"], f"{path.name}.derived_from")
    ensure_non_empty_string(pack["governance_role"], f"{path.name}.governance_role")
    ensure_non_empty_string(pack["layout_focus"], f"{path.name}.layout_focus")
    ensure_non_empty_string(pack["notes"], f"{path.name}.notes")

    if not isinstance(pack["sort_order"], int):
        raise ValueError(f"{path.name}.sort_order must be an integer")

    if pack["governance_role"] not in ALLOWED_PACK_GOVERNANCE_ROLES:
        allowed = ", ".join(sorted(ALLOWED_PACK_GOVERNANCE_ROLES))
        raise ValueError(f"{path.name}.governance_role must be one of: {allowed}")

    ensure_string_list(pack["mood"], f"{path.name}.mood")
    ensure_string_list(pack["best_for_pages"], f"{path.name}.best_for_pages")
    ensure_string_list(pack["component_focus"], f"{path.name}.component_focus")
    ensure_string_list(pack["variation_scope"], f"{path.name}.variation_scope")
    ensure_module_list(pack["recommended_modules"], f"{path.name}.recommended_modules")

    preview_tokens = pack["preview_tokens"]
    preview_content = pack["preview_content"]
    if not isinstance(preview_tokens, dict):
        raise ValueError(f"{path.name}.preview_tokens must be an object")
    if not isinstance(preview_content, dict):
        raise ValueError(f"{path.name}.preview_content must be an object")

    require_fields(preview_tokens, PACK_REQUIRED_TOKEN_FIELDS, f"{path.name}.preview_tokens")
    require_fields(
        preview_content,
        PACK_REQUIRED_CONTENT_FIELDS,
        f"{path.name}.preview_content",
    )

    for token_name in PACK_REQUIRED_TOKEN_FIELDS:
        ensure_non_empty_string(
            preview_tokens[token_name],
            f"{path.name}.preview_tokens.{token_name}",
        )

    for content_name in PACK_REQUIRED_CONTENT_FIELDS:
        ensure_non_empty_string(
            preview_content[content_name],
            f"{path.name}.preview_content.{content_name}",
        )


def load_design_packs():
    if not PACKS_DIR.exists():
        raise FileNotFoundError(f"missing design packs directory: {PACKS_DIR}")

    pack_paths = sorted(PACKS_DIR.glob("*.json"))
    if not pack_paths:
        raise FileNotFoundError(f"no design pack JSON files found in {PACKS_DIR}")

    packs = []
    seen_slugs = set()

    for pack_path in pack_paths:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        validate_design_pack(pack, pack_path)
        if pack["slug"] in seen_slugs:
            raise ValueError(f"duplicate design pack slug detected: {pack['slug']}")
        seen_slugs.add(pack["slug"])
        packs.append(pack)

    return sorted(packs, key=lambda item: (item["sort_order"], item["slug"]))


def validate_artifact_surface(surface: dict, path: Path, pack_slugs: set[str]) -> None:
    require_fields(surface, ARTIFACT_REQUIRED_FIELDS, path.name)

    for field_name in [
        "slug",
        "title",
        "surface_type",
        "source_pack",
        "primary_use_case",
        "governance_role",
    ]:
        ensure_non_empty_string(surface[field_name], f"{path.name}.{field_name}")

    if surface["surface_type"] not in ALLOWED_ARTIFACT_SURFACE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_ARTIFACT_SURFACE_TYPES))
        raise ValueError(f"{path.name}.surface_type must be one of: {allowed}")

    if surface["governance_role"] not in ALLOWED_ARTIFACT_GOVERNANCE_ROLES:
        allowed = ", ".join(sorted(ALLOWED_ARTIFACT_GOVERNANCE_ROLES))
        raise ValueError(f"{path.name}.governance_role must be one of: {allowed}")

    if surface["source_pack"] not in pack_slugs:
        raise ValueError(
            f"{path.name}.source_pack must reference an existing design pack slug"
        )

    ensure_module_list(surface["recommended_modules"], f"{path.name}.recommended_modules")
    ensure_string_list(surface["layout_rules"], f"{path.name}.layout_rules")
    ensure_string_list(surface["failure_modes"], f"{path.name}.failure_modes")

    preview_content = surface["preview_content"]
    if not isinstance(preview_content, dict):
        raise ValueError(f"{path.name}.preview_content must be an object")

    require_fields(preview_content, ARTIFACT_REQUIRED_CONTENT_FIELDS, f"{path.name}.preview_content")
    for field_name in ARTIFACT_REQUIRED_CONTENT_FIELDS:
        ensure_non_empty_string(
            preview_content[field_name],
            f"{path.name}.preview_content.{field_name}",
        )

    if surface["surface_type"] == "quote_card":
        if "quote_samples" not in surface:
            raise ValueError(f"{path.name}.quote_samples required for quote_card surfaces")
        ensure_quote_samples(surface["quote_samples"], f"{path.name}.quote_samples")


def load_artifact_surfaces(pack_slugs: set[str]):
    if not ARTIFACT_SURFACES_DIR.exists():
        raise FileNotFoundError(f"missing artifact surfaces directory: {ARTIFACT_SURFACES_DIR}")

    surface_paths = sorted(ARTIFACT_SURFACES_DIR.glob("*.json"))
    if not surface_paths:
        raise FileNotFoundError(
            f"no artifact surface JSON files found in {ARTIFACT_SURFACES_DIR}"
        )

    surfaces = []
    seen_slugs = set()
    for surface_path in surface_paths:
        surface = json.loads(surface_path.read_text(encoding="utf-8"))
        validate_artifact_surface(surface, surface_path, pack_slugs)
        if surface["slug"] in seen_slugs:
            raise ValueError(f"duplicate artifact surface slug detected: {surface['slug']}")
        seen_slugs.add(surface["slug"])
        surfaces.append(surface)

    return surfaces


def render_filter_group(label: str, key: str, values) -> str:
    buttons = [
        '<button class="filter-button active" type="button" data-filter-key="{}" data-filter-value="all" aria-pressed="true">全部</button>'.format(
            html.escape(key)
        )
    ]
    for value in values:
        buttons.append(
            '<button class="filter-button" type="button" data-filter-key="{}" data-filter-value="{}" aria-pressed="false">{}</button>'.format(
                html.escape(key),
                html.escape(value),
                html.escape(value),
            )
        )

    return dedent(
        """
        <div class="filter-group">
          <span class="filter-label">{label}</span>
          <div class="filter-buttons">
            {buttons}
          </div>
        </div>
        """
    ).format(label=html.escape(label), buttons="".join(buttons))


def render_pack_tab_button(pack: dict) -> str:
    preview_tokens = pack["preview_tokens"]
    return dedent(
        """
        <button
          class="pack-tab"
          type="button"
          data-pack-tab="{slug}"
          data-variant="{variant}"
          style="{style}"
          aria-pressed="false"
        >
          <span class="pack-tab-kicker">{eyebrow}</span>
          <strong>{title}</strong>
          <span>{subtitle}</span>
        </button>
        """
    ).format(
        slug=html.escape(pack["slug"]),
        variant=html.escape(pack["preview_variant"]),
        style=html.escape(
            "; ".join(
                [
                    f"--pack-tab-bg:{preview_tokens['background']}",
                    f"--pack-tab-surface:{preview_tokens['surface']}",
                    f"--pack-tab-line:{preview_tokens['line']}",
                    f"--pack-tab-accent:{preview_tokens['accent']}",
                    f"--pack-tab-glow:{preview_tokens['hero_glow']}",
                ]
            )
        ),
        eyebrow=html.escape(pack["best_for_pages"][0]),
        title=html.escape(pack["title"]),
        subtitle=html.escape(f"{pack['cta_tone']} · {pack['density']}"),
    )


def render_pack_card(pack: dict) -> str:
    preview_tokens = pack["preview_tokens"]
    swatches = "".join(
        '<span class="pack-swatch" style="background:{};"></span>'.format(
            html.escape(preview_tokens[token_name])
        )
        for token_name in ("background", "surface", "elevated", "accent")
    )
    moods = "".join(
        '<span class="pack-chip">{}</span>'.format(html.escape(value))
        for value in pack["mood"]
    )

    return dedent(
        """
        <button
          class="pack-card"
          type="button"
          style="{style}"
          data-pack-slug="{slug}"
          data-pages="{pages}"
          data-density="{density}"
          data-cta="{cta_tone}"
          aria-pressed="false"
        >
          <span class="pack-card-eyebrow">{slug}</span>
          <span class="pack-swatch-row">{swatches}</span>
          <strong>{title}</strong>
          <p>{summary}</p>
          <div class="chip-row">{moods}</div>
          <div class="pack-card-meta">
            <span>角色：受控变化层</span>
            <span>适用页面：{pages_display}</span>
            <span>信息密度：{density}</span>
            <span>CTA 语气：{cta_tone}</span>
            <span>模块栈：{module_count} 段</span>
          </div>
        </button>
        """
    ).format(
        style=html.escape(render_pack_preview_style(pack)),
        slug=html.escape(pack["slug"]),
        pages=html.escape("|".join(pack["best_for_pages"])),
        density=html.escape(pack["density"]),
        cta_tone=html.escape(pack["cta_tone"]),
        swatches=swatches,
        title=html.escape(pack["title"]),
        summary=html.escape(pack["summary"]),
        moods=moods,
        pages_display=html.escape(" / ".join(pack["best_for_pages"])),
        module_count=len(pack["recommended_modules"]),
    )


def render_tag_list(items, class_name: str) -> str:
    return "".join(
        '<span class="{}">{}</span>'.format(
            html.escape(class_name),
            html.escape(item),
        )
        for item in items
    )


def render_pack_preview_style(pack: dict) -> str:
    preview_tokens = pack["preview_tokens"]
    styles = [
        ("--pack-background", preview_tokens["background"]),
        ("--pack-surface", preview_tokens["surface"]),
        ("--pack-elevated", preview_tokens["elevated"]),
        ("--pack-accent", preview_tokens["accent"]),
        ("--pack-line", preview_tokens["line"]),
        ("--pack-hero-glow", preview_tokens["hero_glow"]),
        ("--pack-panel-tint", preview_tokens["panel_tint"]),
        ("--pack-chip-tint", preview_tokens["chip_tint"]),
    ]
    return "; ".join(f"{name}: {value}" for name, value in styles)


def render_json_for_html(payload: object) -> str:
    return (
        json.dumps(payload, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def render_preview_button_row(content: dict) -> str:
    return dedent(
        """
        <div class="button-row preview-actions">
          <button class="primary-button" type="button">{primary}</button>
          <button class="secondary-button" type="button">{secondary}</button>
        </div>
        """
    ).format(
        primary=html.escape(content["primary_cta"]),
        secondary=html.escape(content["secondary_cta"]),
    )


def render_preview_stat_pills(pack: dict) -> str:
    items = [
        ("信息密度", pack["density"]),
        ("CTA 语气", pack["cta_tone"]),
        ("中文可读性", pack["zh_readability"]),
    ]
    return "".join(
        dedent(
            """
            <div class="preview-stat-pill">
              <span>{label}</span>
              <strong>{value}</strong>
            </div>
            """
        ).format(label=html.escape(label), value=html.escape(value))
        for label, value in items
    )


def render_preview_tag_block(title: str, items, class_name: str = "preview-detail-chip") -> str:
    return dedent(
        """
        <article class="preview-card">
          <strong>{title}</strong>
          <div class="preview-detail-list">
            {items}
          </div>
        </article>
        """
    ).format(
        title=html.escape(title),
        items=render_tag_list(items, class_name),
    )


def render_preview_text_card(title: str, body: str, extra_body: str | None = None) -> str:
    extra_markup = ""
    if extra_body:
        extra_markup = '<p class="preview-card-secondary">{}</p>'.format(
            html.escape(extra_body)
        )

    return dedent(
        """
        <article class="preview-card">
          <strong>{title}</strong>
          <p>{body}</p>
          {extra}
        </article>
        """
    ).format(
        title=html.escape(title),
        body=html.escape(body),
        extra=extra_markup,
    )


def render_module_recipe_cards(modules, class_name: str = "module-recipe-card") -> str:
    cards = []
    for index, module in enumerate(modules, start=1):
        cards.append(
            dedent(
                """
                <article class="{class_name}">
                  <span>{index:02d}</span>
                  <strong>{name}</strong>
                  <p>{purpose}</p>
                  <p class="preview-card-secondary">{layout_hint}</p>
                </article>
                """
            ).format(
                class_name=html.escape(class_name),
                index=index,
                name=html.escape(module["name"]),
                purpose=html.escape(module["purpose"]),
                layout_hint=html.escape(module["layout_hint"]),
            )
        )
    return "".join(cards)


def render_pack_preview_markup(pack: dict) -> str:
    content = pack["preview_content"]
    modules = pack["recommended_modules"]
    primary_modules = modules[:3]
    meta = '<div class="pack-preview-meta">Pack Preview · {slug}</div>'.format(
        slug=html.escape(pack["slug"])
    )
    summary = '<p class="preview-summary">{title} · {summary}</p>'.format(
        title=html.escape(pack["title"]),
        summary=html.escape(pack["summary"]),
    )
    mood_chips = '<div class="chip-row preview-chip-row">{}</div>'.format(
        render_tag_list(pack["mood"], "preview-chip")
    )
    buttons = render_preview_button_row(content)
    stat_pills = '<div class="preview-stat-pills">{}</div>'.format(
        render_preview_stat_pills(pack)
    )
    module_recipe_cards = render_module_recipe_cards(primary_modules, "preview-module-card")

    variant = pack["preview_variant"]

    if variant == "gallery":
        return dedent(
            """
            <div class="preview-layout preview-layout-gallery">
              <div class="preview-gallery-main">
                {meta}
                {summary}
                <div class="preview-gallery-stage">
                  <div class="preview-gallery-art">
                    <span class="preview-overline">{module_name}</span>
                    <h3 class="preview-title">{title}</h3>
                    <p class="preview-lead">{lead}</p>
                    {moods}
                  </div>
                  <div class="preview-gallery-note preview-card">
                    <strong>{module_note_title}</strong>
                    <p>{module_note_body}</p>
                    <p class="preview-quote-line">{module_note_hint}</p>
                  </div>
                </div>
                {buttons}
              </div>
              <aside class="preview-gallery-sidebar">
                {stats}
                {module_card}
                {imagery}
              </aside>
            </div>
            """
        ).format(
            meta=meta,
            summary=summary,
            module_name=html.escape(primary_modules[0]["name"]),
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            moods=mood_chips,
            module_note_title=html.escape(primary_modules[1]["name"]),
            module_note_body=html.escape(primary_modules[1]["purpose"]),
            module_note_hint=html.escape(primary_modules[1]["layout_hint"]),
            buttons=buttons,
            stats=stat_pills,
            module_card=render_preview_text_card(
                primary_modules[2]["name"],
                primary_modules[2]["purpose"],
                primary_modules[2]["layout_hint"],
            ),
            imagery=render_preview_text_card("图像策略", pack["imagery"], content["hero_note"]),
        )

    if variant == "editorial":
        return dedent(
            """
            <div class="preview-layout preview-layout-editorial">
              <aside class="preview-editorial-rail">
                <span class="preview-section-number">01</span>
                <div>
                  <p class="preview-rail-label">Material Dossier</p>
                  <p class="preview-rail-copy">{note}</p>
                </div>
                {stats}
              </aside>
              <div class="preview-editorial-main">
                {meta}
                {summary}
                <h3 class="preview-title">{title}</h3>
                <p class="preview-lead">{lead}</p>
                <div class="preview-editorial-columns">
                  {modules}
                </div>
                {buttons}
              </div>
            </div>
            """
        ).format(
            note=html.escape(content["hero_note"]),
            stats=stat_pills,
            meta=meta,
            summary=summary,
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            modules=module_recipe_cards,
            buttons=buttons,
        )

    if variant == "analytical":
        return dedent(
            """
            <div class="preview-layout preview-layout-analytical">
              <div class="preview-analytical-head">
                {meta}
                {summary}
                <h3 class="preview-title">{title}</h3>
                <p class="preview-lead">{lead}</p>
                {buttons}
              </div>
              <div class="preview-analytical-grid">
                {stats}
                {module_a}
                {module_b}
                {module_c}
                {notes}
              </div>
            </div>
            """
        ).format(
            meta=meta,
            summary=summary,
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            buttons=buttons,
            stats=stat_pills,
            module_a=render_preview_text_card(
                primary_modules[0]["name"],
                primary_modules[0]["purpose"],
                primary_modules[0]["layout_hint"],
            ),
            module_b=render_preview_text_card(
                primary_modules[1]["name"],
                primary_modules[1]["purpose"],
                primary_modules[1]["layout_hint"],
            ),
            module_c=render_preview_text_card(
                primary_modules[2]["name"],
                primary_modules[2]["purpose"],
                primary_modules[2]["layout_hint"],
            ),
            notes=render_preview_text_card("判断语气", content["quote"], content["hero_note"]),
        )

    if variant == "luxury":
        return dedent(
            """
            <div class="preview-layout preview-layout-luxury">
              <div class="preview-luxury-hero">
                {meta}
                <span class="preview-signature">Quiet Signature</span>
                {summary}
                <h3 class="preview-title">{title}</h3>
                <p class="preview-lead">{lead}</p>
                {moods}
                {buttons}
              </div>
              <div class="preview-luxury-band">
                {modules}
              </div>
            </div>
            """
        ).format(
            meta=meta,
            summary=summary,
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            moods=mood_chips,
            buttons=buttons,
            modules=module_recipe_cards,
        )

    if variant == "storytelling":
        return dedent(
            """
            <div class="preview-layout preview-layout-storytelling">
              <div class="preview-story-header">
                {meta}
                {summary}
                <h3 class="preview-title">{title}</h3>
                <p class="preview-lead">{lead}</p>
              </div>
              <div class="preview-story-grid">
                <div class="preview-timeline">
                  <div class="preview-timeline-item">
                    <span>01</span>
                    <div>
                      <strong>{module_one_title}</strong>
                      <p>{module_one_body}</p>
                    </div>
                  </div>
                  <div class="preview-timeline-item">
                    <span>02</span>
                    <div>
                      <strong>{module_two_title}</strong>
                      <p>{module_two_body}</p>
                    </div>
                  </div>
                  <div class="preview-timeline-item">
                    <span>03</span>
                    <div>
                      <strong>{module_three_title}</strong>
                      <p>{module_three_body}</p>
                    </div>
                  </div>
                </div>
                <aside class="preview-story-aside">
                  {pages}
                  {components}
                  <article class="preview-card">
                    <strong>建议语气</strong>
                    <p>{quote}</p>
                  </article>
                  {buttons}
                </aside>
              </div>
            </div>
            """
        ).format(
            meta=meta,
            summary=summary,
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            module_one_title=html.escape(primary_modules[0]["name"]),
            module_one_body=html.escape(primary_modules[0]["purpose"]),
            module_two_title=html.escape(primary_modules[1]["name"]),
            module_two_body=html.escape(primary_modules[1]["purpose"]),
            module_three_title=html.escape(primary_modules[2]["name"]),
            module_three_body=html.escape(primary_modules[2]["purpose"]),
            pages=render_preview_tag_block("章节适配", pack["best_for_pages"]),
            components=render_preview_tag_block("叙事组件", pack["component_focus"]),
            quote=html.escape(content["quote"]),
            buttons=buttons,
        )

    if variant == "consultation":
        return dedent(
            """
            <div class="preview-layout preview-layout-consultation">
              <div class="preview-consultation-main">
                {meta}
                {summary}
                <h3 class="preview-title">{title}</h3>
                <p class="preview-lead">{lead}</p>
                {buttons}
                <div class="preview-process-steps">
                  <article class="preview-step-card">
                    <span>01</span>
                    <strong>{module_one_title}</strong>
                    <p>{module_one_body}</p>
                  </article>
                  <article class="preview-step-card">
                    <span>02</span>
                    <strong>{module_two_title}</strong>
                    <p>{module_two_body}</p>
                  </article>
                  <article class="preview-step-card">
                    <span>03</span>
                    <strong>{module_three_title}</strong>
                    <p>{module_three_body}</p>
                  </article>
                </div>
              </div>
              <aside class="preview-consultation-aside">
                {stats}
                {pages}
                {components}
              </aside>
            </div>
            """
        ).format(
            meta=meta,
            summary=summary,
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            buttons=buttons,
            module_one_title=html.escape(primary_modules[0]["name"]),
            module_one_body=html.escape(primary_modules[0]["purpose"]),
            module_two_title=html.escape(primary_modules[1]["name"]),
            module_two_body=html.escape(primary_modules[1]["purpose"]),
            module_three_title=html.escape(primary_modules[2]["name"]),
            module_three_body=html.escape(primary_modules[2]["purpose"]),
            stats=stat_pills,
            pages=render_preview_tag_block("服务适配", pack["best_for_pages"]),
            components=render_preview_tag_block("承接组件", pack["component_focus"]),
        )

    raise ValueError(f"unsupported preview_variant: {variant}")


def build_pack_payload(pack: dict) -> dict:
    payload = dict(pack)
    payload["preview_markup"] = render_pack_preview_markup(pack)
    return payload


def surface_type_label(surface_type: str) -> str:
    labels = {
        "web": "网页样例",
        "mobile_h5": "手机 H5",
        "quote_card": "图文报价体",
    }
    return labels[surface_type]


def render_artifact_surface_card(surface: dict, pack: dict) -> str:
    preview_tokens = pack["preview_tokens"]
    preview_content = surface["preview_content"]
    module_names = "".join(
        '<li>{}</li>'.format(html.escape(module["name"]))
        for module in surface["recommended_modules"][:3]
    )
    return dedent(
        """
        <a class="artifact-card" href="/artifact-{slug}" style="{style}">
          <span class="artifact-card-type">{surface_type}</span>
          <div class="artifact-card-stage">
            <span class="artifact-card-pack">{pack_title}</span>
            <h3>{hero_title}</h3>
            <p>{hero_lead}</p>
          </div>
          <strong>{title}</strong>
          <p>{use_case}</p>
          <div class="artifact-card-meta">
            <span>绑定方向：{pack_title}</span>
            <span>核心场景：{use_case}</span>
            <span>主 CTA：{primary_cta}</span>
          </div>
          <ol class="artifact-card-modules">
            {module_names}
          </ol>
          <span class="artifact-card-link">查看这个成品</span>
        </a>
        """
    ).format(
        slug=html.escape(surface["slug"]),
        style=html.escape(
            "; ".join(
                [
                    f"--artifact-bg:{preview_tokens['background']}",
                    f"--artifact-surface:{preview_tokens['surface']}",
                    f"--artifact-elevated:{preview_tokens['elevated']}",
                    f"--artifact-line:{preview_tokens['line']}",
                    f"--artifact-accent:{preview_tokens['accent']}",
                    f"--artifact-glow:{preview_tokens['hero_glow']}",
                ]
            )
        ),
        surface_type=html.escape(surface_type_label(surface["surface_type"])),
        title=html.escape(surface["title"]),
        use_case=html.escape(surface["primary_use_case"]),
        pack_title=html.escape(pack["title"]),
        hero_title=html.escape(preview_content["hero_title"]),
        hero_lead=html.escape(preview_content["hero_lead"]),
        primary_cta=html.escape(preview_content["primary_cta"]),
        module_names=module_names,
    )


def render_artifact_modules(modules) -> str:
    return "".join(
        dedent(
            """
            <article class="artifact-module-card">
              <span>{index:02d}</span>
              <strong>{name}</strong>
              <p>{purpose}</p>
              <p class="artifact-muted">{layout_hint}</p>
            </article>
            """
        ).format(
            index=index,
            name=html.escape(module["name"]),
            purpose=html.escape(module["purpose"]),
            layout_hint=html.escape(module["layout_hint"]),
        )
        for index, module in enumerate(modules, start=1)
    )


def render_artifact_rules(layout_rules) -> str:
    return "".join(
        "<li>{}</li>".format(html.escape(rule))
        for rule in layout_rules
    )


def render_quote_sample_section(section: dict) -> str:
    lines = "".join(
        '<div class="quote-sample-line"><span>{}</span><strong>{}</strong></div>'.format(
            html.escape(line["label"]),
            html.escape(line["value"]),
        )
        for line in section["lines"]
    )
    return dedent(
        """
        <section class="quote-sample-section">
          <span class="quote-sample-section-label">{label}</span>
          {lines}
        </section>
        """
    ).format(label=html.escape(section["label"]), lines=lines)


def render_quote_sample_cards(samples) -> str:
    cards = []
    for sample in samples:
        reference_class = ""
        if sample["quote_type"] == "reference_quote":
            reference_class = " quote-sample-card--reference"
        cards.append(
            dedent(
                """
                <article class="quote-sample-card{reference_class}">
                  <div class="quote-sample-topbar">
                    <span class="quote-badge">{badge}</span>
                    <span class="quote-sample-eyebrow">{eyebrow}</span>
                  </div>
                  <div class="quote-sample-hero">
                    <div>
                      <h3>{product_name}</h3>
                      <p>{subtitle}</p>
                    </div>
                    <strong>{total_price}</strong>
                  </div>
                  <div class="quote-sample-tags">{tags}</div>
                  <p class="quote-sample-scenario">{scenario}</p>
                  <div class="quote-sample-sections">{sections}</div>
                  <p class="quote-sample-note">{note}</p>
                </article>
                """
            ).format(
                reference_class=reference_class,
                badge=html.escape(sample["badge"]),
                eyebrow=html.escape(sample["eyebrow"]),
                product_name=html.escape(sample["product_name"]),
                subtitle=html.escape(sample["subtitle"]),
                total_price=html.escape(sample["total_price"]),
                tags="".join(
                    '<span>{}</span>'.format(html.escape(tag))
                    for tag in sample["tags"]
                ),
                scenario=html.escape(sample["scenario"]),
                sections="".join(
                    render_quote_sample_section(section)
                    for section in sample["sections"]
                ),
                note=html.escape(sample["note"]),
            )
        )
    return "".join(cards)


def render_artifact_surface_page(dna: dict, surface: dict, pack: dict) -> str:
    colors = dna["design_system"]["color"]
    typography = dna["design_system"]["typography"]["type_scale"]
    content = surface["preview_content"]
    pack_style = render_pack_preview_style(pack)
    module_cards = render_artifact_modules(surface["recommended_modules"])
    rules = render_artifact_rules(surface["layout_rules"])
    failure_modes = render_artifact_rules(surface["failure_modes"])
    badge = surface_type_label(surface["surface_type"])

    quote_gallery = ""
    stage_markup = ""
    if surface["surface_type"] == "web":
        stage_markup = dedent(
            """
            <section class="artifact-stage artifact-stage-web">
              <div class="artifact-stage-copy">
                <span class="artifact-kicker">{eyebrow}</span>
                <h1>{title}</h1>
                <p>{lead}</p>
                <div class="artifact-actions">
                  <button type="button" class="artifact-primary">{primary_cta}</button>
                  <button type="button" class="artifact-secondary">{secondary_cta}</button>
                </div>
              </div>
              <aside class="artifact-stage-panel">
                <strong>Page Goal</strong>
                <p>{page_goal}</p>
                <p class="artifact-muted">绑定 Pack：{pack_title}</p>
              </aside>
            </section>
            """
        ).format(
            eyebrow=html.escape(content["eyebrow"]),
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            primary_cta=html.escape(content["primary_cta"]),
            secondary_cta=html.escape(content["secondary_cta"]),
            page_goal=html.escape(content["page_goal"]),
            pack_title=html.escape(pack["title"]),
        )
    elif surface["surface_type"] == "mobile_h5":
        stage_markup = dedent(
            """
            <section class="artifact-stage artifact-stage-mobile">
              <div class="mobile-frame">
                <div class="mobile-status">
                  <span>9:41</span>
                  <span>良禽佳木 H5</span>
                </div>
                <div class="mobile-body">
                  <span class="artifact-kicker">{eyebrow}</span>
                  <h1>{title}</h1>
                  <p>{lead}</p>
                  <div class="mobile-module-stack">
                    {mobile_modules}
                  </div>
                </div>
                <div class="mobile-actions">
                  <button type="button" class="artifact-primary">{primary_cta}</button>
                  <button type="button" class="artifact-secondary">{secondary_cta}</button>
                </div>
              </div>
              <aside class="artifact-stage-panel">
                <strong>Page Goal</strong>
                <p>{page_goal}</p>
                <p class="artifact-muted">手机 H5 重点检验窄屏秩序、CTA 承接和 FAQ/流程节奏。</p>
              </aside>
            </section>
            """
        ).format(
            eyebrow=html.escape(content["eyebrow"]),
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            mobile_modules="".join(
                '<div class="mobile-module-item"><strong>{}</strong><p>{}</p></div>'.format(
                    html.escape(module["name"]),
                    html.escape(module["purpose"]),
                )
                for module in surface["recommended_modules"][:3]
            ),
            primary_cta=html.escape(content["primary_cta"]),
            secondary_cta=html.escape(content["secondary_cta"]),
            page_goal=html.escape(content["page_goal"]),
        )
    else:
        quote_gallery = dedent(
            """
            <section class="quote-sample-shell" id="quote-samples">
              <div class="quote-sample-intro">
                <strong>真实报价样例</strong>
                <p>下面每张卡都来自结构化报价数据，而不是规则说明文案。目标是让客户先理解产品与总价，再理解条件与边界。</p>
              </div>
              <div class="quote-sample-grid">
                {cards}
              </div>
            </section>
            """
        ).format(cards=render_quote_sample_cards(surface["quote_samples"]))
        stage_markup = dedent(
            """
            <section class="artifact-stage artifact-stage-quote">
              <div class="artifact-stage-copy">
                <span class="artifact-kicker">{eyebrow}</span>
                <h1>{title}</h1>
                <p>{lead}</p>
                <div class="artifact-actions">
                  <a class="artifact-primary artifact-link" href="#quote-samples">{primary_cta}</a>
                  <button type="button" class="artifact-secondary">{secondary_cta}</button>
                </div>
              </div>
              <aside class="artifact-stage-panel">
                <strong>报价页判断标准</strong>
                <p>{page_goal}</p>
                <p class="artifact-muted">如果没有真实报价数据，就不应该开始做报价成品页。</p>
              </aside>
            </section>
            """
        ).format(
            eyebrow=html.escape(content["eyebrow"]),
            title=html.escape(content["hero_title"]),
            lead=html.escape(content["hero_lead"]),
            primary_cta=html.escape(content["primary_cta"]),
            secondary_cta=html.escape(content["secondary_cta"]),
            page_goal=html.escape(content["page_goal"]),
        )

    return (
        dedent(
            f"""
            <!doctype html>
            <html lang="zh-CN">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>{html.escape(surface['title'])} · 良禽佳木载体样例</title>
              <style>
                @font-face {{
                  font-family: "Swei Sugar";
                  src:
                    url("assets/fonts/SweiSugarCJKtc-ExtraLight.woff2") format("woff2"),
                    url("assets/fonts/SweiSugarCJKtc-ExtraLight.ttf") format("truetype");
                  font-style: normal;
                  font-weight: 200;
                  font-display: swap;
                }}

                @font-face {{
                  font-family: "OPPO Sans 4.0";
                  src:
                    url("assets/fonts/OPPO-Sans-4.0.woff2") format("woff2"),
                    url("assets/fonts/OPPO-Sans-4.0.ttf") format("truetype");
                  font-style: normal;
                  font-weight: 400;
                  font-display: swap;
                }}

                :root {{
                  --bg: {colors['surface']['background']};
                  --surface: {colors['surface']['card']};
                  --surface-elevated: {colors['surface']['elevated']};
                  --ink: {colors['primary']['hex']};
                  --line: {colors['neutral']['scale']['200']};
                  --muted: {colors['neutral']['scale']['500']};
                  --shadow-low: 0 10px 24px rgba(31, 29, 27, 0.05);
                  --shadow-medium: 0 18px 40px rgba(31, 29, 27, 0.08);
                }}

                * {{ box-sizing: border-box; }}
                body {{
                  margin: 0;
                  background: linear-gradient(180deg, var(--bg) 0%, #fffdf9 100%);
                  color: var(--ink);
                  font-family: "OPPO Sans 4.0", "PingFang SC", "Noto Sans SC", sans-serif;
                  line-height: {typography['body']['line_height']};
                }}
                a {{ color: inherit; text-decoration: none; }}
                button {{ font: inherit; }}
                .artifact-shell {{
                  width: min(1160px, calc(100vw - 32px));
                  margin: 0 auto;
                  padding: 28px 0 80px;
                }}
                .artifact-topbar {{
                  display: flex;
                  justify-content: space-between;
                  gap: 16px;
                  align-items: center;
                  margin-bottom: 20px;
                }}
                .artifact-breadcrumbs {{
                  display: flex;
                  gap: 12px;
                  flex-wrap: wrap;
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}
                .artifact-chip {{
                  display: inline-flex;
                  align-items: center;
                  padding: 7px 12px;
                  border: 1px solid var(--line);
                  border-radius: 999px;
                  background: rgba(255,255,255,0.74);
                }}
                .artifact-hero {{
                  padding: 28px;
                  border-radius: 28px;
                  border: 1px solid var(--pack-line);
                  background:
                    radial-gradient(circle at top right, var(--pack-hero-glow), transparent 35%),
                    linear-gradient(135deg, var(--pack-elevated), var(--pack-background));
                  box-shadow: var(--shadow-medium);
                }}
                .artifact-kicker {{
                  display: inline-flex;
                  padding: 8px 14px;
                  border-radius: 999px;
                  border: 1px solid var(--pack-line);
                  color: var(--pack-accent);
                  background: rgba(255,255,255,0.68);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                  text-transform: uppercase;
                }}
                .artifact-stage {{
                  display: grid;
                  gap: 24px;
                  align-items: start;
                }}
                .artifact-stage-web,
                .artifact-stage-quote {{
                  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
                }}
                .artifact-stage-mobile {{
                  grid-template-columns: minmax(300px, 420px) minmax(0, 1fr);
                  justify-content: center;
                }}
                .artifact-stage-copy {{
                  display: grid;
                  gap: 16px;
                }}
                .artifact-stage-copy h1 {{
                  margin: 0;
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-weight: 200;
                  font-size: {typography['display']['size']};
                  line-height: {typography['display']['line_height']};
                  letter-spacing: {typography['display']['tracking']};
                  max-width: 12ch;
                }}
                .artifact-stage-panel,
                .artifact-section,
                .artifact-module-card,
                .quote-artifact-card,
                .mobile-module-item {{
                  padding: 20px;
                  border-radius: 22px;
                  border: 1px solid var(--pack-line);
                  background: var(--pack-panel-tint);
                }}
                .artifact-stage-panel strong,
                .artifact-section strong,
                .artifact-module-card strong,
                .quote-artifact-card h3,
                .mobile-module-item strong {{
                  display: block;
                  margin-bottom: 8px;
                }}
                .artifact-muted {{
                  color: #61574d;
                  font-size: {typography['body_small']['size']};
                }}
                .artifact-actions {{
                  display: flex;
                  gap: 12px;
                  flex-wrap: wrap;
                }}
                .artifact-primary,
                .artifact-secondary {{
                  min-height: 46px;
                  padding: 0 22px;
                  border-radius: 999px;
                  border: 1px solid transparent;
                  cursor: pointer;
                }}
                .artifact-primary {{
                  background: var(--pack-accent);
                  color: #fffaf5;
                }}
                .artifact-secondary {{
                  background: transparent;
                  border-color: var(--pack-line);
                  color: var(--ink);
                }}
                .artifact-link {{
                  display: inline-flex;
                  align-items: center;
                }}
                .artifact-grid {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                  margin-top: 24px;
                }}
                .artifact-module-card span {{
                  color: var(--pack-accent);
                  font-size: {typography['caption']['size']};
                }}
                .artifact-rule-list {{
                  margin: 0;
                  padding-left: 18px;
                  display: grid;
                  gap: 8px;
                }}
                .mobile-frame {{
                  width: min(100%, 390px);
                  border-radius: 36px;
                  border: 1px solid var(--pack-line);
                  background: color-mix(in srgb, var(--pack-background) 88%, white);
                  box-shadow: var(--shadow-medium);
                  overflow: hidden;
                }}
                .mobile-status,
                .mobile-actions {{
                  display: flex;
                  align-items: center;
                  justify-content: space-between;
                  padding: 14px 18px;
                  border-bottom: 1px solid var(--pack-line);
                }}
                .mobile-actions {{
                  gap: 10px;
                  border-top: 1px solid var(--pack-line);
                  border-bottom: none;
                }}
                .mobile-body {{
                  display: grid;
                  gap: 16px;
                  padding: 20px 18px;
                }}
                .mobile-body h1 {{
                  margin: 0;
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-weight: 200;
                  font-size: {typography['heading_1']['size']};
                  line-height: {typography['heading_1']['line_height']};
                }}
                .mobile-module-stack,
                .quote-artifact-gallery {{
                  display: grid;
                  gap: 12px;
                }}
                .quote-artifact-gallery {{
                  margin-top: 24px;
                  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                }}
                .quote-badge {{
                  display: inline-flex;
                  margin-bottom: 10px;
                  padding: 6px 10px;
                  border-radius: 999px;
                  border: 1px solid var(--pack-line);
                  color: var(--pack-accent);
                  font-size: {typography['caption']['size']};
                }}
                .quote-badge-reference {{
                  color: #7a6555;
                }}
                .quote-sample-shell {{
                  display: grid;
                  gap: 18px;
                  margin-top: 28px;
                }}
                .quote-sample-intro {{
                  display: grid;
                  gap: 8px;
                  padding: 20px 24px;
                  border: 1px solid var(--pack-line);
                  border-radius: 24px;
                  background: rgba(255, 255, 255, 0.72);
                  box-shadow: var(--shadow-low);
                }}
                .quote-sample-grid {{
                  display: grid;
                  gap: 18px;
                  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                }}
                .quote-sample-card {{
                  display: grid;
                  gap: 16px;
                  padding: 24px;
                  border: 1px solid var(--pack-line);
                  border-radius: 28px;
                  background:
                    linear-gradient(180deg, rgba(255, 252, 248, 0.98), rgba(248, 245, 240, 0.94));
                  box-shadow: var(--shadow-medium);
                }}
                .quote-sample-card--reference {{
                  background:
                    linear-gradient(180deg, rgba(255, 250, 245, 0.98), rgba(245, 239, 232, 0.96));
                }}
                .quote-sample-topbar,
                .quote-sample-line,
                .quote-sample-hero {{
                  display: flex;
                  align-items: flex-start;
                  justify-content: space-between;
                  gap: 14px;
                }}
                .quote-sample-eyebrow,
                .quote-sample-section-label {{
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.08em;
                  text-transform: uppercase;
                }}
                .quote-sample-hero {{
                  align-items: end;
                  padding-bottom: 14px;
                  border-bottom: 1px solid var(--pack-line);
                }}
                .quote-sample-hero h3 {{
                  margin: 0 0 6px;
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-weight: 200;
                  font-size: {typography['heading_2']['size']};
                  line-height: {typography['heading_2']['line_height']};
                }}
                .quote-sample-hero p,
                .quote-sample-scenario,
                .quote-sample-note {{
                  color: #5d574f;
                }}
                .quote-sample-hero strong {{
                  color: var(--ink-deep);
                  font-size: {typography['heading_3']['size']};
                  line-height: {typography['heading_3']['line_height']};
                }}
                .quote-sample-tags {{
                  display: flex;
                  flex-wrap: wrap;
                  gap: 10px;
                }}
                .quote-sample-tags span {{
                  padding: 7px 12px;
                  border-radius: 999px;
                  background: color-mix(in srgb, var(--pack-surface) 82%, white);
                  border: 1px solid var(--pack-line);
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}
                .quote-sample-sections {{
                  display: grid;
                  gap: 14px;
                }}
                .quote-sample-section {{
                  display: grid;
                  gap: 10px;
                  padding: 16px 18px;
                  border-radius: 18px;
                  background: color-mix(in srgb, var(--pack-surface) 72%, white);
                  border: 1px solid color-mix(in srgb, var(--pack-line) 88%, white);
                }}
                .quote-sample-line {{
                  padding-top: 10px;
                  border-top: 1px solid color-mix(in srgb, var(--pack-line) 75%, white);
                }}
                .quote-sample-line:first-of-type {{
                  padding-top: 0;
                  border-top: none;
                }}
                .quote-sample-line span,
                .quote-sample-line strong {{
                  font-size: {typography['body_small']['size']};
                }}
                .quote-sample-line span {{
                  color: var(--muted);
                }}
                .quote-sample-line strong {{
                  color: var(--ink);
                  text-align: right;
                }}
                @media (max-width: 920px) {{
                  .artifact-stage-web,
                  .artifact-stage-quote,
                  .artifact-stage-mobile {{
                    grid-template-columns: 1fr;
                  }}
                }}
              </style>
            </head>
            <body>
              <main class="artifact-shell">
                <div class="artifact-topbar">
                  <div class="artifact-breadcrumbs">
                    <a class="artifact-chip" href="/">首页</a>
                    <a class="artifact-chip" href="/design-preview">Design Preview</a>
                    <span class="artifact-chip">{html.escape(badge)}</span>
                  </div>
                  <div class="artifact-breadcrumbs">
                    <span>绑定 Pack：{html.escape(pack['title'])}</span>
                    <span>用途：{html.escape(surface['primary_use_case'])}</span>
                  </div>
                </div>

                <section class="artifact-hero" style="{html.escape(pack_style)}">
                  {stage_markup}
                </section>

                {quote_gallery}

                <section class="artifact-grid">
                  {module_cards}
                </section>

                <section class="artifact-grid">
                  <article class="artifact-section">
                    <strong>载体类型</strong>
                    <p>{html.escape(badge)}</p>
                  </article>
                  <article class="artifact-section">
                    <strong>绑定风格包</strong>
                    <p>{html.escape(pack['slug'])}</p>
                  </article>
                  <article class="artifact-section">
                    <strong>核心用途</strong>
                    <p>{html.escape(surface['primary_use_case'])}</p>
                  </article>
                  <article class="artifact-section">
                    <strong>布局规则</strong>
                    <ul class="artifact-rule-list">
                      {rules}
                    </ul>
                  </article>
                  <article class="artifact-section">
                    <strong>易失真点</strong>
                    <ul class="artifact-rule-list">
                      {failure_modes}
                    </ul>
                  </article>
                </section>
              </main>
            </body>
            </html>
            """
        ).strip()
        + "\n"
    )


def generate_preview_html(dna: dict, packs, artifact_surfaces) -> str:
    meta = dna["meta"]
    colors = dna["design_system"]["color"]
    typography = dna["design_system"]["typography"]["type_scale"]
    spacing = dna["design_system"]["spacing"]
    elevation = dna["design_system"]["elevation"]["levels"]
    components = dna["design_system"]["components"]
    design_style = dna["design_style"]
    localization = dna["localization"]

    swatch_items = [
        ("Background", colors["surface"]["background"], "页面主背景"),
        ("Surface", colors["surface"]["card"], "卡片 / 次级背景"),
        ("Elevated", colors["surface"]["elevated"], "浮层 / 强调区块"),
        ("Ink 900", colors["neutral"]["scale"]["900"], "最深正文"),
        ("Primary Ink", colors["primary"]["hex"], "品牌锚点"),
        ("Accent", colors["accent"]["hex"], "CTA / 重点链接"),
        ("Brand Asset", colors["brand_asset"]["hex"], "品牌资产色"),
        ("Line", colors["neutral"]["scale"]["200"], "分割线"),
    ]
    swatches = []
    for name, value, note in swatch_items:
        swatches.append(
            """
            <article class="swatch-card">
              <div class="swatch" style="background:{value};"></div>
              <strong>{name}</strong>
              <code>{value}</code>
              <p>{note}</p>
            </article>
            """.format(
                name=html.escape(name),
                value=html.escape(value),
                note=html.escape(note),
            )
        )

    neutral_scale = []
    for level, value in colors["neutral"]["scale"].items():
        neutral_scale.append(
            """
            <div class="neutral-row">
              <span>N{level}</span>
              <div class="neutral-bar" style="background:{value};"></div>
              <code>{value}</code>
            </div>
            """.format(level=html.escape(level), value=html.escape(value))
        )

    pack_map = {pack["slug"]: pack for pack in packs}
    featured_packs = [
        pack_map[slug]
        for slug in FEATURED_PREVIEW_PACK_SLUGS
        if slug in pack_map
    ] or packs[:3]

    pack_tabs = "".join(render_pack_tab_button(pack) for pack in featured_packs)
    pack_payloads = [build_pack_payload(pack) for pack in featured_packs]
    pack_data_json = render_json_for_html(pack_payloads)
    default_pack = featured_packs[0]
    default_pack_payload = pack_payloads[0]
    artifact_cards = "".join(
        render_artifact_surface_card(surface, pack_map[surface["source_pack"]])
        for surface in artifact_surfaces
    )

    script = dedent(
        """
        <script id="design-pack-data" type="application/json">{pack_data}</script>
        <script>
          (() => {{
            const packDataElement = document.getElementById("design-pack-data");
            if (!packDataElement) {{
              return;
            }}

            const packs = JSON.parse(packDataElement.textContent);
            const packMap = new Map(packs.map((pack) => [pack.slug, pack]));

            let activeSlug = window.location.hash.replace(/^#/, "");
            if (!packMap.has(activeSlug) && packs.length) {{
              activeSlug = packs[0].slug;
            }}

            const packTabs = Array.from(document.querySelectorAll(".pack-tab"));
            const preview = document.getElementById("pack-preview");

            const previewFields = {{
              pages: document.getElementById("pack-preview-pages"),
              layout: document.getElementById("pack-preview-layout"),
              notes: document.getElementById("pack-preview-notes"),
              ctaTone: document.getElementById("pack-preview-cta"),
              tabMeaning: document.getElementById("style-direction-note"),
            }};

            const renderTagGroup = (container, values, className) => {{
              if (!container) {{
                return;
              }}

              container.replaceChildren();
              values.forEach((value) => {{
                const item = document.createElement("span");
                item.className = className;
                item.textContent = value;
                container.appendChild(item);
              }});
            }};

            const updatePreview = () => {{
              const pack = packMap.get(activeSlug);
              if (!pack || !preview) {{
                return;
              }}

              preview.dataset.variant = pack.preview_variant;
              Object.entries(pack.preview_tokens).forEach(([key, value]) => {{
                preview.style.setProperty("--pack-" + key.replace(/_/g, "-"), value);
              }});
              preview.innerHTML = pack.preview_markup;
              previewFields.layout.textContent = pack.layout_focus;
              previewFields.notes.textContent = pack.notes;
              previewFields.ctaTone.textContent = pack.cta_tone;
              previewFields.tabMeaning.textContent =
                "当前方向是「" + pack.title + "」，重点看版式气质、信息节奏和行动语气怎么变化。";

              renderTagGroup(previewFields.pages, pack.best_for_pages, "detail-chip");
              packTabs.forEach((tab) => {{
                const isActive = tab.dataset.packTab === activeSlug;
                tab.classList.toggle("active", isActive);
                tab.setAttribute("aria-pressed", isActive ? "true" : "false");
              }});
            }};

            packTabs.forEach((tab) => {{
              tab.addEventListener("click", () => {{
                activeSlug = tab.dataset.packTab;
                history.replaceState(null, "", "#" + activeSlug);
                updatePreview();
              }});
            }});

            window.addEventListener("hashchange", () => {{
              const nextSlug = window.location.hash.replace(/^#/, "");
              if (!packMap.has(nextSlug)) {{
                return;
              }}

              activeSlug = nextSlug;
              updatePreview();
            }});

            updatePreview();
          }})();
        </script>
        """
    ).format(pack_data=pack_data_json)

    return (
        dedent(
            f"""
            <!doctype html>
            <html lang="zh-CN">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>Liangqin Ji Mu DESIGN.md Preview</title>
              <style>
                @font-face {{
                  font-family: "Swei Sugar";
                  src:
                    url("assets/fonts/SweiSugarCJKtc-ExtraLight.woff2") format("woff2"),
                    url("assets/fonts/SweiSugarCJKtc-ExtraLight.ttf") format("truetype");
                  font-style: normal;
                  font-weight: 200;
                  font-display: swap;
                }}

                @font-face {{
                  font-family: "OPPO Sans 4.0";
                  src:
                    url("assets/fonts/OPPO-Sans-4.0.woff2") format("woff2"),
                    url("assets/fonts/OPPO-Sans-4.0.ttf") format("truetype");
                  font-style: normal;
                  font-weight: 400;
                  font-display: swap;
                }}

                :root {{
                  --bg: {colors['surface']['background']};
                  --surface: {colors['surface']['card']};
                  --surface-elevated: {colors['surface']['elevated']};
                  --ink: {colors['primary']['hex']};
                  --ink-deep: {colors['neutral']['scale']['900']};
                  --muted: {colors['neutral']['scale']['500']};
                  --line: {colors['neutral']['scale']['200']};
                  --accent: {colors['accent']['hex']};
                  --brand-asset: {colors['brand_asset']['hex']};
                  --shadow-low: {elevation['low']};
                  --shadow-medium: {elevation['medium']};
                }}

                * {{
                  box-sizing: border-box;
                }}

                [hidden] {{
                  display: none !important;
                }}

                body {{
                  margin: 0;
                  background: linear-gradient(180deg, var(--bg) 0%, #fffdf9 100%);
                  color: var(--ink);
                  font-family: "OPPO Sans 4.0", "PingFang SC", "Noto Sans SC", sans-serif;
                  line-height: {typography['body']['line_height']};
                }}

                img {{
                  max-width: 100%;
                  display: block;
                }}

                button {{
                  font: inherit;
                }}

                .shell {{
                  width: min(1180px, calc(100vw - 32px));
                  margin: 0 auto;
                  padding: 32px 0 96px;
                }}

                .hero {{
                  position: relative;
                  overflow: hidden;
                  padding: 32px;
                  border: 1px solid var(--line);
                  border-radius: 28px;
                  background:
                    radial-gradient(circle at top right, rgba(156, 127, 102, 0.14), transparent 32%),
                    linear-gradient(135deg, rgba(255, 252, 248, 0.96), rgba(242, 238, 232, 0.96));
                  box-shadow: var(--shadow-medium);
                }}

                .hero-meta,
                .pack-preview-meta {{
                  display: inline-flex;
                  align-items: center;
                  gap: 12px;
                  padding: 8px 14px;
                  border: 1px solid var(--line);
                  border-radius: 999px;
                  color: var(--muted);
                  background: rgba(255, 255, 255, 0.66);
                  font-size: {typography['caption']['size']};
                }}

                .hero-grid {{
                  display: grid;
                  gap: 24px;
                  grid-template-columns: minmax(0, 1.3fr) minmax(260px, 0.7fr);
                  align-items: end;
                  margin-top: 24px;
                }}

                .brand-mark {{
                  width: 180px;
                  opacity: 0.92;
                  margin-bottom: 24px;
                }}

                h1,
                h2,
                h3 {{
                  margin: 0;
                  color: var(--ink-deep);
                  font-family: "Swei Sugar", "Source Han Serif SC", "Songti SC", serif;
                  font-weight: 200;
                }}

                h1 {{
                  font-size: {typography['display']['size']};
                  line-height: {typography['display']['line_height']};
                  letter-spacing: {typography['display']['tracking']};
                  max-width: 10ch;
                }}

                h2 {{
                  font-size: {typography['heading_2']['size']};
                  line-height: {typography['heading_2']['line_height']};
                  letter-spacing: {typography['heading_2']['tracking']};
                  margin-bottom: 18px;
                }}

                h3 {{
                  font-size: {typography['heading_1']['size']};
                  line-height: {typography['heading_1']['line_height']};
                  letter-spacing: {typography['heading_1']['tracking']};
                }}

                p {{
                  margin: 0;
                  color: var(--ink);
                  font-size: {typography['body']['size']};
                }}

                .hero-copy {{
                  display: grid;
                  gap: 18px;
                }}

                .hero-copy .lead {{
                  max-width: 34em;
                  color: #4b4640;
                }}

                .chip-row,
                .button-row,
                .detail-chip-list {{
                  display: flex;
                  flex-wrap: wrap;
                  gap: 12px;
                }}

                .chip,
                .pack-chip,
                .preview-chip,
                .detail-chip {{
                  padding: 8px 14px;
                  border: 1px solid var(--line);
                  border-radius: 999px;
                  background: rgba(255, 255, 255, 0.72);
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .primary-button,
                .secondary-button {{
                  min-height: 46px;
                  padding: 0 24px;
                  border-radius: 999px;
                  border: 1px solid transparent;
                  cursor: pointer;
                }}

                .primary-button {{
                  background: var(--ink);
                  color: var(--bg);
                  box-shadow: var(--shadow-low);
                }}

                .secondary-button {{
                  background: transparent;
                  color: var(--ink);
                  border-color: var(--line);
                }}

                .hero-panel {{
                  padding: 24px;
                  border-radius: 22px;
                  background: rgba(255, 252, 248, 0.88);
                  border: 1px solid rgba(216, 208, 196, 0.9);
                  box-shadow: var(--shadow-low);
                }}

                .hero-panel strong,
                .detail-card strong {{
                  display: block;
                  margin-bottom: 10px;
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                  text-transform: uppercase;
                  color: var(--brand-asset);
                }}

                .section {{
                  margin-top: 32px;
                  padding: 28px;
                  border-radius: 24px;
                  border: 1px solid var(--line);
                  background: rgba(255, 252, 248, 0.78);
                }}

                .section-header {{
                  display: flex;
                  align-items: flex-end;
                  justify-content: space-between;
                  gap: 16px;
                  margin-bottom: 20px;
                }}

                .section-header p,
                .section-kicker,
                .detail-card p,
                .preview-layout p,
                .pack-card p,
                .empty-state {{
                  color: var(--muted);
                  font-size: {typography['body_small']['size']};
                }}

                .section-kicker {{
                  max-width: 22em;
                  text-align: right;
                }}

                .pack-tabs-shell {{
                  display: grid;
                  gap: 16px;
                }}

                .pack-tabs-note {{
                  padding: 14px 16px;
                  border: 1px solid var(--line);
                  border-radius: 16px;
                  background: rgba(255, 255, 255, 0.68);
                  color: var(--muted);
                  font-size: {typography['body_small']['size']};
                }}

                .pack-tab-row {{
                  display: flex;
                  gap: 12px;
                  overflow-x: auto;
                  padding-bottom: 6px;
                  scrollbar-width: none;
                }}

                .pack-tab-row::-webkit-scrollbar {{
                  display: none;
                }}

                .pack-tab {{
                  display: grid;
                  gap: 4px;
                  min-width: 176px;
                  min-height: 88px;
                  padding: 14px 16px 16px;
                  border-radius: 22px;
                  border: 1px solid var(--pack-tab-line, var(--line));
                  background:
                    radial-gradient(circle at top right, var(--pack-tab-glow, rgba(156, 127, 102, 0.12)), transparent 38%),
                    linear-gradient(180deg, color-mix(in srgb, var(--pack-tab-surface, rgba(255,255,255,0.9)) 92%, white), var(--pack-tab-bg, rgba(255, 255, 255, 0.82)));
                  color: var(--ink);
                  text-align: left;
                  cursor: pointer;
                  box-shadow: inset 0 1px 0 rgba(255,255,255,0.75);
                }}

                .pack-tab-kicker {{
                  display: inline-flex;
                  width: fit-content;
                  margin-bottom: 2px;
                  padding: 4px 9px;
                  border-radius: 999px;
                  border: 1px solid color-mix(in srgb, var(--pack-tab-accent, var(--accent)) 20%, transparent);
                  color: var(--pack-tab-accent, var(--brand-asset));
                  background: rgba(255,255,255,0.54);
                  font-size: 11px;
                  letter-spacing: 0.08em;
                  text-transform: uppercase;
                }}

                .pack-tab strong {{
                  font-size: {typography['body_small']['size']};
                  line-height: 1.3;
                }}

                .pack-tab span {{
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .pack-tab.active {{
                  background:
                    radial-gradient(circle at top right, var(--pack-tab-glow, rgba(156, 127, 102, 0.18)), transparent 42%),
                    linear-gradient(180deg, color-mix(in srgb, var(--pack-tab-surface, var(--surface)) 80%, white), color-mix(in srgb, var(--pack-tab-bg, var(--bg)) 78%, white));
                  border-color: var(--pack-tab-accent, var(--accent));
                  color: var(--ink-deep);
                  box-shadow: var(--shadow-medium);
                  transform: translateY(-2px);
                }}

                .pack-tab.active span {{
                  color: color-mix(in srgb, var(--pack-tab-accent, var(--accent)) 82%, #5f564c);
                }}

                .pack-grid {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                  margin-top: 20px;
                }}

                .artifact-grid {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                  margin-top: 20px;
                }}

                .artifact-card {{
                  --artifact-bg: rgba(255,255,255,0.8);
                  --artifact-surface: rgba(255,255,255,0.92);
                  --artifact-elevated: rgba(255,255,255,0.98);
                  --artifact-line: var(--line);
                  --artifact-accent: var(--accent);
                  --artifact-glow: rgba(156, 127, 102, 0.12);
                  position: relative;
                  overflow: hidden;
                  display: grid;
                  gap: 14px;
                  padding: 20px;
                  border-radius: 24px;
                  border: 1px solid var(--artifact-line);
                  background:
                    radial-gradient(circle at top right, var(--artifact-glow), transparent 38%),
                    linear-gradient(180deg, var(--artifact-elevated), var(--artifact-bg));
                  color: var(--ink);
                  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
                }}

                .artifact-card:hover {{
                  transform: translateY(-4px);
                  border-color: color-mix(in srgb, var(--artifact-accent) 40%, var(--artifact-line));
                  box-shadow: var(--shadow-medium);
                }}

                .artifact-card-type {{
                  display: inline-flex;
                  width: fit-content;
                  padding: 7px 12px;
                  border: 1px solid color-mix(in srgb, var(--artifact-accent) 18%, transparent);
                  border-radius: 999px;
                  color: var(--artifact-accent);
                  background: rgba(255, 255, 255, 0.72);
                  font-size: {typography['caption']['size']};
                }}

                .artifact-card-stage {{
                  display: grid;
                  gap: 8px;
                  min-height: 170px;
                  padding: 18px;
                  border-radius: 20px;
                  border: 1px solid color-mix(in srgb, var(--artifact-accent) 18%, var(--artifact-line));
                  background:
                    linear-gradient(180deg, color-mix(in srgb, var(--artifact-surface) 86%, white), color-mix(in srgb, var(--artifact-bg) 82%, white));
                }}

                .artifact-card-pack {{
                  display: inline-flex;
                  width: fit-content;
                  padding: 4px 9px;
                  border-radius: 999px;
                  background: rgba(255,255,255,0.76);
                  color: var(--artifact-accent);
                  font-size: 11px;
                  letter-spacing: 0.08em;
                  text-transform: uppercase;
                }}

                .artifact-card-stage h3 {{
                  margin: 0;
                  max-width: 11ch;
                  color: var(--ink-deep);
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_2']['size']};
                  line-height: {typography['heading_2']['line_height']};
                  letter-spacing: {typography['heading_2']['tracking']};
                }}

                .artifact-card-stage p {{
                  max-width: 24em;
                  color: #5b544d;
                  font-size: {typography['body_small']['size']};
                }}

                .artifact-card strong {{
                  color: var(--ink-deep);
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_3']['size']};
                  line-height: {typography['heading_3']['line_height']};
                }}

                .artifact-card-meta {{
                  display: grid;
                  gap: 6px;
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .artifact-card-modules {{
                  margin: 0;
                  padding-left: 18px;
                  display: grid;
                  gap: 6px;
                  color: #5f564c;
                  font-size: {typography['body_small']['size']};
                }}

                .artifact-card-link {{
                  display: inline-flex;
                  align-items: center;
                  width: fit-content;
                  margin-top: 4px;
                  color: var(--artifact-accent);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.08em;
                  text-transform: uppercase;
                }}

                .pack-card {{
                  position: relative;
                  overflow: hidden;
                  display: grid;
                  gap: 14px;
                  width: 100%;
                  padding: 20px;
                  border: 1px solid var(--pack-line, var(--line));
                  border-radius: 20px;
                  background:
                    radial-gradient(circle at top right, var(--pack-hero-glow, rgba(156, 127, 102, 0.12)), transparent 35%),
                    linear-gradient(180deg, var(--pack-elevated, rgba(255, 255, 255, 0.92)), var(--pack-background, rgba(255, 255, 255, 0.82)));
                  text-align: left;
                  cursor: pointer;
                  transition:
                    transform 180ms ease,
                    box-shadow 180ms ease,
                    border-color 180ms ease,
                    background 180ms ease;
                }}

                .pack-card:hover {{
                  transform: translateY(-2px);
                  box-shadow: var(--shadow-low);
                }}

                .pack-card.active {{
                  border-color: var(--pack-accent, var(--accent));
                  box-shadow: var(--shadow-medium);
                }}

                .pack-card::after {{
                  content: "";
                  position: absolute;
                  left: 20px;
                  right: 20px;
                  bottom: 0;
                  height: 1px;
                  background: linear-gradient(90deg, var(--pack-accent, var(--accent)), transparent);
                  opacity: 0.32;
                }}

                .pack-card-eyebrow {{
                  color: var(--pack-accent, var(--brand-asset));
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                  text-transform: uppercase;
                }}

                .pack-swatch-row {{
                  display: grid;
                  gap: 8px;
                  grid-template-columns: repeat(4, 1fr);
                }}

                .pack-swatch {{
                  height: 16px;
                  border-radius: 999px;
                }}

                .pack-card strong {{
                  color: var(--ink-deep);
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_3']['size']};
                  line-height: {typography['heading_3']['line_height']};
                }}

                .pack-card .pack-chip {{
                  border-color: var(--pack-line, var(--line));
                  background: var(--pack-chip-tint, rgba(255, 255, 255, 0.72));
                  color: #5f564c;
                }}

                .pack-card-meta {{
                  display: grid;
                  gap: 6px;
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .empty-state {{
                  margin-top: 16px;
                  padding: 18px;
                  border: 1px dashed var(--line);
                  border-radius: 18px;
                }}

                .pack-preview {{
                  position: relative;
                  overflow: hidden;
                  margin-top: 20px;
                  padding: 28px;
                  border-radius: 24px;
                  border: 1px solid var(--pack-line);
                  background:
                    radial-gradient(circle at top right, var(--pack-hero-glow), transparent 35%),
                    linear-gradient(135deg, var(--pack-elevated), var(--pack-background));
                  box-shadow: var(--shadow-medium);
                }}

                .preview-layout {{
                  position: relative;
                  z-index: 1;
                  display: grid;
                  gap: 20px;
                }}

                .preview-summary {{
                  color: #5d554d;
                  font-size: {typography['body_small']['size']};
                }}

                .preview-title {{
                  max-width: 12ch;
                  margin: 0;
                  color: var(--ink-deep);
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_1']['size']};
                  line-height: {typography['heading_1']['line_height']};
                  letter-spacing: {typography['heading_1']['tracking']};
                }}

                .preview-lead {{
                  max-width: 34em;
                  color: #413b35;
                }}

                .preview-overline,
                .preview-signature,
                .preview-rail-label {{
                  display: inline-flex;
                  align-items: center;
                  width: fit-content;
                  padding: 7px 12px;
                  border: 1px solid var(--pack-line);
                  border-radius: 999px;
                  color: var(--pack-accent);
                  background: rgba(255, 255, 255, 0.64);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                  text-transform: uppercase;
                }}

                .preview-chip-row {{
                  margin-top: 4px;
                }}

                .preview-actions {{
                  margin-top: 8px;
                }}

                .pack-preview .primary-button {{
                  background: var(--pack-accent);
                  color: #fff9f3;
                }}

                .pack-preview .secondary-button {{
                  border-color: var(--pack-line);
                }}

                .preview-chip,
                .preview-detail-chip {{
                  border-color: var(--pack-line);
                  background: var(--pack-chip-tint);
                  color: #585047;
                }}

                .preview-stat-pills {{
                  display: grid;
                  gap: 10px;
                  grid-template-columns: repeat(auto-fit, minmax(128px, 1fr));
                }}

                .preview-stat-pill,
                .preview-step-card,
                .preview-card {{
                  padding: 18px;
                  border-radius: 18px;
                  border: 1px solid var(--pack-line);
                  background: var(--pack-panel-tint);
                }}

                .preview-stat-pill {{
                  display: grid;
                  gap: 6px;
                }}

                .preview-stat-pill span,
                .preview-step-card span {{
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .preview-stat-pill strong,
                .preview-step-card strong,
                .preview-card strong {{
                  display: block;
                  color: var(--pack-accent);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                  text-transform: uppercase;
                }}

                .preview-card {{
                  display: grid;
                  gap: 10px;
                }}

                .preview-module-card,
                .module-recipe-card {{
                  display: grid;
                  gap: 8px;
                  padding: 16px;
                  border-radius: 18px;
                  border: 1px solid var(--pack-line);
                  background: color-mix(in srgb, var(--pack-panel-tint) 92%, white);
                }}

                .preview-module-card span,
                .module-recipe-card span {{
                  color: var(--pack-accent);
                  font-size: {typography['caption']['size']};
                  letter-spacing: 0.12em;
                }}

                .preview-module-card strong,
                .module-recipe-card strong {{
                  display: block;
                  color: var(--ink-deep);
                  font-size: {typography['body_small']['size']};
                  letter-spacing: 0;
                  text-transform: none;
                }}

                .preview-card-secondary,
                .preview-quote-line {{
                  color: #5f564c;
                  font-size: {typography['body_small']['size']};
                }}

                .preview-detail-list {{
                  display: flex;
                  flex-wrap: wrap;
                  gap: 10px;
                }}

                .preview-layout-gallery {{
                  grid-template-columns: minmax(0, 1.35fr) minmax(260px, 0.65fr);
                }}

                .preview-gallery-main,
                .preview-gallery-sidebar,
                .preview-editorial-main,
                .preview-analytical-head,
                .preview-story-header,
                .preview-consultation-main {{
                  display: grid;
                  gap: 16px;
                }}

                .preview-gallery-stage {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: minmax(0, 1.15fr) minmax(220px, 0.85fr);
                  align-items: stretch;
                }}

                .preview-gallery-art {{
                  display: grid;
                  gap: 16px;
                  min-height: 320px;
                  align-content: end;
                  padding: 24px;
                  border-radius: 24px;
                  border: 1px solid color-mix(in srgb, var(--pack-line) 82%, white);
                  background:
                    linear-gradient(180deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.58)),
                    linear-gradient(135deg, color-mix(in srgb, var(--pack-background) 92%, white), color-mix(in srgb, var(--pack-surface) 88%, white));
                }}

                .preview-gallery-sidebar {{
                  align-content: start;
                }}

                .preview-layout-editorial {{
                  grid-template-columns: 180px minmax(0, 1fr);
                  align-items: start;
                }}

                .preview-editorial-rail {{
                  display: grid;
                  gap: 16px;
                  padding: 20px 18px;
                  border-right: 1px solid var(--pack-line);
                }}

                .preview-section-number {{
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: clamp(44px, 5vw, 72px);
                  line-height: 0.92;
                  color: color-mix(in srgb, var(--pack-accent) 80%, white);
                }}

                .preview-editorial-columns {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(3, minmax(0, 1fr));
                }}

                .preview-layout-analytical {{
                  grid-template-columns: minmax(0, 0.92fr) minmax(0, 1.08fr);
                }}

                .preview-analytical-grid {{
                  display: grid;
                  gap: 14px;
                  grid-template-columns: repeat(2, minmax(0, 1fr));
                }}

                .preview-layout-luxury {{
                  gap: 24px;
                }}

                .preview-luxury-hero {{
                  display: grid;
                  justify-items: center;
                  gap: 14px;
                  padding: 12px 0 4px;
                  text-align: center;
                }}

                .preview-luxury-hero .preview-title,
                .preview-luxury-hero .preview-lead {{
                  max-width: 16ch;
                  text-align: center;
                }}

                .preview-luxury-band {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(3, minmax(0, 1fr));
                }}

                .preview-layout-storytelling {{
                  gap: 24px;
                }}

                .preview-story-grid {{
                  display: grid;
                  gap: 18px;
                  grid-template-columns: minmax(0, 1.1fr) minmax(280px, 0.9fr);
                  align-items: start;
                }}

                .preview-timeline {{
                  display: grid;
                  gap: 14px;
                }}

                .preview-timeline-item {{
                  display: grid;
                  gap: 14px;
                  grid-template-columns: 40px minmax(0, 1fr);
                  padding: 18px 0;
                  border-top: 1px solid var(--pack-line);
                }}

                .preview-timeline-item:first-child {{
                  border-top: none;
                  padding-top: 0;
                }}

                .preview-timeline-item span {{
                  display: inline-flex;
                  align-items: center;
                  justify-content: center;
                  width: 32px;
                  height: 32px;
                  border-radius: 999px;
                  border: 1px solid var(--pack-line);
                  color: var(--pack-accent);
                  font-size: {typography['caption']['size']};
                }}

                .preview-story-aside,
                .preview-consultation-aside {{
                  display: grid;
                  gap: 14px;
                }}

                .preview-layout-consultation {{
                  grid-template-columns: minmax(0, 1.08fr) minmax(280px, 0.92fr);
                }}

                .preview-process-steps {{
                  display: grid;
                  gap: 12px;
                  grid-template-columns: repeat(3, minmax(0, 1fr));
                }}

                .preview-step-card {{
                  display: grid;
                  gap: 8px;
                }}

                .preview-step-card span {{
                  color: var(--pack-accent);
                }}

                .pack-preview[data-variant="luxury"] .preview-chip-row,
                .pack-preview[data-variant="luxury"] .preview-actions {{
                  justify-content: center;
                }}

                .pack-preview[data-variant="consultation"] .preview-stat-pills {{
                  grid-template-columns: 1fr;
                }}

                .pack-preview[data-variant="analytical"] .preview-stat-pills {{
                  grid-template-columns: repeat(3, minmax(0, 1fr));
                }}

                .pack-preview[data-variant="storytelling"] .preview-actions,
                .pack-preview[data-variant="consultation"] .preview-actions {{
                  margin-top: 4px;
                }}

                .preview-meta-list {{
                  display: grid;
                  gap: 8px;
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .detail-grid {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                  margin-top: 20px;
                }}

                .detail-card {{
                  padding: 20px;
                  border-radius: 18px;
                  border: 1px solid var(--line);
                  background: rgba(255, 255, 255, 0.74);
                }}

                .detail-card-wide {{
                  grid-column: span 2;
                }}

                .detail-chip {{
                  border-color: rgba(0, 0, 0, 0.06);
                }}

                .module-recipe-list {{
                  display: grid;
                  gap: 12px;
                }}

                .swatch-grid,
                .type-grid,
                .example-grid {{
                  display: grid;
                  gap: 16px;
                  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                }}

                .swatch-card,
                .type-card,
                .example-card {{
                  padding: 20px;
                  border-radius: 18px;
                  border: 1px solid var(--line);
                  background: rgba(255, 255, 255, 0.74);
                }}

                .swatch {{
                  height: 90px;
                  border-radius: 14px;
                  border: 1px solid rgba(0, 0, 0, 0.06);
                  margin-bottom: 14px;
                }}

                .swatch-card strong,
                .type-card strong,
                .example-card strong {{
                  display: block;
                  margin-bottom: 6px;
                }}

                .swatch-card code,
                .neutral-row code {{
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .display-sample {{
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['display']['size']};
                  line-height: {typography['display']['line_height']};
                  letter-spacing: {typography['display']['tracking']};
                }}

                .h1-sample {{
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_1']['size']};
                  line-height: {typography['heading_1']['line_height']};
                  letter-spacing: {typography['heading_1']['tracking']};
                }}

                .h2-sample {{
                  font-family: "Swei Sugar", "Source Han Serif SC", serif;
                  font-size: {typography['heading_2']['size']};
                  line-height: {typography['heading_2']['line_height']};
                  letter-spacing: {typography['heading_2']['tracking']};
                }}

                .caption-sample,
                .footer-note {{
                  color: var(--muted);
                  font-size: {typography['caption']['size']};
                }}

                .panel-dark {{
                  background: var(--ink);
                  color: var(--bg);
                }}

                .panel-dark p,
                .panel-dark strong {{
                  color: var(--bg);
                }}

                .neutral-stack {{
                  display: grid;
                  gap: 10px;
                }}

                .neutral-row {{
                  display: grid;
                  grid-template-columns: 48px 1fr auto;
                  align-items: center;
                  gap: 12px;
                  color: var(--muted);
                }}

                .neutral-bar {{
                  height: 22px;
                  border-radius: 999px;
                  border: 1px solid rgba(0, 0, 0, 0.05);
                }}

                @media (max-width: 960px) {{
                  .hero-grid,
                  .preview-layout-gallery,
                  .preview-layout-editorial,
                  .preview-layout-analytical,
                  .preview-story-grid,
                  .preview-layout-consultation {{
                    grid-template-columns: 1fr;
                  }}

                  .preview-gallery-stage,
                  .preview-editorial-columns,
                  .preview-analytical-grid,
                  .preview-luxury-band,
                  .preview-process-steps {{
                    grid-template-columns: 1fr;
                  }}

                  .preview-editorial-rail {{
                    border-right: none;
                    border-bottom: 1px solid var(--pack-line);
                    padding-bottom: 18px;
                  }}

                  .detail-card-wide {{
                    grid-column: auto;
                  }}
                }}

                @media (max-width: 900px) {{
                  h1 {{
                    font-size: {typography['heading_1']['size']};
                    line-height: {typography['heading_1']['line_height']};
                    letter-spacing: {typography['heading_1']['tracking']};
                  }}

                  .preview-title {{
                    font-size: {typography['heading_2']['size']};
                    line-height: {typography['heading_2']['line_height']};
                  }}

                  .section-header {{
                    align-items: flex-start;
                    flex-direction: column;
                  }}

                  .section-kicker {{
                    text-align: left;
                  }}
                }}

                @media (max-width: 640px) {{
                  .shell {{
                    width: min(100vw - 24px, 100%);
                    padding-top: 16px;
                    padding-bottom: 64px;
                  }}

                  .hero,
                  .section,
                  .pack-preview {{
                    padding: 20px;
                    border-radius: 20px;
                  }}
                }}

                @media (prefers-reduced-motion: reduce) {{
                  * {{
                    scroll-behavior: auto;
                    transition-duration: 0.01ms !important;
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                  }}
                }}
              </style>
            </head>
            <body>
              <main class="shell">
                <section class="hero">
                  <div class="hero-meta">Brand Surface Preview · {html.escape(meta['version'])} · Generated from Foundation DNA</div>
                  <div class="hero-grid">
                    <div class="hero-copy">
                      <img class="brand-mark" src="assets/brand/liangqinjiamu-logo-horizontal.svg" alt="良禽佳木标志">
                      <h1>温润、克制、可信的中文高端家居界面</h1>
                      <p class="lead">{html.escape(dna['brand_principles']['anchor_sentence'])}</p>
                      <div class="chip-row">
                        <span class="chip">{html.escape(design_style['aesthetic']['genre'])}</span>
                        <span class="chip">{html.escape(design_style['interaction_feel']['feedback_style'])}</span>
                        <span class="chip">{html.escape(localization['tone_goal'])}</span>
                      </div>
                      <div class="button-row">
                        <button class="primary-button" type="button">预约咨询</button>
                        <button class="secondary-button" type="button">查看案例</button>
                      </div>
                    </div>
                    <aside class="hero-panel">
                      <strong>Brand Surface Preview</strong>
                      <p>{html.escape(design_style['aesthetic']['visual_metaphor'])}</p>
                      <p style="margin-top:12px;">先看最终成品，再回头看风格方向。这个首页现在只保留 3 个最能代表品牌落地方式的展示切口。</p>
                    </aside>
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Artifact Surfaces</h2>
                      <p>先看这套系统最终会长成什么样。这里优先展示网页、手机 H5 与图文报价体 3 个高价值成品入口。</p>
                    </div>
                    <p class="section-kicker">先看最终成品，再回头看风格方向，会比先读一堆系统说明更容易理解这套品牌系统。</p>
                  </div>
                  <div class="artifact-grid">
                    {artifact_cards}
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Style Directions</h2>
                      <p>这里不是另一套规范，而是 3 个最有代表性的品牌方向。它们帮助你快速判断同一品牌在展示、咨询和规格场景里的气质差异。</p>
                    </div>
                    <p class="section-kicker">保留少量代表方向，比把所有内部变量都摊开给人看更有效。</p>
                  </div>
                  <div class="pack-tabs-shell">
                    <div class="pack-tab-row" role="tablist" aria-label="Design pack styles">
                      {pack_tabs}
                    </div>
                    <div class="pack-tabs-note">切换这里时，重点看页面节奏、视觉重心和行动语气，而不只是换一层配色。</div>
                  </div>
                  <div class="section-header" style="margin-top:20px;">
                    <div>
                      <h2>当前风格方向</h2>
                      <p>这里看的是同一品牌下的不同落地气质，不是给 AI 读的内部规则说明。</p>
                    </div>
                    <p id="style-direction-note" class="section-kicker">当前方向是「{html.escape(default_pack['title'])}」，重点看版式气质、信息节奏和行动语气怎么变化。</p>
                  </div>
                  <div
                    id="pack-preview"
                    class="pack-preview"
                    style="{html.escape(render_pack_preview_style(default_pack))}"
                    aria-live="polite"
                    data-variant="{html.escape(default_pack['preview_variant'])}"
                  >{default_pack_payload['preview_markup']}</div>

                  <div class="detail-grid">
                    <article class="detail-card">
                      <strong>适合场景</strong>
                      <div id="pack-preview-pages" class="detail-chip-list">
                        {render_tag_list(default_pack['best_for_pages'], 'detail-chip')}
                      </div>
                    </article>
                    <article class="detail-card">
                      <strong>版式气质</strong>
                      <p id="pack-preview-layout">{html.escape(default_pack['layout_focus'])}</p>
                    </article>
                    <article class="detail-card">
                      <strong>行动语气</strong>
                      <p><span id="pack-preview-cta">{html.escape(default_pack['cta_tone'])}</span></p>
                    </article>
                    <article class="detail-card">
                      <strong>方向说明</strong>
                      <p id="pack-preview-notes">{html.escape(default_pack['notes'])}</p>
                    </article>
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Color Palette</h2>
                      <p>通用界面 CTA 使用 {html.escape(colors['accent']['hex'])}，品牌识别与 logo 资产使用 {html.escape(colors['brand_asset']['hex'])}。</p>
                    </div>
                  </div>
                  <div class="swatch-grid">
                    {''.join(swatches)}
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Typography</h2>
                      <p>标题由 Swei Sugar 驱动，正文、导航、按钮与表单由 OPPO Sans 4.0 驱动，先保证中文可读，再谈高级感。</p>
                    </div>
                  </div>
                  <div class="type-grid">
                    <article class="type-card">
                      <strong>Display</strong>
                      <div class="display-sample">营造慢慢观看的秩序感</div>
                    </article>
                    <article class="type-card">
                      <strong>Heading 1</strong>
                      <div class="h1-sample">让摄影与标题共同承担主重量</div>
                    </article>
                    <article class="type-card">
                      <strong>Heading 2</strong>
                      <div class="h2-sample">在留白里建立可信度</div>
                    </article>
                    <article class="type-card">
                      <strong>Body</strong>
                      <p>正文默认不少于 16px，并保持较宽松行高。按钮、标签、表单字段名称允许更完整的中文表达。</p>
                      <p class="caption-sample" style="margin-top:12px;">Caption / 元信息 / 说明文字</p>
                    </article>
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Components & Hierarchy</h2>
                      <p>按钮、导航、表单、卡片都必须让位于内容、摄影与材质表达，不滑向促销卡或电商页节奏。</p>
                    </div>
                  </div>
                  <div class="example-grid">
                    <article class="example-card">
                      <strong>Button System</strong>
                      <p>{html.escape(components['button_style'])}</p>
                    </article>
                    <article class="example-card">
                      <strong>Card Surface</strong>
                      <p>{html.escape(components['card_style'])}</p>
                    </article>
                    <article class="example-card panel-dark">
                      <strong>Navigation Tone</strong>
                      <p>{html.escape(components['navigation_pattern'])}</p>
                    </article>
                  </div>
                </section>

                <section class="section">
                  <div class="section-header">
                    <div>
                      <h2>Neutral Scale</h2>
                      <p>主中性色阶用于建立稳定的层次、边界和大面积呼吸感，而不是用鲜艳色彩制造刺激。</p>
                    </div>
                  </div>
                  <div class="neutral-stack">
                    {''.join(neutral_scale)}
                  </div>
                  <p class="footer-note">Spacing scale: {html.escape(', '.join(spacing['scale']))} · Motion philosophy: {html.escape(dna['design_system']['motion']['philosophy'])}</p>
                </section>
              </main>
              {script}
            </body>
            </html>
            """
        ).strip()
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 Foundation DNA 导出 DESIGN.md、治理说明和静态设计预览页"
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT),
        help="输出目录，默认写入仓库根目录",
    )
    args = parser.parse_args()

    output_root = Path(args.output_dir).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    dna = json.loads(DNA_PATH.read_text(encoding="utf-8"))
    packs = load_design_packs()
    pack_map = {pack["slug"]: pack for pack in packs}
    artifact_surfaces = load_artifact_surfaces(set(pack_map))
    design_md = generate_design_md(dna)
    governance_md = generate_design_governance_md(dna)
    preview_html = generate_preview_html(dna, packs, artifact_surfaces)

    (output_root / "DESIGN.md").write_text(design_md, encoding="utf-8")
    (output_root / "DESIGN-GOVERNANCE.md").write_text(governance_md, encoding="utf-8")
    (output_root / "design-preview.html").write_text(preview_html, encoding="utf-8")
    (output_root / "index.html").write_text(preview_html, encoding="utf-8")
    for surface in artifact_surfaces:
        artifact_html = render_artifact_surface_page(
            dna,
            surface,
            pack_map[surface["source_pack"]],
        )
        artifact_path = output_root / f"artifact-{surface['slug']}.html"
        artifact_path.write_text(artifact_html, encoding="utf-8")

    print(
        "exported DESIGN.md, DESIGN-GOVERNANCE.md, design-preview.html, index.html, and "
        f"{len(artifact_surfaces)} artifact pages to {output_root} with {len(packs)} design packs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
