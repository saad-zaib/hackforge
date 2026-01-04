# Exploitation Hints

**Machine ID:** `f7f456de4b789e55`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: search_function
2. Shell: zsh
3. Command structure: redirection_chain
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{3fee2c7bf40b64d3e7154cccfd9b2acd}`
