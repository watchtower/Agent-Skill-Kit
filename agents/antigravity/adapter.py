"""Antigravity adapter - transforms skills for Google Antigravity."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class AntigravityAdapter(BaseAdapter):
    """Adapter for Antigravity skill format.
    
    Paths (from https://antigravity.google/docs/skills):
    - Local (project): .agent/skills/<skill-name>/SKILL.md
    - Global (user):   ~/.gemini/antigravity/skills/<skill-name>/SKILL.md
    """
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            # Global: ~/.gemini/antigravity/skills/
            self.target_dir = Path.home() / ".gemini" / "antigravity" / "skills"
        else:
            # Local: .agent/skills/
            self.project_root = project_root or Path.cwd()
            self.target_dir = self.project_root / ".agent" / "skills"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / skill_name / "SKILL.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Antigravity format.
        
        Antigravity uses SKILL.md with YAML frontmatter.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        content = f"""---
name: {name}
description: {description}
---

{readme}
"""
        return content
