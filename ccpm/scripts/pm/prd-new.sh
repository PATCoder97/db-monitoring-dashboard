#!/bin/bash

# PRD New - Create a new Product Requirements Document

if [ -z "$1" ]; then
    echo "❌ Usage: pm prd-new <feature-name>"
    echo ""
    echo "Example: pm prd-new user-authentication"
    exit 1
fi

FEATURE_NAME="$1"
PRD_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)/ccpm/prds"
PRD_FILE="$PRD_DIR/${FEATURE_NAME}.md"

# Create directory if it doesn't exist
mkdir -p "$PRD_DIR"

# Check if PRD already exists
if [ -f "$PRD_FILE" ]; then
    echo "❌ PRD already exists: $PRD_FILE"
    echo ""
    echo "Edit with: pm prd-edit $FEATURE_NAME"
    exit 1
fi

# Create PRD template
cat > "$PRD_FILE" << 'EOF'
# Product Requirements Document (PRD)

**Feature**: {{FEATURE_NAME}}
**Status**: Draft
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Updated**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

---

## 1. Overview

### Problem Statement
_What problem does this feature solve?_

### Goals
_What are the primary goals?_

- Goal 1
- Goal 2
- Goal 3

### Success Metrics
_How will we measure success?_

- Metric 1: Definition
- Metric 2: Definition

---

## 2. Requirements

### Functional Requirements
_What must the system do?_

- Requirement 1
- Requirement 2
- Requirement 3

### Non-Functional Requirements
_Performance, security, scalability, etc._

- Requirement 1
- Requirement 2

---

## 3. User Stories

### Story 1
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3

### Story 2
_Continue with more stories..._

---

## 4. Technical Considerations

### Architecture
_Technical approach and architecture decisions_

### Technology Stack
_Tools, frameworks, libraries to use_

### Integration Points
_How does this integrate with existing systems?_

---

## 5. Timeline & Resources

### Estimated Effort
_Hours/days needed_

### Dependencies
_What needs to happen first?_

### Risks
_What could go wrong?_

---

## 6. Open Questions

- Question 1?
- Question 2?
- Question 3?

---

## Notes

_Any additional notes or context_
EOF

# Replace placeholder
sed -i "s|{{FEATURE_NAME}}|$FEATURE_NAME|g" "$PRD_FILE"

echo "✅ PRD created: $PRD_FILE"
echo ""
echo "📝 Next steps:"
echo "  1. Edit: pm prd-edit $FEATURE_NAME"
echo "  2. Parse: pm prd-parse $FEATURE_NAME"
echo "  3. View: pm prd-list"
