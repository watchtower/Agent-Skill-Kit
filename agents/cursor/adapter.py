"""Cursor adapter - transforms skills for Cursor AI."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class CursorAdapter(BaseAdapter):
    """Adapter for Cursor AI format.
    
    Paths:
    - Local: .cursor/rules/<skill-name>.md
    - Global: ~/.cursor/rules/<skill-name>.md
    
    Format:
    Cursor uses Markdown files in the .cursor/rules directory.
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".cursor" / "rules"
        else:
            self.target_dir = Path.cwd() / ".cursor" / "rules"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        # Cursor rules are typically markdown files
        return self.target_dir / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """Transform a skill into Cursor format."""
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        # Cursor reads the markdown file directly.
        # We include the description at the top.
        content = f"""# {name}

{description}

---

{readme}
"""
        return content
