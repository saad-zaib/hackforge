# Exploitation Hints

**Machine ID:** `61c36deb608d67b2`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: export_tool
2. Shell: zsh
3. Command structure: command_grouping
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{fe7624e28830430ca32b163216f3e37e}`
