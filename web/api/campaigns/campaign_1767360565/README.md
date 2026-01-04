# Hackforge Campaign: campaign_1767360565

Generated: 2026-01-02 18:29:25
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `0df2ca73e33eb636`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{4e32d6f27c55bb3a1847cd725a475151}`

**Exploitation Hints**:
- Context: file_processor
- Shell: dash
- Command structure: piped_commands
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `e4f2298a21fe321f`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{4b3b78ce98f869f8a9dd6317556ae19c}`

**Exploitation Hints**:
- Access control: timing_vulnerable
- Resource ID type: predictable_pattern
- Authentication: session_cookie

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
