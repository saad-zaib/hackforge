from fastapi import APIRouter, HTTPException
from dependencies import generator
from config import CORE_PATH
import yaml
import logging
from pathlib import Path

router = APIRouter(prefix="/api/blueprints", tags=["blueprints"])
logger = logging.getLogger(__name__)

def load_blueprints_directly(blueprints_dir: Path):
    """Load blueprints directly from YAML files"""
    blueprints = []

    if not blueprints_dir.exists():
        logger.warning(f"Blueprints directory not found: {blueprints_dir}")
        return blueprints

    yaml_files = list(blueprints_dir.glob("*_blueprint.yaml"))

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)

            class BlueprintObj:
                def __init__(self, data):
                    self.blueprint_id = data.get('blueprint_id', 'unknown')
                    self.name = data.get('name', 'Unknown')
                    self.category = data.get('category', 'unknown')
                    self.description = data.get('description', '')
                    self.difficulty_range = data.get('difficulty_range', [1, 5])
                    self.variants = data.get('variants', [])
                    self.technologies = data.get('technologies', [])
                    self.entry_points = data.get('entry_points', [])
                    self.mutation_axes = data.get('mutation_axes', {})

            blueprint = BlueprintObj(data)
            blueprints.append(blueprint)

        except Exception as e:
            logger.error(f"✗ Failed to load {yaml_file.name}: {e}")

    return blueprints

@router.get("")
async def list_blueprints():
    """List all available blueprints"""
    try:
        try:
            blueprints = generator.list_blueprints()
        except Exception:
            blueprints_dir = CORE_PATH / "blueprints"
            blueprints = load_blueprints_directly(blueprints_dir)

        if not blueprints:
            return []

        result = [
            {
                "blueprint_id": bp.blueprint_id,
                "name": bp.name,
                "category": bp.category,
                "description": bp.description,
                "difficulty_range": bp.difficulty_range,
                "variants": bp.variants,
                "technologies": getattr(bp, 'technologies', [])
            }
            for bp in blueprints
        ]

        return result

    except Exception as e:
        logger.error(f"Error in list_blueprints: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{blueprint_id}")
async def get_blueprint(blueprint_id: str):
    """Get specific blueprint details"""
    try:
        blueprints = generator.list_blueprints()
        blueprint = next((bp for bp in blueprints if bp.blueprint_id == blueprint_id), None)

        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found")

        return {
            "blueprint_id": blueprint.blueprint_id,
            "name": blueprint.name,
            "category": blueprint.category,
            "description": blueprint.description,
            "difficulty_range": blueprint.difficulty_range,
            "variants": blueprint.variants,
            "entry_points": blueprint.entry_points,
            "mutation_axes": blueprint.mutation_axes,
            "technologies": getattr(blueprint, 'technologies', [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
