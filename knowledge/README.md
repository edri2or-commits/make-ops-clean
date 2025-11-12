# Knowledge Base

**Purpose**: Central repository for system patterns, specifications, and operational knowledge

---

## Contents

### Specifications
- **PROOF_PACK_SPEC.json** - Schema for evidence documentation
- Structure for API proof packs
- Required fields, validation rules

### Terminology
- **GLOSSARY.md** - Key terms and definitions
- SSOT, Proof Pack, Anchors, DoD, Canary, Idempotency
- Integration terms (MCP, WIF, Webhooks)

### Operations
- **OPERATING_MODES.md** - System operating levels
- L1 (Read-Only), L2 (Controlled-Write), L3 (Automations)
- Mode transitions, DoD criteria, enforcement

---

## Usage

### For New Team Members
1. Read GLOSSARY.md first
2. Understand OPERATING_MODES.md
3. Review PROOF_PACK_SPEC.json for evidence format

### For Operations
- Check current operating mode
- Follow DoD checklists
- Generate proof packs per spec
- Update DECISION_LOG.md for transitions

### For Development
- Use PROOF_PACK_SPEC.json for evidence generation
- Follow mode restrictions
- Document patterns here

---

## Adding New Knowledge

1. **Create markdown file** with clear title
2. **Add to this README** in relevant section
3. **Link from other docs** where referenced
4. **Update GLOSSARY.md** if new terms introduced

---

**Created**: 2025-11-12  
**Branch**: unified/desktop-merge  
**Maintained by**: Claude & GPT
