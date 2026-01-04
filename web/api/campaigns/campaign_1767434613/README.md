# Hackforge Campaign: campaign_1767434613

Generated: 2026-01-03 15:03:33
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `ddd66645e72efb21`
- **Category**: inj_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{7246bd9f2601cbfeb9cbd5203330be6a}`

**Exploitation Hints**:
- Context: ping_utility
- Shell: sh
- Command structure: piped_commands
- ✓ No filtering - direct command injection possible
- 💡 Try: ; cat /flag.txt

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `ffb4bbd15ac7a56c`
- **Category**: bac_001
- **Difficulty**: 1/5
- **Flag**: `HACKFORGE{beec54351c6950c2835d66835f2514e0}`

**Exploitation Hints**:
- Access control: timing_vulnerable
- Resource ID type: predictable_pattern
- Authentication: basic_auth

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
