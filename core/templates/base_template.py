"""
Base Template Classes
Abstract interfaces for code generation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from base import MachineConfig


class BaseTemplate(ABC):
    """
    Abstract base class for all templates
    """
    
    def __init__(self, config: MachineConfig):
        self.config = config
        self.machine_id = config.machine_id
        self.variant = config.variant
        self.difficulty = config.difficulty
    
    @abstractmethod
    def generate_code(self) -> str:
        """Generate the vulnerable application code"""
        pass
    
    @abstractmethod
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile for the application"""
        pass
    
    def generate_docker_compose(self, port: int) -> str:
        """Generate docker-compose.yml entry"""
        flag_location = self.config.flag.get('location', '/var/www/html/flag.txt')
        
        return f"""
  machine_{self.machine_id}:
    build: ./machines/{self.machine_id}
    container_name: hackforge_{self.machine_id}
    ports:
      - "{port}:80"
    volumes:
      - ./machines/{self.machine_id}/app:/var/www/html
      - ./machines/{self.machine_id}/flag.txt:{flag_location}:ro
    environment:
      - MACHINE_ID={self.machine_id}
      - DIFFICULTY={self.difficulty}
"""
    
    def get_flag_content(self) -> str:
        """Get flag content"""
        return self.config.flag['content']
    
    def get_hints(self) -> list:
        """Get exploitation hints"""
        return self.config.metadata.get('exploit_hints', [])


class TemplateRenderer:
    """
    Factory class for rendering templates based on vulnerability type
    """
    
    @staticmethod
    def get_template_class(config: MachineConfig):
        """Get appropriate template class for machine config"""
        
        category = config.blueprint_id
        
        if category == 'inj_001':
            # Import from templates directory
            from templates.injection_templates import InjectionTemplate
            return InjectionTemplate
        elif category == 'bac_001':
            from templates.bac_templates import BrokenAccessControlTemplate
            return BrokenAccessControlTemplate
        else:
            raise ValueError(f"No template for category: {category}")
    
    @staticmethod
    def render(config: MachineConfig) -> Dict[str, str]:
        """
        Render machine config to code
        
        Returns:
            Dict with 'code', 'dockerfile', 'docker_compose'
        """
        
        template_class = TemplateRenderer.get_template_class(config)
        template = template_class(config)
        
        return {
            'code': template.generate_code(),
            'dockerfile': template.generate_dockerfile(),
            'docker_compose': template.generate_docker_compose(8080),
            'flag': template.get_flag_content(),
            'hints': template.get_hints(),
        }
