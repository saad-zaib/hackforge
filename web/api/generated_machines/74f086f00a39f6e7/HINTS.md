# Exploitation Hints

**Machine ID:** `74f086f00a39f6e7`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: export_tool
2. Shell: zsh
3. Command structure: redirection_chain
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{8fddc2ff2250c92f9a074c348d8cb192}`
