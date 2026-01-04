# Exploitation Hints

**Machine ID:** `963e7614f1ace7b6`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: ping_utility
2. Shell: zsh
3. Command structure: redirection_chain
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{c368f300cf1c4f16a2259c953238f946}`
