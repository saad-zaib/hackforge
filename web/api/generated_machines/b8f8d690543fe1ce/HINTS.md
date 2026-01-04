# Exploitation Hints

**Machine ID:** `b8f8d690543fe1ce`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: sh
3. Command structure: single_command
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{697337dff51139e13a4dd20c14e7b205}`
