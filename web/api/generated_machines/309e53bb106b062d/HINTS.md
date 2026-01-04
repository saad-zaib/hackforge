# Exploitation Hints

**Machine ID:** `309e53bb106b062d`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: file_processor
2. Shell: sh
3. Command structure: backgrounded_process
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{37db93fa106a3fee43daa0b5a6bc0204}`
