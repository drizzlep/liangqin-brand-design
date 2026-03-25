#!/bin/zsh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_SOURCE_DIR="$PROJECT_DIR/skill/liangqin-brand-design"

if [[ -n "${SOURCE_DIR:-}" ]]; then
  SOURCE_DIR="$SOURCE_DIR"
elif [[ -d "$REPO_SOURCE_DIR" ]]; then
  SOURCE_DIR="$REPO_SOURCE_DIR"
else
  SOURCE_DIR="$HOME/.openclaw/skills/liangqin-brand-design"
fi

OUTPUT_DIR="${1:-$PROJECT_DIR/dist}"
PACKAGE_DATE="$(date +%Y%m%d)"
PACKAGE_NAME="liangqin-brand-design-openclaw-${PACKAGE_DATE}.zip"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "未找到 skill 目录：$SOURCE_DIR" >&2
  exit 1
fi

for required_file in \
  "$SOURCE_DIR/SKILL.md" \
  "$SOURCE_DIR/README.md" \
  "$SOURCE_DIR/scripts/publish_skill.py" \
  "$SOURCE_DIR/scripts/refresh_and_test.py"; do
  if [[ ! -f "$required_file" ]]; then
    echo "缺少必要文件：$required_file" >&2
    exit 1
  fi
done

STAGING_ROOT="$(mktemp -d)"
trap 'rm -rf "$STAGING_ROOT"' EXIT

PACKAGE_ROOT="$STAGING_ROOT/liangqin-brand-design"
mkdir -p "$PACKAGE_ROOT" "$OUTPUT_DIR"

cp "$SOURCE_DIR/SKILL.md" "$PACKAGE_ROOT/SKILL.md"
cp "$SOURCE_DIR/README.md" "$PACKAGE_ROOT/README.md"
cp -R "$SOURCE_DIR/references" "$PACKAGE_ROOT/references"
cp -R "$SOURCE_DIR/scripts" "$PACKAGE_ROOT/scripts"

find "$PACKAGE_ROOT" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$PACKAGE_ROOT" -type f \( -name "*.pyc" -o -name ".DS_Store" \) -delete

ZIP_PATH="$OUTPUT_DIR/$PACKAGE_NAME"
rm -f "$ZIP_PATH"

if command -v zip >/dev/null 2>&1; then
  (cd "$STAGING_ROOT" && zip -qr "$ZIP_PATH" liangqin-brand-design)
elif command -v ditto >/dev/null 2>&1; then
  (cd "$STAGING_ROOT" && ditto -c -k --sequesterRsrc --keepParent liangqin-brand-design "$ZIP_PATH")
else
  echo "系统缺少 zip 或 ditto，无法生成压缩包。" >&2
  exit 1
fi

echo "打包完成：$ZIP_PATH"
