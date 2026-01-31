"""
xss Mutation Engine
Generates unique variants of xss vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any


class CrossSiteScriptingMutation(MutationEngine):
    """
    Mutation engine for xss vulnerabilities
    """

    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique xss machine configuration"""

        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)

        # Generate machine ID
        machine_id = self.generate_machine_id()

        # Generate configuration based on variant
        if variant == "Reflected XSS":
            config = self._generate_reflected_xss(blueprint, difficulty)
        elif variant == "Stored XSS":
            config = self._generate_stored_xss(blueprint, difficulty)
        elif variant == "DOM-based XSS":
            config = self._generate_dom_based_xss(blueprint, difficulty)
        elif variant == "Attribute-based XSS":
            config = self._generate_attribute_based_xss(blueprint, difficulty)
        else:
            config = self._generate_reflected_xss(blueprint, difficulty)

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

    def _generate_reflected_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Reflected XSS vulnerability configuration"""

        contexts = ['comment_system', 'search_results', 'user_profile', 'message_board']
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
                'variant': 'Reflected XSS',
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
                'vulnerability_type': 'Reflected XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'xss',
                'category': 'cross_site_scripting',
                'description': 'User input is immediately reflected back in the response without proper sanitization',
            }
        }

    def _generate_stored_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Stored XSS vulnerability configuration"""

        contexts = ['comment_system', 'search_results', 'user_profile', 'message_board']
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
                'variant': 'Stored XSS',
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
                'vulnerability_type': 'Stored XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'xss',
                'category': 'cross_site_scripting',
                'description': 'Malicious script is stored in database and executed when viewed by other users',
            }
        }

    def _generate_dom_based_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate DOM-based XSS vulnerability configuration"""

        contexts = ['comment_system', 'search_results', 'user_profile', 'message_board']
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
                'variant': 'DOM-based XSS',
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
                'vulnerability_type': 'DOM-based XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'xss',
                'category': 'cross_site_scripting',
                'description': 'Client-side JavaScript code processes user input unsafely, creating XSS vulnerability',
            }
        }

    def _generate_attribute_based_xss(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate Attribute-based XSS vulnerability configuration"""

        contexts = ['comment_system', 'search_results', 'user_profile', 'message_board']
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
                'variant': 'Attribute-based XSS',
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
                'vulnerability_type': 'Attribute-based XSS',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
                'vuln_name': 'xss',
                'category': 'cross_site_scripting',
                'description': 'User input is placed inside HTML attributes without proper encoding',
            }
        }


    def _get_filter_codes(self, filter_names: List[str]) -> List[Dict]:
        """Convert filter names to filter code objects"""
        filter_map = {
            'script_tag_filter': {
                'type': 'script_tag',
                'description': 'Blocks <script> tags (case-sensitive)',
                'php_code': '''$input = str_replace(\'<script>\', \'\', $input); $input = str_replace(\'</script>\', \'\', $input);''',
                'python_code': '''input_data = input_data.replace(\'<script>\', \'\').replace(\'</script>\', \'\')''',
            },
            'angle_bracket_filter': {
                'type': 'character_filter',
                'description': 'Removes < and > characters',
                'php_code': '''$input = str_replace([\'<\', \'>\'], \'\', $input);''',
                'python_code': '''input_data = input_data.replace(\'<\', \'\').replace(\'>\', \'\')''',
            },
            'htmlspecialchars_partial': {
                'type': 'encoding',
                'description': 'Partial HTML entity encoding (missing ENT_QUOTES)',
                'php_code': '''$input = htmlspecialchars($input);''',
                'python_code': '''import html; input_data = html.escape(input_data)''',
            },
            'event_handler_filter': {
                'type': 'event_filter',
                'description': 'Blocks common event handlers (onerror, onload, onclick)',
                'php_code': '''$input = preg_replace(\'/on\w+\s*=/i\', \'\', $input);''',
                'python_code': '''import re; input_data = re.sub(r\'on\w+\s*=\', \'\', input_data, flags=re.IGNORECASE)''',
            },
            'javascript_protocol_filter': {
                'type': 'protocol_filter',
                'description': 'Blocks javascript: protocol',
                'php_code': '''$input = str_replace(\'javascript:\', \'\', $input);''',
                'python_code': '''input_data = input_data.replace(\'javascript:\', \'\')''',
            },
            'dom_purify_bypass': {
                'type': 'sanitization',
                'description': 'Client-side sanitization with potential bypasses',
                'php_code': '''// Client-side sanitization only''',
                'python_code': '''# Client-side sanitization only''',
            },
            'csp_bypass': {
                'type': 'csp',
                'description': 'Content Security Policy with unsafe-inline',
                'php_code': '''header(\"Content-Security-Policy: script-src \'self\' \'unsafe-inline\'\");''',
                'python_code': '''response.headers[\'Content-Security-Policy\'] = \"script-src \'self\' \'unsafe-inline\'\"''',
            },
            'regex_blacklist': {
                'type': 'regex_filter',
                'description': 'Regex-based blacklist that can be bypassed',
                'php_code': '''$input = preg_replace(\'/<script.*?>.*?<\/script>/is\', \'\', $input);''',
                'python_code': '''import re; input_data = re.sub(r\'<script.*?>.*?</script>\', \'\', input_data, flags=re.IGNORECASE|re.DOTALL)''',
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
