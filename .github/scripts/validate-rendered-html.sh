#!/usr/bin/env bash

set -euo pipefail

task_tmp_dir=$(mktemp -d)
trap 'rm -rf "$task_tmp_dir"' EXIT

task_script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
table_count=0

while IFS= read -r -d '' task_markdown_file; do
  if ! grep -q '<table[ >]' "$task_markdown_file"; then
    continue
  fi

  table_count=$((table_count + 1))
  task_rendered_file="$task_tmp_dir/rendered-$table_count.html"

  {
    printf '%s\n' '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Rendered Markdown</title></head><body>'
    npx --yes marked@18.0.9 "$task_markdown_file"
    printf '%s\n' '</body></html>'
  } > "$task_rendered_file"

  echo "Validating rendered HTML from $task_markdown_file"
  # GitHub supports these legacy attributes but strips author CSS. Exempt
  # only our approved values on table cells, in a temporary validation copy.
  # Published HTML is unchanged; every other Tidy diagnostic still fails.
  python3 "$task_script_dir/prepare-html-validation.py" "$task_rendered_file"
  tidy -errors -quiet -utf8 "$task_rendered_file" > /dev/null
done < <(find . -name '*.md' -not -path './.git/*' -print0)

if (( table_count == 0 )); then
  echo "No Markdown files with raw HTML tables found."
else
  echo "Validated $table_count Markdown file(s) with raw HTML tables."
fi
