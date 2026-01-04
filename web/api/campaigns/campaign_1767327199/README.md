# Hackforge Campaign: campaign_1767327199

Generated: 2026-01-02 09:13:19
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `2fd4eb88b5be65a8`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{937422ea6068b49b4f7da093e9d59a84}`

**Exploitation Hints**:
- Context: report_generator
- Shell: zsh
- Command structure: piped_commands
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `9173430f4deaeb86`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{dbe3b97ee3b7fbb8b5536cc298bdbb81}`

**Exploitation Hints**:
- Access control: weak_session_check
- Resource ID type: predictable_pattern
- Authentication: session_cookie
- ⚠️ Session validation is weak

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
