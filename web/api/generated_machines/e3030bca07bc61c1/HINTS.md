# Exploitation Hints

**Machine ID:** `e3030bca07bc61c1`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: bash
3. Command structure: redirection_chain
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline
7. 💡 Bash features available: process substitution, brace expansion

## Flag

`HACKFORGE{6c9812be9951285cd890ed5486fdc17d}`
