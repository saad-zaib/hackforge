# Exploitation Hints

**Machine ID:** `7898514abe3f6988`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: zsh
3. Command structure: backgrounded_process
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{80d0ebc26d58e1029b6e15cb6f7d1328}`
