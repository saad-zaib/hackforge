# Exploitation Hints

**Machine ID:** `0df2ca73e33eb636`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: file_processor
2. Shell: dash
3. Command structure: piped_commands
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{4e32d6f27c55bb3a1847cd725a475151}`
