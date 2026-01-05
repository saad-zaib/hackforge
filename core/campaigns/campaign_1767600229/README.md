# Hackforge Campaign: campaign_1767600229

Generated: 2026-01-05 13:03:49
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `ff77d2a629131a1b`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{af75050b7fe3257787d008a4acb479c0}`

**Exploitation Hints**:
- Context: login_form
- Shell: zsh
- Command structure: piped_commands
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `d0c890e41e738bef`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{c6f8f4983a8f099e325589140eb94f34}`

**Exploitation Hints**:
- Access control: timing_vulnerable
- Resource ID type: base64_encoded
- Authentication: basic_auth
- 💡 IDs are base64 encoded - try decoding and modifying

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
