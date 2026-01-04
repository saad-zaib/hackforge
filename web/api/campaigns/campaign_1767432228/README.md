# Hackforge Campaign: campaign_1767432228

Generated: 2026-01-03 14:23:48
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `993d6c62cc61d84c`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{ce5deb56bff48249cf22d0e886b8abe7}`

**Exploitation Hints**:
- Context: export_tool
- Shell: sh
- Command structure: piped_commands
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `0189c0a526033fe8`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{6e2282fc1bf49ad90800413658383e79}`

**Exploitation Hints**:
- Access control: predictable_token
- Resource ID type: uuid_v4
- Authentication: api_key
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
