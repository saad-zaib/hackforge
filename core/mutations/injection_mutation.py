"""
Command Injection Mutation Engine
Generates unique variants of command injection vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class InjectionMutation(MutationEngine):
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
        elif variant == "Blind Command Injection":
            config = self._generate_blind_command_injection(blueprint, difficulty)
        elif variant == "Time-based Command Injection":
            config = self._generate_time_based_command_injection(blueprint, difficulty)
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

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['ping_command']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['system']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

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
            }
        }

    def _generate_blind_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Blind Command Injection vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['file_operation']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['exec']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

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
            }
        }

    def _generate_time_based_command_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Time-based Command Injection vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['default_context']))
        entry_point = self.select_random(blueprint.entry_points)

        # Select filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('basic', []))
        elif difficulty == 3:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('medium', []))
        else:
            filters = self._get_filter_codes(blueprint.mutation_axes.get('filters', {}).get('advanced', []))

        flag_content = self.generate_flag()
        hints = self._generate_hints(filters, context, difficulty)

        return {
            'application': {
                'context': context,
                'variant': 'Time-based Command Injection',
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
                'vulnerability_type': 'Time-based Command Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'semicolon': {
                'type': 'semicolon',
                'description': 'Semicolon filtering',
                'php_code': "$input = str_replace('s', '', $input);",
                'python_code': "input = input.replace('s', '')",
            },
            'pipe': {
                'type': 'pipe',
                'description': 'Pipe filtering',
                'php_code': "$input = str_replace('p', '', $input);",
                'python_code': "input = input.replace('p', '')",
            },
            'backtick': {
                'type': 'backtick',
                'description': 'Backtick filtering',
                'php_code': "$input = str_replace('b', '', $input);",
                'python_code': "input = input.replace('b', '')",
            },
            'ampersand': {
                'type': 'ampersand',
                'description': 'Ampersand filtering',
                'php_code': "$input = str_replace('a', '', $input);",
                'python_code': "input = input.replace('a', '')",
            },
            'newline': {
                'type': 'newline',
                'description': 'Newline filtering',
                'php_code': "$input = str_replace('n', '', $input);",
                'python_code': "input = input.replace('n', '')",
            },
            'dollar_paren': {
                'type': 'dollar_paren',
                'description': 'Dollar_paren filtering',
                'php_code': "$input = str_replace('d', '', $input);",
                'python_code': "input = input.replace('d', '')",
            },
            'command_substitution': {
                'type': 'command_substitution',
                'description': 'Command_substitution filtering',
                'php_code': "$input = str_replace('c', '', $input);",
                'python_code': "input = input.replace('c', '')",
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
