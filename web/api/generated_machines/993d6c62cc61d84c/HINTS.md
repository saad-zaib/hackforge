# Exploitation Hints

**Machine ID:** `993d6c62cc61d84c`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: export_tool
2. Shell: sh
3. Command structure: piped_commands
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{ce5deb56bff48249cf22d0e886b8abe7}`
