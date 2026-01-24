"""
Cross-Site Request Forgery Mutation Engine
Generates unique variants of cross-site request forgery vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class BrokenAccessControlMutation(MutationEngine):
    """
    Mutation engine for Cross-Site Request Forgery vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique cross-site request forgery machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "Basic CSRF":
            config = self._generate_basic_csrf(blueprint, difficulty)
        elif variant == "CSRF with SameSite Bypass":
            config = self._generate_csrf_with_samesite_bypass(blueprint, difficulty)
        elif variant == "JSON CSRF":
            config = self._generate_json_csrf(blueprint, difficulty)
        else:
            config = self._generate_basic_csrf(blueprint, difficulty)

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

    def _generate_basic_csrf(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Basic CSRF vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['password_change']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['state_change']))
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
                'variant': 'Basic CSRF',
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
                'vulnerability_type': 'Basic CSRF',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_csrf_with_samesite_bypass(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate CSRF with SameSite Bypass vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['email_change']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['database_update']))
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
                'variant': 'CSRF with SameSite Bypass',
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
                'vulnerability_type': 'CSRF with SameSite Bypass',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_json_csrf(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate JSON CSRF vulnerability configuration"""

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
                'variant': 'JSON CSRF',
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
                'vulnerability_type': 'JSON CSRF',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'no_csrf_token': {
                'type': 'no_csrf_token',
                'description': 'No_csrf_token filtering',
                'php_code': "$input = str_replace('n', '', $input);",
                'python_code': "input = input.replace('n', '')",
            },
            'weak_token_validation': {
                'type': 'weak_token_validation',
                'description': 'Weak_token_validation filtering',
                'php_code': "$input = str_replace('w', '', $input);",
                'python_code': "input = input.replace('w', '')",
            },
            'samesite_bypass': {
                'type': 'samesite_bypass',
                'description': 'Samesite_bypass filtering',
                'php_code': "$input = str_replace('s', '', $input);",
                'python_code': "input = input.replace('s', '')",
            },
            'origin_bypass': {
                'type': 'origin_bypass',
                'description': 'Origin_bypass filtering',
                'php_code': "$input = str_replace('o', '', $input);",
                'python_code': "input = input.replace('o', '')",
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
