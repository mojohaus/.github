#!/usr/bin/env bash
# Guard-railed verification for a small, behaviour-preserving change in a
# MojoHaus Maven repository. Run from the repository root on a working branch.
#
#   # before editing:
#   scripts/sweep-verify.sh --record-baseline ExecMojoTest
#   # -> prints a baseline file path, e.g. /tmp/sweep-baseline-ExecMojoTest.txt
#
#   # after editing, with that path:
#   scripts/sweep-verify.sh --test-class ExecMojoTest \
#       --baseline /tmp/sweep-baseline-ExecMojoTest.txt
#
# It never resets, checks out or discards files: a dirty tree is a hard stop.
# The second mode applies spotless, runs the tests and refuses to continue if
# the per-class surefire counts changed.
set -euo pipefail

# Use the caller's JAVA_HOME; without one, derive it from the java on the PATH.
if [ -z "${JAVA_HOME:-}" ]; then
  if ! command -v java >/dev/null 2>&1; then
    echo "JAVA_HOME is not set and no java was found on the PATH" >&2
    exit 2
  fi
  JAVA_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")"
fi
export JAVA_HOME
MODE=""
TEST_CLASS=""
BASELINE=""

usage() {
  echo "usage: $0 --record-baseline <Class> | --test-class <Class> --baseline <file>" >&2
  exit 2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --record-baseline) [ $# -ge 2 ] || usage; MODE=record; TEST_CLASS="$2"; shift 2 ;;
    --test-class)      [ $# -ge 2 ] || usage; MODE=compare; TEST_CLASS="$2"; shift 2 ;;
    --baseline)        [ $# -ge 2 ] || usage; BASELINE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown argument: $1" >&2; usage ;;
  esac
done

[ -n "$TEST_CLASS" ] || usage
if [ "$MODE" = compare ] && [ -z "$BASELINE" ]; then
  echo "--baseline is required with --test-class" >&2
  exit 2
fi

# 1. Never overwrite work in progress.
if [ -n "$(git status --porcelain)" ]; then
  echo "STOP: working tree is dirty. Commit or stash your work first." >&2
  git status --short >&2
  exit 1
fi
echo "==> tree clean, HEAD $(git rev-parse --short HEAD)"

counts() {
  grep -ho 'tests="[0-9]*" errors="[0-9]*" skipped="[0-9]*" failures="[0-9]*"' \
    target/surefire-reports/TEST-*"$TEST_CLASS"*.xml | sort
}

if [ "$MODE" = record ]; then
  mvn -B -o test -Dtest="$TEST_CLASS" >/dev/null
  out="/tmp/sweep-baseline-${TEST_CLASS}.txt"
  counts > "$out"
  echo "==> baseline for $TEST_CLASS written to $out"
  echo "==> $(cat "$out")"
  exit 0
fi

[ -f "$BASELINE" ] || { echo "baseline file not found: $BASELINE" >&2; exit 1; }

# 2. Formatter: apply first, then verify. Re-stage only tracked files.
mvn -B -o spotless:apply
mvn -B -o -Dspotless.action=check spotless:check
git add -u

# 3. Unit tests.
mvn -B -o test

# 4. Compare test counts. A dropped case is a failure, not a detail.
after=$(mktemp)
counts > "$after"
if ! diff -u "$BASELINE" "$after"; then
  echo "STOP: surefire counts changed for $TEST_CLASS" >&2
  exit 1
fi
echo "==> test counts unchanged: $(cat "$after")"
echo "==> verification complete; review 'git diff --cached' before committing"
