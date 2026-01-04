# Exploitation Hints

**Machine ID:** `7e7ced290b1eddb4`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: export_tool
2. Shell: dash
3. Command structure: command_substitution
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{1d5a1cc803e799abb93648d1dfe9a212}`
