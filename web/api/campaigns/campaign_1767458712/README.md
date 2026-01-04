# Hackforge Campaign: campaign_1767458712

Generated: 2026-01-03 21:45:12
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `13c0c424cf469df0`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{642d4488744c3167ea9cf7b1a4ab1430}`

**Exploitation Hints**:
- Context: whois_lookup
- Shell: dash
- Command structure: command_substitution
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `056b7a4a4de8c9ba`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{8125b0133213cbfa5ade22cef5db7e65}`

**Exploitation Hints**:
- Access control: none
- Resource ID type: predictable_pattern
- Authentication: none
- ✓ No access control - direct ID manipulation possible

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
