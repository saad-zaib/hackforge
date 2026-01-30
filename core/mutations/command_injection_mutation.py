"""
Command Injection Mutation Engine
Generates unique variants of command injection vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class CommandInjectionMutation(MutationEngine):
    """
    Mutation engine for Command Injection vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique command injection machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "Basic Command Injection":
            config = self._generate_basic_command_injection(blueprint, difficulty)
        elif variant == "Command Injection with Filters":
            config = self._generate_command_injection_with_filters(blueprint, difficulty)
        elif variant == "Blind Command Injection":
            config = self._generate_blind_command_injection(blueprint, difficulty)
        elif variant == "Advanced Command Injection":
            config = self._generate_advanced_command_injection(blueprint, difficulty)
        else:
            config = self._generate_basic_command_injection(blueprint, difficulty)

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
            easy_variants = variants[:len(variants)//2] if len(variants) > 2 else variants
            return self.select_random(easy_variants)
        else:
            return self.select_random(variants)

    def _generate_basic_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Basic Command Injection vulnerability configuration"""

        contexts = ['ping_utility', 'whois_lookup', 'dns_lookup', 'url_checker']
        context = self.select_random(contexts)
        
        entry_points = blueprint.entry_points
        entry_point = self.select_random(entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(['single_quote', 'or_keyword'])
        elif difficulty == 3:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword'])
        else:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword', 'select_keyword'])

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Basic Command Injection',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Basic Command Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'Command Injection',
                'category': 'command_injection',
                'description': 'Direct command execution without any filtering',
            }
        }

    def _generate_command_injection_with_filters(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Command Injection with Filters vulnerability configuration"""

        contexts = ['ping_utility', 'whois_lookup', 'dns_lookup', 'url_checker']
        context = self.select_random(contexts)
        
        entry_points = blueprint.entry_points
        entry_point = self.select_random(entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(['single_quote', 'or_keyword'])
        elif difficulty == 3:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword'])
        else:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword', 'select_keyword'])

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Command Injection with Filters',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Command Injection with Filters',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'Command Injection',
                'category': 'command_injection',
                'description': 'Basic filtering that can be bypassed',
            }
        }

    def _generate_blind_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Blind Command Injection vulnerability configuration"""

        contexts = ['ping_utility', 'whois_lookup', 'dns_lookup', 'url_checker']
        context = self.select_random(contexts)
        
        entry_points = blueprint.entry_points
        entry_point = self.select_random(entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(['single_quote', 'or_keyword'])
        elif difficulty == 3:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword'])
        else:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword', 'select_keyword'])

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Blind Command Injection',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Blind Command Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'Command Injection',
                'category': 'command_injection',
                'description': 'No direct output, must use out-of-band techniques',
            }
        }

    def _generate_advanced_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Advanced Command Injection vulnerability configuration"""

        contexts = ['ping_utility', 'whois_lookup', 'dns_lookup', 'url_checker']
        context = self.select_random(contexts)
        
        entry_points = blueprint.entry_points
        entry_point = self.select_random(entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(['single_quote', 'or_keyword'])
        elif difficulty == 3:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword'])
        else:
            filters = self._get_filter_codes(['single_quote', 'or_keyword', 'union_keyword', 'select_keyword'])

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Advanced Command Injection',
                'entry_point': entry_point,
            },
            'constraints': {
                'filters': filters,
            },
            'flag': {
                'content': flag_content,
                'location': '/var/www/html/flag.txt',
            },
            'behavior': {
                'output': 'direct_echo',
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Advanced Command Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'Command Injection',
                'category': 'command_injection',
                'description': 'Multiple filters requiring creative bypass',
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'semicolon': {
                'type': 'command_separator',
                'description': 'Removes semicolons',
                'php_code': '''$input = str_replace(\';\', \'\', $input);''',
                'python_code': '''''',
            },
            'pipe': {
                'type': 'command_separator',
                'description': 'Removes pipes',
                'php_code': '''$input = str_replace(\'|\', \'\', $input);''',
                'python_code': '''''',
            },
            'ampersand': {
                'type': 'command_separator',
                'description': 'Removes ampersands',
                'php_code': '''$input = str_replace(\'&\', \'\', $input);''',
                'python_code': '''''',
            },
            'space_filter': {
                'type': 'whitespace',
                'description': 'Removes spaces',
                'php_code': '''$input = str_replace(\' \', \'\', $input);''',
                'python_code': '''''',
            },
            'cat_command': {
                'type': 'keyword_filter',
                'description': 'Removes \'cat\' command',
                'php_code': '''$input = str_replace(\'cat\', \'\', $input);''',
                'python_code': '''''',
            },
            'slash_filter': {
                'type': 'path_separator',
                'description': 'Removes forward slashes',
                'php_code': '''$input = str_replace(\'/\', \'\', $input);''',
                'python_code': '''''',
            },
            'dollar_filter': {
                'type': 'special_char',
                'description': 'Removes dollar signs',
                'php_code': '''$input = str_replace(\'$\', \'\', $input);''',
                'python_code': '''''',
            },
            'backtick_filter': {
                'type': 'command_substitution',
                'description': 'Removes backticks',
                'php_code': '''$input = str_replace(\'`\', \'\', $input);''',
                'python_code': '''''',
            }
        }

        return [filter_map[f] for f in filter_names if f in filter_map]

    def _generate_hints(self, filters: List[Dict], context: str, difficulty: int) -> List[str]:
        """Generate context-specific hints"""
        hints = [
            f"Context: {context}",
            f"Difficulty: {difficulty}/5",
        ]

        if not filters:
            hints.append("✓ No input filtering - direct attack possible")
        else:
            hints.append(f"⚠️ Filters active: {', '.join([f['type'] for f in filters])}")

        if difficulty <= 2:
            hints.append("💡 Try basic payloads first")

        return hints
