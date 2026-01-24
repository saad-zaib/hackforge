"""
NoSQL Injection Mutation Engine
Generates unique variants of nosql injection vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class NosqlInjectionMutation(MutationEngine):
    """
    Mutation engine for NoSQL Injection vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique nosql injection machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "MongoDB Injection":
            config = self._generate_mongodb_injection(blueprint, difficulty)
        elif variant == "Authentication Bypass":
            config = self._generate_authentication_bypass(blueprint, difficulty)
        elif variant == "Operator Injection":
            config = self._generate_operator_injection(blueprint, difficulty)
        else:
            config = self._generate_mongodb_injection(blueprint, difficulty)

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

    def _generate_mongodb_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate MongoDB Injection vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['user_authentication']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['mongodb_query']))
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
                'variant': 'MongoDB Injection',
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
                'vulnerability_type': 'MongoDB Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_authentication_bypass(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Authentication Bypass vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['login_form']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['find_one']))
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
                'variant': 'Authentication Bypass',
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
                'vulnerability_type': 'Authentication Bypass',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_operator_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Operator Injection vulnerability configuration"""

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
                'variant': 'Operator Injection',
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
                'vulnerability_type': 'Operator Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'dollar_operator': {
                'type': 'dollar_operator',
                'description': 'Dollar_operator filtering',
                'php_code': "$input = str_replace('d', '', $input);",
                'python_code': "input = input.replace('d', '')",
            },
            'ne_operator': {
                'type': 'ne_operator',
                'description': 'Ne_operator filtering',
                'php_code': "$input = str_replace('n', '', $input);",
                'python_code': "input = input.replace('n', '')",
            },
            'regex_operator': {
                'type': 'regex_operator',
                'description': 'Regex_operator filtering',
                'php_code': "$input = str_replace('r', '', $input);",
                'python_code': "input = input.replace('r', '')",
            },
            'gt_operator': {
                'type': 'gt_operator',
                'description': 'Gt_operator filtering',
                'php_code': "$input = str_replace('g', '', $input);",
                'python_code': "input = input.replace('g', '')",
            },
            'where_clause': {
                'type': 'where_clause',
                'description': 'Where_clause filtering',
                'php_code': "$input = str_replace('w', '', $input);",
                'python_code': "input = input.replace('w', '')",
            },
            'javascript_injection': {
                'type': 'javascript_injection',
                'description': 'Javascript_injection filtering',
                'php_code': "$input = str_replace('j', '', $input);",
                'python_code': "input = input.replace('j', '')",
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
