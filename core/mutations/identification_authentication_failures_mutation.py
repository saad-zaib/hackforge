"""
Authentication Bypass Mutation Engine
Generates unique variants of authentication bypass vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class IdentificationAuthenticationFailuresMutation(MutationEngine):
    """
    Mutation engine for Authentication Bypass vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique authentication bypass machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "SQL Injection Auth Bypass":
            config = self._generate_sql_injection_auth_bypass(blueprint, difficulty)
        elif variant == "Default Credentials":
            config = self._generate_default_credentials(blueprint, difficulty)
        elif variant == "Session Fixation":
            config = self._generate_session_fixation(blueprint, difficulty)
        elif variant == "JWT Manipulation":
            config = self._generate_jwt_manipulation(blueprint, difficulty)
        else:
            config = self._generate_sql_injection_auth_bypass(blueprint, difficulty)

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

    def _generate_sql_injection_auth_bypass(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate SQL Injection Auth Bypass vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['login_page']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['sql_query']))
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
                'variant': 'SQL Injection Auth Bypass',
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
                'vulnerability_type': 'SQL Injection Auth Bypass',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_default_credentials(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Default Credentials vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['admin_panel']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['session_store']))
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
                'variant': 'Default Credentials',
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
                'vulnerability_type': 'Default Credentials',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_session_fixation(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Session Fixation vulnerability configuration"""

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
                'variant': 'Session Fixation',
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
                'vulnerability_type': 'Session Fixation',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_jwt_manipulation(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate JWT Manipulation vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['api_authentication']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['jwt_validator']))
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
                'variant': 'JWT Manipulation',
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
                'vulnerability_type': 'JWT Manipulation',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'or_1_equals_1': {
                'type': 'or_1_equals_1',
                'description': 'Or_1_equals_1 filtering',
                'php_code': "$input = str_replace('o', '', $input);",
                'python_code': "input = input.replace('o', '')",
            },
            'admin_admin': {
                'type': 'admin_admin',
                'description': 'Admin_admin filtering',
                'php_code': "$input = str_replace('a', '', $input);",
                'python_code': "input = input.replace('a', '')",
            },
            'null_byte': {
                'type': 'null_byte',
                'description': 'Null_byte filtering',
                'php_code': "$input = str_replace('n', '', $input);",
                'python_code': "input = input.replace('n', '')",
            },
            'comment_bypass': {
                'type': 'comment_bypass',
                'description': 'Comment_bypass filtering',
                'php_code': "$input = str_replace('c', '', $input);",
                'python_code': "input = input.replace('c', '')",
            },
            'jwt_manipulation': {
                'type': 'jwt_manipulation',
                'description': 'Jwt_manipulation filtering',
                'php_code': "$input = str_replace('j', '', $input);",
                'python_code': "input = input.replace('j', '')",
            },
            'session_hijacking': {
                'type': 'session_hijacking',
                'description': 'Session_hijacking filtering',
                'php_code': "$input = str_replace('s', '', $input);",
                'python_code': "input = input.replace('s', '')",
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
