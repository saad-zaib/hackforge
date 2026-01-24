"""
Insecure Deserialization Mutation Engine
Generates unique variants of insecure deserialization vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class SoftwareDataIntegrityFailuresMutation(MutationEngine):
    """
    Mutation engine for Insecure Deserialization vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique insecure deserialization machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "PHP Object Injection":
            config = self._generate_php_object_injection(blueprint, difficulty)
        elif variant == "Java Deserialization":
            config = self._generate_java_deserialization(blueprint, difficulty)
        elif variant == "Python Pickle Injection":
            config = self._generate_python_pickle_injection(blueprint, difficulty)
        else:
            config = self._generate_php_object_injection(blueprint, difficulty)

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

    def _generate_php_object_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate PHP Object Injection vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['session_handler']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['unserialize']))
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
                'variant': 'PHP Object Injection',
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
                'vulnerability_type': 'PHP Object Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_java_deserialization(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Java Deserialization vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['api_endpoint']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['objectmapper_readvalue']))
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
                'variant': 'Java Deserialization',
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
                'vulnerability_type': 'Java Deserialization',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_python_pickle_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Python Pickle Injection vulnerability configuration"""

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
                'variant': 'Python Pickle Injection',
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
                'vulnerability_type': 'Python Pickle Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'php_object': {
                'type': 'php_object',
                'description': 'Php_object filtering',
                'php_code': "$input = str_replace('p', '', $input);",
                'python_code': "input = input.replace('p', '')",
            },
            'java_serialized': {
                'type': 'java_serialized',
                'description': 'Java_serialized filtering',
                'php_code': "$input = str_replace('j', '', $input);",
                'python_code': "input = input.replace('j', '')",
            },
            'python_pickle': {
                'type': 'python_pickle',
                'description': 'Python_pickle filtering',
                'php_code': "$input = str_replace('p', '', $input);",
                'python_code': "input = input.replace('p', '')",
            },
            'yaml_deserialization': {
                'type': 'yaml_deserialization',
                'description': 'Yaml_deserialization filtering',
                'php_code': "$input = str_replace('y', '', $input);",
                'python_code': "input = input.replace('y', '')",
            },
            'json_deserialization': {
                'type': 'json_deserialization',
                'description': 'Json_deserialization filtering',
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
