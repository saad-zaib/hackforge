# Exploitation Hints

**Machine ID:** `ff77d2a629131a1b`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: login_form
2. Shell: zsh
3. Command structure: piped_commands
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{af75050b7fe3257787d008a4acb479c0}`
