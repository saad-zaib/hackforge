"""
Injection Mutation Engine
Generates unique variants of injection vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class InjectionMutation(MutationEngine):
    """
    Mutation engine for Injection vulnerabilities
    """
    
    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique injection machine configuration"""
        
        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)
        
        # Generate machine ID
        machine_id = self.generate_machine_id()
        
        # Generate configuration based on variant
        if variant == "SQL Injection":
            config = self._generate_sql_injection(blueprint, difficulty)
        elif variant == "Command Injection":
            config = self._generate_command_injection(blueprint, difficulty)
        elif variant == "NoSQL Injection":
            config = self._generate_nosql_injection(blueprint, difficulty)
        elif variant == "LDAP Injection":
            config = self._generate_ldap_injection(blueprint, difficulty)
        elif variant == "Template Injection":
            config = self._generate_template_injection(blueprint, difficulty)
        else:
            config = self._generate_command_injection(blueprint, difficulty)
        
        # Create machine config
        return MachineConfig(
            machine_id=machine_id,
            blueprint_id=blueprint.blueprint_id,
            variant=variant,
            difficulty=difficulty,
            seed=self.seed,
            application=config['application'],
            constraints=config['constraints'],
            flag=config['flag'],
            behavior=config['behavior'],
            metadata=config['metadata']
        )
    
    def _select_variant(self, variants: List[str], difficulty: int) -> str:
        """Select variant based on difficulty level"""
        if difficulty <= 2:
            easy_variants = [v for v in variants if "Command" in v or "SQL" in v]
            return self.select_random(easy_variants if easy_variants else variants)
        else:
            return self.select_random(variants)
    
    def _generate_sql_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate SQL injection vulnerability configuration"""
        
        context = self.select_random(blueprint.mutation_axes['contexts'])
        database = self.select_random(blueprint.mutation_axes['databases'])
        sink = self.select_random(blueprint.mutation_axes['sinks']['sql'])
        entry_point = self.select_random(blueprint.entry_points)
        output_behavior = self.select_random(blueprint.mutation_axes['output_behavior'])
        
        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['basic'])
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['medium'])
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['advanced'])
        
        # SQL query context
        if context == 'search_function':
            base_query = "SELECT * FROM products WHERE name LIKE '%{input}%'"
            param_name = 'search'
        elif context == 'login_form':
            base_query = "SELECT * FROM users WHERE username='{input}' AND password='{password}'"
            param_name = 'username'
        else:
            base_query = "SELECT * FROM items WHERE id={input}"
            param_name = 'id'
        
        # Flag storage
        flag_content = self.generate_flag()
        flag_table = 'secrets' if database != 'mongodb' else 'secrets_collection'
        
        # Generate hints
        hints = self._generate_sql_hints(filters, database, context, difficulty, output_behavior)
        
        return {
            'application': {
                'context': context,
                'variant': 'SQL Injection',
                'entry_point': entry_point,
                'param_name': param_name,
                'sink': sink,
            },
            'constraints': {
                'filters': filters,
                'database': database,
                'base_query': base_query,
                'injectable_param': param_name,
            },
            'flag': {
                'content': flag_content,
                'location': f"database:{flag_table}.flag",
                'table_name': flag_table,
                'column_name': 'flag',
            },
            'behavior': {
                'output': output_behavior,
                'error_disclosure': difficulty <= 2,
                'union_based': difficulty <= 3,
                'blind': difficulty >= 4,
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'SQL Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }
    
    def _generate_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate command injection vulnerability configuration"""
        
        context = self.select_random(blueprint.mutation_axes['contexts'])
        sink = self.select_random(blueprint.mutation_axes['sinks']['command'])
        entry_point = self.select_random(blueprint.entry_points)
        shell = self.select_random(blueprint.mutation_axes['shells'])
        cmd_structure = self.select_random(blueprint.mutation_axes['command_structures'])
        output_behavior = self.select_random(blueprint.mutation_axes['output_behavior'])
        
        # Base command context
        if context == 'ping_utility':
            base_command = "ping -c 1"
            param_name = 'host'
        elif context == 'whois_lookup':
            base_command = "whois"
            param_name = 'domain'
        elif context == 'log_analyzer':
            base_command = "grep"
            param_name = 'pattern'
        else:
            base_command = "nslookup"
            param_name = 'hostname'
        
        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['basic'])
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['medium'])
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes['filters']['advanced'])
        
        # Flag location
        flag_content = self.generate_flag()
        flag_location = self.select_random(blueprint.mutation_axes['flag_locations'][:5])
        
        # Generate hints
        hints = self._generate_command_hints(filters, shell, context, cmd_structure)
        
        return {
            'application': {
                'context': context,
                'variant': 'Command Injection',
                'base_command': base_command,
                'entry_point': entry_point,
                'param_name': param_name,
                'sink': sink,
            },
            'constraints': {
                'filters': filters,
                'shell': shell,
                'command_structure': cmd_structure,
            },
            'flag': {
                'content': flag_content,
                'location': flag_location,
            },
            'behavior': {
                'output': output_behavior,
                'shell_features': self._get_shell_features(shell),
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Command Injection',
                'estimated_solve_time': f"{difficulty * 5}-{difficulty * 10} minutes",
            }
        }
    
    def _generate_nosql_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate NoSQL injection vulnerability configuration"""
        
        context = self.select_random(['search_function', 'login_form', 'export_tool'])
        sink = self.select_random(blueprint.mutation_axes['sinks']['nosql'])
        entry_point = self.select_random([e for e in blueprint.entry_points if 'json' in e or 'post' in e])
        
        # MongoDB query context
        if context == 'login_form':
            base_query = "db.users.find({username: input, password: input2})"
            param_name = 'username'
        else:
            base_query = "db.products.find({category: input})"
            param_name = 'category'
        
        flag_content = self.generate_flag()
        
        hints = [
            f"Context: {context}",
            "MongoDB NoSQL database",
            f"Parameter: {param_name}",
            "💡 Try NoSQL operators: $ne, $gt, $regex",
            "💡 JSON injection possible in POST body",
            f"Flag stored in 'secrets' collection",
        ]
        
        if difficulty > 2:
            hints.append("⚠️ Input validation present - bypass needed")
        
        return {
            'application': {
                'context': context,
                'variant': 'NoSQL Injection',
                'entry_point': entry_point,
                'param_name': param_name,
                'sink': sink,
            },
            'constraints': {
                'database': 'mongodb',
                'base_query': base_query,
                'operators_allowed': ['$ne', '$gt', '$regex', '$where'],
            },
            'flag': {
                'content': flag_content,
                'location': 'mongodb:secrets.flag',
                'collection': 'secrets',
            },
            'behavior': {
                'output': 'direct_echo',
                'json_parsing': True,
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'NoSQL Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }
    
    def _generate_ldap_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate LDAP injection vulnerability configuration"""
        
        context = 'login_form'
        entry_point = 'http_post_param'
        
        base_query = "(&(uid={username})(password={password}))"
        
        flag_content = self.generate_flag()
        
        hints = [
            "LDAP authentication system",
            "💡 Try LDAP filter injection",
            "💡 Bypass: username=*)(uid=*))(|(uid=*",
            "Flag stored in admin LDAP entry",
        ]
        
        return {
            'application': {
                'context': context,
                'variant': 'LDAP Injection',
                'entry_point': entry_point,
                'param_name': 'username',
            },
            'constraints': {
                'base_query': base_query,
                'ldap_server': 'openldap',
            },
            'flag': {
                'content': flag_content,
                'location': 'ldap:cn=admin,dc=example,dc=com',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'LDAP Injection',
                'estimated_solve_time': f"{difficulty * 15}-{difficulty * 20} minutes",
            }
        }
    
    def _generate_template_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate template injection vulnerability configuration"""
        
        context = 'report_generator'
        entry_point = 'http_post_param'
        
        template_engine = self.select_random(['jinja2', 'twig', 'freemarker'])
        
        flag_content = self.generate_flag()
        flag_location = '/var/www/flag.txt'
        
        hints = [
            f"Template engine: {template_engine}",
            "Report generation with user input",
            "💡 Try template injection syntax",
        ]
        
        if template_engine == 'jinja2':
            hints.append("💡 Jinja2: {{7*7}} or {{config.items()}}")
        elif template_engine == 'twig':
            hints.append("💡 Twig: {{7*7}} or {{_self.env.display()}}")
        
        return {
            'application': {
                'context': context,
                'variant': 'Template Injection',
                'entry_point': entry_point,
                'param_name': 'template_data',
                'template_engine': template_engine,
            },
            'constraints': {
                'template_engine': template_engine,
                'sandbox': difficulty > 3,
            },
            'flag': {
                'content': flag_content,
                'location': flag_location,
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Template Injection',
                'estimated_solve_time': f"{difficulty * 15}-{difficulty * 20} minutes",
            }
        }
    
    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'space': {
                'type': 'space',
                'description': 'Spaces are removed',
                'php_code': "$input = str_replace(' ', '', $input);",
                'python_code': "input = input.replace(' ', '')",
            },
            'semicolon': {
                'type': 'semicolon',
                'description': 'Semicolons are removed',
                'php_code': "$input = str_replace(';', '', $input);",
                'python_code': "input = input.replace(';', '')",
            },
            'pipe': {
                'type': 'pipe',
                'description': 'Pipes are removed',
                'php_code': "$input = str_replace('|', '', $input);",
                'python_code': "input = input.replace('|', '')",
            },
            'quote': {
                'type': 'quote',
                'description': 'Quotes are escaped',
                'php_code': "$input = addslashes($input);",
                'python_code': "input = input.replace(\"'\", \"\\\\'\").replace('\"', '\\\\\"')",
            },
            'comment': {
                'type': 'comment',
                'description': 'SQL comments blocked',
                'php_code': "$input = str_replace(['--', '#', '/*'], '', $input);",
                'python_code': "input = input.replace('--', '').replace('#', '').replace('/*', '')",
            },
            'union': {
                'type': 'union',
                'description': 'UNION keyword blocked',
                'php_code': "$input = preg_replace('/union/i', '', $input);",
                'python_code': "input = re.sub(r'union', '', input, flags=re.IGNORECASE)",
            },
            'ampersand': {
                'type': 'ampersand',
                'description': 'Ampersands blocked',
                'php_code': "$input = str_replace('&', '', $input);",
                'python_code': "input = input.replace('&', '')",
            },
        }
        
        return [filter_map[f] for f in filter_names if f in filter_map]
    
    def _get_shell_features(self, shell: str) -> List[str]:
        """Get available features for shell type"""
        features = {
            'bash': ['process_substitution', 'brace_expansion', 'command_substitution'],
            'sh': ['command_substitution', 'basic_redirection'],
            'dash': ['command_substitution', 'basic_redirection'],
            'zsh': ['process_substitution', 'brace_expansion', 'glob_expansion'],
        }
        return features.get(shell, ['command_substitution'])
    
    def _generate_sql_hints(self, filters: List[Dict], database: str, context: str, difficulty: int, output: str) -> List[str]:
        """Generate context-specific hints for SQL injection"""
        hints = [
            f"Context: {context}",
            f"Database: {database}",
            f"Output behavior: {output}",
        ]
        
        if not filters:
            hints.append("✓ No input filtering - direct injection possible")
        else:
            hints.append(f"⚠️ Filters active: {', '.join([f['type'] for f in filters])}")
        
        if difficulty <= 2:
            hints.append("💡 Try: ' OR '1'='1")
        
        if output == 'error_based':
            hints.append("💡 Use error-based extraction")
        elif output == 'blind':
            hints.append("💡 Blind SQLi - use time-based or boolean techniques")
        
        hints.append(f"Flag stored in 'secrets' table")
        
        return hints
    
    def _generate_command_hints(self, filters: List[Dict], shell: str, context: str, cmd_structure: str) -> List[str]:
        """Generate context-specific hints for command injection"""
        hints = [
            f"Context: {context}",
            f"Shell: {shell}",
            f"Command structure: {cmd_structure}",
        ]
        
        if not filters:
            hints.append("✓ No filtering - direct command injection possible")
            hints.append("💡 Try: ; cat /flag.txt")
        else:
            blocked = [f['type'] for f in filters]
            hints.append(f"⚠️ Filters: {', '.join(blocked)}")
            
            if 'space' in blocked:
                hints.append("💡 Bypass spaces: Use ${IFS} or $IFS$ or {cat,/flag.txt}")
            if 'semicolon' in blocked:
                hints.append("💡 Bypass semicolon: Use && or || or newline")
            if 'pipe' in blocked:
                hints.append("💡 Bypass pipe: Use command substitution $()")
        
        if shell == 'bash':
            hints.append("💡 Bash features available: process substitution, brace expansion")
        
        return hints
