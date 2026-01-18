"""Base adapter class with safe copy logic."""

from pathlib import Path
from typing import Dict


class BaseAdapter:
    """Base class for all agent adapters with safe copy behavior."""
    
    target_dir: Path = None
    
    def get_target_path(self, skill: Dict, name: str = None) -> Path:
        """Get the target path for a skill. Override in subclasses."""
        raise NotImplementedError
    
    def transform(self, skill: Dict) -> str:
        """Transform skill to agent format. Override in subclasses."""
        raise NotImplementedError
    
    def install_resources(self, skill: Dict, target_dir: Path, dry_run: bool = False) -> Dict[str, bool]:
        """
        Install additional resources (scripts, references, etc.).
        Override in subclasses to handle these.
        
        Args:
            skill: The skill data
            target_dir: Where to install
            dry_run: If True, only check for conflicts
            
        Returns:
            Dict indicating status, e.g., {"conflict": True, "details": "..."}
        """
        return {"conflict": False}

    def install(self, skill: Dict) -> Dict:
        """
        Install a skill (new method to replace copy_skill eventually).
        Defaults to the simple behavior of writing a single file.
        """
        status = self.copy_skill(skill)
        return status

    def copy_skill(self, skill: Dict, dry_run: bool = False, new_name: str = None) -> Dict:
        """
        Copy a skill to the agent's directory with safe copy behavior.
        
        Safe Copy Rules:
        - NEVER overwrite existing files
        - If same name exists: return conflict status (caller prompts for new name)
        - Never delete existing user folders
        - Check ALL resources for conflicts before writing anything
        
        Args:
            skill: Skill dictionary with metadata
            dry_run: If True, don't actually copy
            new_name: Optional new name if renaming due to conflict
        
        Returns:
            status dict with: status, target, would_conflict (for dry-run)
        """
        # Use new_name if provided (for conflict resolution)
        name_to_use = new_name or skill.get("name")
        target = self.get_target_path(skill, name_to_use)
        
        # 1. Check main file conflict
        if target.exists():
            if dry_run:
                return {
                    "status": "dry-run",
                    "target": str(target),
                    "would_conflict": True,
                    "reason": "Main file exists"
                }
            return {
                "status": "conflict",
                "target": str(target),
                "reason": "Main file exists"
            }
            
        # 2. Check resource conflicts
        # We pass target.parent because resources usually live relative to the command or in a fixed spot
        resource_status = self.install_resources(skill, target.parent, dry_run=True)
        if resource_status.get("conflict"):
             if dry_run:
                return {
                    "status": "dry-run",
                    "target": str(target),
                    "would_conflict": True,
                    "reason": f"Resources conflict: {resource_status.get('details')}"
                }
             return {
                "status": "conflict",
                "target": str(target),
                "reason": f"Resources conflict: {resource_status.get('details')}"
            }
        
        if dry_run:
            return {"status": "dry-run", "target": str(target), "would_conflict": False}
        
        # Ensure parent directory exists
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Transform and write (Core Instruction)
        content = self.transform(skill)
        target.write_text(content)
        
        # Install resources (if any)
        self.install_resources(skill, target.parent, dry_run=False)
        
        return {"status": "copied", "target": str(target)}

    def remove_skill(self, skill: Dict, name: str = None) -> Dict:
        """
        Remove a skill from the agent's directory.
        
        Args:
            skill: Skill dictionary (must at least contain 'name')
            name: Optional specific name (overrides skill['name'])
            
        Returns:
            status dict with: status ('removed', 'not_found', 'error'), target
        """
        name_to_use = name or skill.get("name")
        target = self.get_target_path(skill, name_to_use)
        
        if not target.exists():
            return {"status": "not_found", "target": str(target)}
            
        try:
            if target.is_dir():
                import shutil
                shutil.rmtree(target)
            else:
                target.unlink()
            return {"status": "removed", "target": str(target)}
        except Exception as e:
            return {"status": "error", "error": str(e), "target": str(target)}
