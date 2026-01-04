"""
Broken Access Control Mutation Engine
Generates unique variants of access control vulnerabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import MutationEngine, VulnerabilityBlueprint, MachineConfig
from typing import Dict, List, Any
import uuid


class BrokenAccessControlMutation(MutationEngine):
    """
    Mutation engine for Broken Access Control vulnerabilities
    """
    
    def mutate(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> MachineConfig:
        """Generate unique BAC machine configuration"""
        
        # Select variant based on difficulty
        variant = self._select_variant(blueprint.variants, difficulty)
        
        # Generate machine ID
        machine_id = self.generate_machine_id()
        
        # Generate configuration based on variant
        if variant == "IDOR (Insecure Direct Object Reference)":
            config = self._generate_idor(blueprint, difficulty)
        elif variant == "Horizontal Privilege Escalation":
            config = self._generate_horizontal_escalation(blueprint, difficulty)
        elif variant == "Vertical Privilege Escalation":
            config = self._generate_vertical_escalation(blueprint, difficulty)
        elif variant == "Missing Function Level Access Control":
            config = self._generate_missing_function_access(blueprint, difficulty)
        elif variant == "Path Traversal":
            config = self._generate_path_traversal(blueprint, difficulty)
        else:
            config = self._generate_idor(blueprint, difficulty)
        
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
        # Easier variants for lower difficulty
        if difficulty <= 2:
            easy_variants = [v for v in variants if "IDOR" in v or "Missing" in v]
            return self.select_random(easy_variants if easy_variants else variants)
        else:
            return self.select_random(variants)
    
    def _get_context(self, blueprint: VulnerabilityBlueprint) -> str:
        """Get context from blueprint, with fallback"""
        contexts = blueprint.mutation_axes.get('contexts', [
            'social_media_profile',
            'banking_transaction',
            'document_management',
            'e_commerce_order'
        ])
        return self.select_random(contexts)
    
    def _generate_idor(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate IDOR vulnerability configuration"""
        
        access_check = self.select_random(blueprint.mutation_axes['access_check'])
        resource_id_type = self.select_random(blueprint.mutation_axes['resource_id_type'])
        resource_type = self.select_random(blueprint.mutation_axes['resource_types'])
        context = self._get_context(blueprint)
        entry_point = self.select_random(blueprint.entry_points)
        auth_method = self.select_random(blueprint.mutation_axes['authorization_method'])
        
        # Generate fake users
        users = self._generate_users(count=10)
        target_user = self.rng.choice([u for u in users if u['role'] == 'admin'])
        current_user = self.rng.choice([u for u in users if u['role'] == 'user'])
        
        # Generate resource IDs based on type
        if resource_id_type == 'sequential_numeric':
            target_id = str(self.rng.randint(1, 1000))
            current_id = str(self.rng.randint(1, 1000))
        elif resource_id_type == 'uuid_v4':
            target_id = str(uuid.uuid4())
            current_id = str(uuid.uuid4())
        elif resource_id_type == 'base64_encoded':
            import base64
            target_id = base64.b64encode(f"user_{target_user['id']}".encode()).decode()
            current_id = base64.b64encode(f"user_{current_user['id']}".encode()).decode()
        elif resource_id_type == 'md5_hash':
            import hashlib
            target_id = hashlib.md5(f"{target_user['id']}".encode()).hexdigest()[:16]
            current_id = hashlib.md5(f"{current_user['id']}".encode()).hexdigest()[:16]
        else:
            target_id = f"user_{target_user['id']}"
            current_id = f"user_{current_user['id']}"
        
        # Flag location
        flag_content = self.generate_flag()
        flag_location = f"/api/{resource_type}/{target_id}/secret"
        
        # Generate hints
        hints = self._generate_idor_hints(access_check, resource_id_type, auth_method, difficulty)
        
        return {
            'application': {
                'context': context,
                'variant': 'IDOR',
                'resource_type': resource_type,
                'entry_point': entry_point,
                'param_name': 'id' if entry_point == 'url_parameter' else 'user_id',
            },
            'constraints': {
                'access_check': access_check,
                'resource_id_type': resource_id_type,
                'target_id': target_id,
                'current_id': current_id,
            },
            'flag': {
                'content': flag_content,
                'location': flag_location,
                'access_method': 'api_endpoint',
            },
            'behavior': {
                'authorization_method': auth_method,
                'response_on_unauthorized': 'empty_or_error' if difficulty > 2 else 'full_data',
                'users': users,
                'target_user': target_user,
                'current_user': current_user,
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'IDOR',
                'estimated_solve_time': f"{difficulty * 5}-{difficulty * 10} minutes",
            }
        }
    
    def _generate_horizontal_escalation(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate horizontal privilege escalation vulnerability"""
        
        context = self._get_context(blueprint)
        auth_method = self.select_random(blueprint.mutation_axes['authorization_method'])
        access_check = self.select_random(blueprint.mutation_axes['access_check'])
        
        # Generate users of same role
        users = self._generate_users(count=8, same_role='user')
        victim_user = users[0]
        attacker_user = users[1]
        
        flag_content = self.generate_flag()
        
        hints = [
            f"Context: {context}",
            f"Authorization: {auth_method}",
            f"You are logged in as: {attacker_user['username']}",
            f"Target user: {victim_user['username']}",
            "⚠️ Access control checks are weak or missing",
            "💡 Try accessing another user's resources with your session",
        ]
        
        return {
            'application': {
                'context': context,
                'variant': 'Horizontal Privilege Escalation',
                'entry_point': 'api_endpoint',
                'endpoint': f"/api/users/{'{user_id}'}/messages",
            },
            'constraints': {
                'access_check': access_check,
                'same_role_bypass': True,
            },
            'flag': {
                'content': flag_content,
                'location': f"/api/users/{victim_user['id']}/messages",
                'access_method': 'authenticated_api_call',
            },
            'behavior': {
                'authorization_method': auth_method,
                'users': users,
                'victim_user': victim_user,
                'attacker_user': attacker_user,
                'session_token': self.generate_random_string(32),
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Horizontal Privilege Escalation',
                'estimated_solve_time': f"{difficulty * 5}-{difficulty * 10} minutes",
            }
        }
    
    def _generate_vertical_escalation(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate vertical privilege escalation vulnerability"""
        
        context = self._get_context(blueprint)
        auth_method = self.select_random(blueprint.mutation_axes['authorization_method'])
        
        users = self._generate_users(count=6)
        admin_user = [u for u in users if u['role'] == 'admin'][0]
        regular_user = [u for u in users if u['role'] == 'user'][0]
        
        flag_content = self.generate_flag()
        
        # Vulnerability mechanism
        if difficulty <= 2:
            vuln_mechanism = "role_parameter_manipulation"
            hint = "💡 Check if role/admin parameters can be modified"
        elif difficulty == 3:
            vuln_mechanism = "jwt_role_manipulation"
            hint = "💡 JWT token may contain role claim that can be modified"
        else:
            vuln_mechanism = "cookie_based_role"
            hint = "💡 Session cookie might contain role information"
        
        hints = [
            f"Context: {context}",
            f"You are: {regular_user['username']} (role: user)",
            f"Target: Admin panel access",
            hint,
            "⚠️ Try to access /admin or modify your privileges",
        ]
        
        return {
            'application': {
                'context': context,
                'variant': 'Vertical Privilege Escalation',
                'entry_point': 'admin_panel',
                'admin_endpoint': '/admin/dashboard',
            },
            'constraints': {
                'mechanism': vuln_mechanism,
                'regular_user_role': 'user',
                'admin_role': 'admin',
            },
            'flag': {
                'content': flag_content,
                'location': '/admin/flag',
                'access_method': 'admin_endpoint',
            },
            'behavior': {
                'authorization_method': auth_method,
                'users': users,
                'admin_user': admin_user,
                'regular_user': regular_user,
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Vertical Privilege Escalation',
                'estimated_solve_time': f"{difficulty * 10}-{difficulty * 15} minutes",
            }
        }
    
    def _generate_missing_function_access(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate missing function-level access control"""
        
        context = self._get_context(blueprint)
        resource_type = self.select_random(blueprint.mutation_axes['resource_types'])
        
        flag_content = self.generate_flag()
        
        # Generate admin functions
        admin_functions = [
            {'name': 'delete_user', 'endpoint': '/api/admin/users/delete'},
            {'name': 'view_all_data', 'endpoint': '/api/admin/data/all'},
            {'name': 'modify_settings', 'endpoint': '/api/admin/settings'},
            {'name': 'export_database', 'endpoint': '/api/admin/export'},
        ]
        
        target_function = self.select_random(admin_functions)
        
        hints = [
            f"Context: {context}",
            "Regular user has limited access",
            f"💡 Admin functions might not check authorization properly",
            f"Try accessing: {target_function['endpoint']}",
            "⚠️ Some endpoints may not validate user role",
        ]
        
        return {
            'application': {
                'context': context,
                'variant': 'Missing Function Level Access Control',
                'entry_point': 'api_endpoint',
            },
            'constraints': {
                'protected_functions': admin_functions,
                'target_function': target_function,
            },
            'flag': {
                'content': flag_content,
                'location': target_function['endpoint'] + '/flag',
                'access_method': 'direct_api_call',
            },
            'behavior': {
                'authorization_method': 'session_cookie',
                'missing_checks_on': [target_function['name']],
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Missing Function Level Access Control',
                'estimated_solve_time': f"{difficulty * 5}-{difficulty * 10} minutes",
            }
        }
    
    def _generate_path_traversal(self, blueprint: VulnerabilityBlueprint, difficulty: int) -> Dict:
        """Generate path traversal vulnerability"""
        
        context = 'document_management'
        
        flag_content = self.generate_flag()
        flag_path = self.select_random([
            '/etc/flag.txt',
            '/var/www/flag.txt',
            '/home/admin/flag.txt',
        ])
        
        # Filters based on difficulty
        if difficulty == 1:
            filters = []
        elif difficulty == 2:
            filters = ['simple_check']
        else:
            filters = ['double_encoding_needed', 'null_byte_possible']
        
        hints = [
            f"Context: {context}",
            "File viewing/download functionality present",
            f"Flag location: {flag_path}",
            "💡 Try path traversal: ../ or ..\\ sequences",
        ]
        
        if filters:
            hints.append(f"⚠️ Filters active: {', '.join(filters)}")
        
        return {
            'application': {
                'context': context,
                'variant': 'Path Traversal',
                'entry_point': 'file_path',
                'param_name': 'file',
            },
            'constraints': {
                'filters': filters,
                'allowed_directory': '/var/www/html/uploads',
            },
            'flag': {
                'content': flag_content,
                'location': flag_path,
                'access_method': 'file_read',
            },
            'behavior': {
                'base_path_check': len(filters) > 0,
                'encoding_bypasses': difficulty > 2,
            },
            'metadata': {
                'exploit_hints': hints,
                'vulnerability_type': 'Path Traversal',
                'estimated_solve_time': f"{difficulty * 5}-{difficulty * 10} minutes",
            }
        }
    
    def _generate_users(self, count: int = 10, same_role: str = None) -> List[Dict]:
        """Generate fake user data"""
        users = []
        roles = ['user', 'user', 'user', 'moderator', 'admin'] if not same_role else [same_role]
        
        for i in range(count):
            role = roles[i % len(roles)] if not same_role else same_role
            users.append({
                'id': i + 1,
                'username': f"user{i+1}",
                'email': f"user{i+1}@example.com",
                'role': role,
                'created': '2025-01-01',
            })
        
        return users
    
    def _generate_idor_hints(self, access_check: str, id_type: str, auth_method: str, difficulty: int) -> List[str]:
        """Generate context-specific hints for IDOR"""
        hints = [
            f"Access control: {access_check}",
            f"Resource ID type: {id_type}",
            f"Authentication: {auth_method}",
        ]
        
        if access_check == 'none':
            hints.append("✓ No access control - direct ID manipulation possible")
        elif access_check == 'client_side_only':
            hints.append("⚠️ Access checks are client-side only")
        elif access_check == 'weak_session_check':
            hints.append("⚠️ Session validation is weak")
        
        if id_type == 'sequential_numeric':
            hints.append("💡 Try incrementing/decrementing the ID parameter")
        elif id_type == 'uuid_v4':
            hints.append("💡 UUIDs are used but might be predictable or leaked")
        elif id_type == 'base64_encoded':
            hints.append("💡 IDs are base64 encoded - try decoding and modifying")
        
        return hints
