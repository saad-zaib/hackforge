# Hackforge Campaign: campaign_1767286613

Generated: 2026-01-01 21:56:53
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `7e7ced290b1eddb4`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{1d5a1cc803e799abb93648d1dfe9a212}`

**Exploitation Hints**:
- Context: export_tool
- Shell: dash
- Command structure: command_substitution
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: Missing Function Level Access Control
- **Machine ID**: `6836d7fe7ca243ae`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{ed059b5889183512a4299c6100791c86}`

**Exploitation Hints**:
- Context: document_management
- Regular user has limited access
- 💡 Admin functions might not check authorization properly
- Try accessing: /api/admin/export
- ⚠️ Some endpoints may not validate user role

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
