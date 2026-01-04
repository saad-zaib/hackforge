# Hackforge Campaign: campaign_1767361602

Generated: 2026-01-02 18:46:42
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `61c36deb608d67b2`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{fe7624e28830430ca32b163216f3e37e}`

**Exploitation Hints**:
- Context: export_tool
- Shell: zsh
- Command structure: command_grouping
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `8d3ad14b1b1469b3`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{c01bad5849f203c567b9dcdb7d655650}`

**Exploitation Hints**:
- Access control: none
- Resource ID type: uuid_v4
- Authentication: jwt_token
- ✓ No access control - direct ID manipulation possible
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
