# Hackforge Campaign: campaign_1766983915

Generated: 2025-12-29 09:51:55
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `7898514abe3f6988`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{80d0ebc26d58e1029b6e15cb6f7d1328}`

**Exploitation Hints**:
- Context: login_form
- Shell: zsh
- Command structure: backgrounded_process
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `a482f0c52af84feb`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{b12e4c0b801b24eeb45bdb869f66204d}`

**Exploitation Hints**:
- Access control: client_side_only
- Resource ID type: uuid_v4
- Authentication: jwt_token
- ⚠️ Access checks are client-side only
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
