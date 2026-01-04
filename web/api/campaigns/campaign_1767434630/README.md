# Hackforge Campaign: campaign_1767434630

Generated: 2026-01-03 15:03:50
Total Machines: 2

## Machines Overview

### Machine 1: Template Injection
- **Machine ID**: `16af3891341e705a`
- **Category**: inj_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{b57c0c2bf6afcd8328c3595d1bee059f}`

**Exploitation Hints**:
- Template engine: freemarker
- Report generation with user input
- 💡 Try template injection syntax

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `90b8f67ccc3016cc`
- **Category**: bac_001
- **Difficulty**: 3/5
- **Flag**: `HACKFORGE{85acd837b3f3faaa8e6ab6a1fb594517}`

**Exploitation Hints**:
- Access control: weak_session_check
- Resource ID type: predictable_pattern
- Authentication: basic_auth
- ⚠️ Session validation is weak

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
