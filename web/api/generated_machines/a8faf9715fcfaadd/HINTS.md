# Exploitation Hints

**Machine ID:** `a8faf9715fcfaadd`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: sh
3. Command structure: redirection_chain
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{bc52da6cee443806aee8e40e18e8f254}`
