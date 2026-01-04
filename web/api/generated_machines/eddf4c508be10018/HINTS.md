# Exploitation Hints

**Machine ID:** `eddf4c508be10018`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: ping_utility
2. Shell: dash
3. Command structure: command_grouping
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{ccc6259340cfd2466ace7190a94d1852}`
