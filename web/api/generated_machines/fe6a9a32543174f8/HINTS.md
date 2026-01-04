# Exploitation Hints

**Machine ID:** `fe6a9a32543174f8`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: bash
3. Command structure: single_command
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline
7. 💡 Bash features available: process substitution, brace expansion

## Flag

`HACKFORGE{41a27876219c01203187b76c1779f8c8}`
