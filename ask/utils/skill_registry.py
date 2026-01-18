"""Skill registry utilities for discovering and parsing skills."""

from pathlib import Path
from typing import List, Dict, Optional

import yaml

from ask.utils.filesystem import get_skills_dir


def get_all_skills() -> List[Dict]:
    """
    Discover and parse all skills in the skills directory.
    
    Returns a list of skill dictionaries with their metadata.
    """
    skills_dir = get_skills_dir()
    skills = []
    
    if not skills_dir.exists():
        return skills
    
    # Walk through category directories
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        
        # Walk through skill directories in each category
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            
            skill_yaml = skill_dir / "skill.yaml"
            if skill_yaml.exists():
                try:
                    skill = parse_skill(skill_yaml)
                    if skill:
                        skill["_path"] = str(skill_dir)
                        skill["_readme"] = str(skill_dir / "README.md")
                        skills.append(skill)
                except Exception:
                    # Skip malformed skills
                    pass
    
    return skills


def get_skill(name: str) -> Optional[Dict]:
    """
    Get a specific skill by name.
    
    Searches through all categories to find a skill with the matching name.
    """
    all_skills = get_all_skills()
    
    for skill in all_skills:
        if skill.get("name") == name:
            return skill
    
    return None


def parse_skill(skill_yaml_path: Path) -> Optional[Dict]:
    """
    Parse a skill.yaml file and return its contents.
    """
    try:
        with open(skill_yaml_path, "r") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def get_skill_readme(skill: Dict) -> Optional[str]:
    """
    Get the README.md content for a skill.
    """
    readme_path = skill.get("_readme")
    if readme_path:
        path = Path(readme_path)
        if path.exists():
            return path.read_text()
    return None
