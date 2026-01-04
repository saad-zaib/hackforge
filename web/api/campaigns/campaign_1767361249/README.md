# Hackforge Campaign: campaign_1767361249

Generated: 2026-01-02 18:40:49
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `d71f2e7025560228`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{7a99b2fea29b22eca8103ffd4a038c5d}`

**Exploitation Hints**:
- Context: log_analyzer
- Shell: dash
- Command structure: command_substitution
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `3ef5c9b9e6aeba91`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{fad731babde257e385ae6a12730130c6}`

**Exploitation Hints**:
- Access control: none
- Resource ID type: uuid_v4
- Authentication: none
- ✓ No access control - direct ID manipulation possible
- 💡 UUIDs are used but might be predictable or leaked

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
