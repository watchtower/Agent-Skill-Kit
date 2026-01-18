"""Codex adapter - transforms skills for OpenAI Codex CLI."""

from pathlib import Path
from typing import Dict

from agents.base import BaseAdapter
from ask.utils.skill_registry import get_skill_readme


class CodexAdapter(BaseAdapter):
    """Adapter for Codex CLI skill format.
    
    Paths (from OpenAI documentation):
    - Local (project): codex.md in repository root (single file per project)
    - Global (user):   ~/.codex/instructions.md (single file)
    
    Note: Codex uses single instruction files, not folders.
    We append skill content to the instructions file.
    """
    
    def __init__(self, use_global: bool = False, project_root: Path = None):
        if use_global:
            # Global: ~/.codex/instructions.md
            self.target_dir = Path.home() / ".codex"
            self.target_file = "instructions.md"
        else:
            # Local: codex.md in project root
            self.target_dir = project_root or Path.cwd()
            self.target_file = "codex.md"
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill."""
        # Codex uses a single file, so we create per-skill files in a subdirectory
        skill_name = name or skill.get("name", "unknown")
        return self.target_dir / "instructions" / f"{skill_name}.md"
    
    def transform(self, skill: Dict) -> str:
        """
        Transform a skill into Codex format.
        
        Codex uses simple markdown instruction files.
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
