# Exploitation Hints

**Machine ID:** `78988e9c80bf4645`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: log_analyzer
2. Shell: dash
3. Command structure: single_command
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{bb995167b40a237c886254a4473b354c}`
