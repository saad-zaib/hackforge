"""
XML External Entity Mutation Engine
Generates unique variants of xml external entity vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class XxeInjectionMutation(MutationEngine):
    """
    Mutation engine for XML External Entity vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique xml external entity machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "File Disclosure XXE":
            config = self._generate_file_disclosure_xxe(blueprint, difficulty)
        elif variant == "Blind XXE":
            config = self._generate_blind_xxe(blueprint, difficulty)
        elif variant == "XXE via File Upload":
            config = self._generate_xxe_via_file_upload(blueprint, difficulty)
        else:
            config = self._generate_file_disclosure_xxe(blueprint, difficulty)

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

    def _generate_file_disclosure_xxe(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate File Disclosure XXE vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['xml_parser']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['xml_parse']))
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
                'variant': 'File Disclosure XXE',
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
                'vulnerability_type': 'File Disclosure XXE',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_blind_xxe(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Blind XXE vulnerability configuration"""

        context = self.select_random(blueprint.mutation_axes.get('contexts', ['soap_endpoint']))
        sink = self.select_random(blueprint.mutation_axes.get('sinks', ['dom_parser']))
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
                'variant': 'Blind XXE',
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
                'vulnerability_type': 'Blind XXE',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }

    def _generate_xxe_via_file_upload(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate XXE via File Upload vulnerability configuration"""

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
                'variant': 'XXE via File Upload',
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
                'vulnerability_type': 'XXE via File Upload',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'file_protocol': {
                'type': 'file_protocol',
                'description': 'File_protocol filtering',
                'php_code': "$input = str_replace('f', '', $input);",
                'python_code': "input = input.replace('f', '')",
            },
            'http_protocol': {
                'type': 'http_protocol',
                'description': 'Http_protocol filtering',
                'php_code': "$input = str_replace('h', '', $input);",
                'python_code': "input = input.replace('h', '')",
            },
            'php_wrapper': {
                'type': 'php_wrapper',
                'description': 'Php_wrapper filtering',
                'php_code': "$input = str_replace('p', '', $input);",
                'python_code': "input = input.replace('p', '')",
            },
            'expect_protocol': {
                'type': 'expect_protocol',
                'description': 'Expect_protocol filtering',
                'php_code': "$input = str_replace('e', '', $input);",
                'python_code': "input = input.replace('e', '')",
            },
            'data_protocol': {
                'type': 'data_protocol',
                'description': 'Data_protocol filtering',
                'php_code': "$input = str_replace('d', '', $input);",
                'python_code': "input = input.replace('d', '')",
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
