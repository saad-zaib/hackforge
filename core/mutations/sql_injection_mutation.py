"""
SQL Injection Mutation Engine
Generates unique variants of sql injection vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class SqlInjectionMutation(MutationEngine):
    """
    Mutation engine for SQL Injection vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique sql injection machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "Error-based SQL Injection":
            config = self._generate_error_based_sql_injection(blueprint, difficulty)
        elif variant == "Union-based SQL Injection":
            config = self._generate_union_based_sql_injection(blueprint, difficulty)
        elif variant == "Blind SQL Injection":
            config = self._generate_blind_sql_injection(blueprint, difficulty)
        else:
            config = self._generate_error_based_sql_injection(blueprint, difficulty)

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

    def _generate_error_based_sql_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Error-based SQL Injection vulnerability configuration"""

        contexts = ['login_form', 'user_search', 'profile_view']
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
                'variant': 'Error-based SQL Injection',
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
                'vulnerability_type': 'Error-based SQL Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'SQL Injection',
                'category': 'sql_injection',
                'description': 'Exploits database error messages to extract information',
            }
        }

    def _generate_union_based_sql_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Union-based SQL Injection vulnerability configuration"""

        contexts = ['login_form', 'user_search', 'profile_view']
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
                'variant': 'Union-based SQL Injection',
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
                'vulnerability_type': 'Union-based SQL Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'SQL Injection',
                'category': 'sql_injection',
                'description': 'Uses UNION to combine results from injected queries',
            }
        }

    def _generate_blind_sql_injection(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Blind SQL Injection vulnerability configuration"""

        contexts = ['login_form', 'user_search', 'profile_view']
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
                'variant': 'Blind SQL Injection',
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
                'vulnerability_type': 'Blind SQL Injection',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'SQL Injection',
                'category': 'sql_injection',
                'description': 'No direct output, must infer data from behavior',
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'single_quote': {
                'type': 'single_quote',
                'description': 'Removes single quotes',
                'php_code': '''$input = str_replace(\"\'\", \"\", $input);''',
                'python_code': '''''',
            },
            'or_keyword': {
                'type': 'or_keyword',
                'description': 'Removes OR keyword',
                'php_code': '''$input = preg_replace(\'/\\bOR\\b/i\', \'\', $input);''',
                'python_code': '''''',
            },
            'union_keyword': {
                'type': 'union_keyword',
                'description': 'Removes UNION keyword',
                'php_code': '''$input = preg_replace(\'/\\bUNION\\b/i\', \'\', $input);''',
                'python_code': '''''',
            },
            'select_keyword': {
                'type': 'select_keyword',
                'description': 'Removes SELECT keyword',
                'php_code': '''$input = preg_replace(\'/\\bSELECT\\b/i\', \'\', $input);''',
                'python_code': '''''',
            },
            'sql_comments': {
                'type': 'sql_comments',
                'description': 'Removes SQL comments',
                'php_code': '''$input = preg_replace(\'/--.*$/m\', \'\', $input);''',
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
