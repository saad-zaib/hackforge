# Hackforge Campaign: campaign_1767431901

Generated: 2026-01-03 14:18:21
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `fe6a9a32543174f8`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{41a27876219c01203187b76c1779f8c8}`

**Exploitation Hints**:
- Context: login_form
- Shell: bash
- Command structure: single_command
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline
- 💡 Bash features available: process substitution, brace expansion

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `be4fe66fd860d0d1`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{2e7521d0e1b081bed9136b393c3abd78}`

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
