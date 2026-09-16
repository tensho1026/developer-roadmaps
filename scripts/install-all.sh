#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD="${PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD:-1}"
export CYPRESS_INSTALL_BINARY="${CYPRESS_INSTALL_BINARY:-0}"

fail=0

install_npm() {
  local dir="$1"
  echo "==> npm install $dir"
  if ! (cd "$dir" && npm install --no-fund --no-audit); then
    echo "!! failed npm install $dir"
    fail=1
  fi
}

while IFS= read -r pkg; do
  install_npm "$(dirname "$pkg")"
done < <(find front back fullstack -name package.json -not -path '*/node_modules/*' | sort)

if [[ -f back/prisma/.env.example && ! -f back/prisma/.env ]]; then
  cp back/prisma/.env.example back/prisma/.env
fi

if [[ -f back/python/pyproject.toml ]]; then
  echo "==> uv sync back/python"
  (cd back/python && uv sync) || fail=1
fi

if [[ -f back/php/composer.json ]]; then
  echo "==> composer install back/php"
  (cd back/php && composer install --no-interaction) || fail=1
fi

if [[ -f back/ruby/Gemfile ]]; then
  echo "==> bundle install back/ruby"
  (cd back/ruby && bundle install) || echo "ruby gems skipped (optional; Webrick app still runs)"
fi

if [[ -f back/go/go.mod ]]; then
  echo "==> go mod tidy back/go"
  (cd back/go && go mod tidy) || fail=1
fi

if [[ -f ios/Package.swift ]]; then
  echo "==> swift package resolve ios"
  (cd ios && swift package resolve) || fail=1
fi

echo "install-all finished (fail=$fail)"
exit "$fail"
