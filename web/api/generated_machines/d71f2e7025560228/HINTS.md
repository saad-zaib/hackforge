# Exploitation Hints

**Machine ID:** `d71f2e7025560228`
**Variant:** Command Injection
**Difficulty:** 2/5

## Hints

1. Context: log_analyzer
2. Shell: dash
3. Command structure: command_substitution
4. ⚠️ Filters: space, semicolon
5. 💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}
6. 💡 Bypass semicolon: Use && or || or newline

## Flag

`HACKFORGE{7a99b2fea29b22eca8103ffd4a038c5d}`
