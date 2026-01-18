"""Claude Code adapter - transforms skills for Claude Code."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class ClaudeAdapter(BaseAdapter):
    """Adapter for Claude Code command format.
    
    Paths:
    - Local (project): .claude/commands/<skill-name>.md
    - Global (user):   ~/.claude/commands/<skill-name>.md
    """
    
    def __init__(self, use_global: bool = False):
        if use_global:
            self.target_dir = Path.home() / ".claude" / "commands"
        else:
            self.target_dir = Path.cwd() / ".claude" / "commands"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Claude Code format.
        
        Claude Code uses markdown command files.
        """
        name = skill.get("name", "Unknown")
        description = skill.get("description", "")
        readme = get_skill_readme(skill) or ""
        
        content = f"""# {name.replace("-", " ").title()}

{description}

---

{readme}
"""
        return content
