# Hackforge Campaign: campaign_1767361155

Generated: 2026-01-02 18:39:15
Total Machines: 2

## Machines Overview

### Machine 1: Command Injection
- **Machine ID**: `e3030bca07bc61c1`
- **Category**: inj_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{6c9812be9951285cd890ed5486fdc17d}`

**Exploitation Hints**:
- Context: login_form
- Shell: bash
- Command structure: redirection_chain
- ⚠️ Filters: space, semicolon
- 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
- 💡 Bypass semicolon: Use && or || or newline
- 💡 Bash features available: process substitution, brace expansion

---

### Machine 2: IDOR (Insecure Direct Object Reference)
- **Machine ID**: `3b0ca8f036a46139`
- **Category**: bac_001
- **Difficulty**: 2/5
- **Flag**: `HACKFORGE{17fa12cf89e25fa2fb3be347869416d1}`

**Exploitation Hints**:
- Access control: client_side_only
- Resource ID type: base64_encoded
- Authentication: basic_auth
- ⚠️ Access checks are client-side only
- 💡 IDs are base64 encoded - try decoding and modifying

---


## How to Use

Each machine directory contains:
- `config.json` - Complete machine configuration
- `flag.txt` - The flag to capture
- `hints.txt` - Exploitation hints

Use the template engine (Component 2) to generate actual vulnerable applications from these configs.
