# Exploitation Hints

**Machine ID:** `e556ba1d41478934`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: export_tool
2. Shell: sh
3. Command structure: command_substitution
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{4ef718a0853161d1e6e3196062196275}`
