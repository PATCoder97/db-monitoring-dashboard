#!/bin/bash

# PRD Parse - Convert PRD to Epic

if [ -z "$1" ]; then
    echo "❌ Usage: pm prd-parse <feature-name>"
    echo ""
    echo "Example: pm prd-parse user-authentication"
    exit 1
fi

FEATURE_NAME="$1"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PRD_DIR="$REPO_ROOT/ccpm/prds"
EPICS_DIR="$REPO_ROOT/ccpm/epics"
PRD_FILE="$PRD_DIR/${FEATURE_NAME}.md"
EPIC_FILE="$EPICS_DIR/${FEATURE_NAME}.md"

# Check if PRD exists
if [ ! -f "$PRD_FILE" ]; then
    echo "❌ PRD not found: $PRD_FILE"
    echo ""
    echo "Create with: pm prd-new $FEATURE_NAME"
    exit 1
fi

mkdir -p "$EPICS_DIR"

# Check if epic already exists
if [ -f "$EPIC_FILE" ]; then
    echo "⚠️  Epic already exists: $EPIC_FILE"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🔄 Parsing PRD: $FEATURE_NAME"
echo ""

# Extract key info from PRD
FEATURE_TITLE=$(grep -m 1 "^# " "$PRD_FILE" | sed 's/^# //')
STATUS=$(grep "^**Status**:" "$PRD_FILE" | head -1 | cut -d: -f2- | xargs)

# Create Epic from PRD
cat > "$EPIC_FILE" << EOF
# Epic: $FEATURE_NAME

**Status**: Ready for Decomposition
**Source**: [PRD: $FEATURE_NAME]($PRD_FILE)
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

---

## Overview

_From PRD_: $(grep -A2 "^## 1. Overview" "$PRD_FILE" | tail -1)

---

## Goals

- [ ] Extract and verify goals from PRD
- [ ] Define technical breakdown
- [ ] Create task decomposition

---

## Tasks

### Phase 1: Setup & Planning
- [ ] Task 1.1: Analysis
- [ ] Task 1.2: Design
- [ ] Task 1.3: Planning

### Phase 2: Implementation
- [ ] Task 2.1: Core feature
- [ ] Task 2.2: Integration
- [ ] Task 2.3: Testing

### Phase 3: QA & Deployment
- [ ] Task 3.1: QA
- [ ] Task 3.2: Documentation
- [ ] Task 3.3: Deployment

---

## Decomposed Issues

_Will be populated after epic-decompose_

---

## Progress

0% Complete

---

## Related PRD

See [PRD: $FEATURE_NAME]($PRD_FILE) for full requirements.
EOF

echo "✅ Epic created: $EPIC_FILE"
echo ""
echo "📚 Next steps:"
echo "  1. Edit epic: pm epic-edit $FEATURE_NAME"
echo "  2. Decompose: pm epic-decompose $FEATURE_NAME"
echo "  3. Sync to GitHub: pm epic-sync $FEATURE_NAME"
echo ""
echo "📖 Or do all at once: pm epic-oneshot $FEATURE_NAME"
