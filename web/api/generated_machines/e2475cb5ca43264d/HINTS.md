# Exploitation Hints

**Machine ID:** `e2475cb5ca43264d`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: file_processor
2. Shell: zsh
3. Command structure: backgrounded_process
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{00e0f5f666f57387dbf05434b8d01e3c}`
