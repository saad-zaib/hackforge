# Hackforge Campaign: campaign_1767360566

Generated: 2026-01-02 18:29:26
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `e556ba1d41478934`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{4ef718a0853161d1e6e3196062196275}`

**Exploitation Hints**:
- Context: export_tool
- Shell: sh
- Command structure: command_substitution
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `200f5b3a856248b6`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{40f14f5bc414a571d60d203768935a43}`

**Exploitation Hints**:
- Context: document_management
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/data/all
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
