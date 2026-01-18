"""Copy command - Copy skills to agent directories."""

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from ask.utils.skill_registry import get_skill, get_all_skills
from ask.utils.filesystem import get_adapter
from ask.utils.agent_registry import get_available_agents, get_agent_scopes

console = Console()


@click.command()
@click.argument("agent", type=click.Choice(get_available_agents(), case_sensitive=False))
@click.option("--skill", "-s", "skill_name", help="Specific skill to copy")
@click.option("--all", "-a", "copy_all", is_flag=True, help="Copy all compatible skills")
def copy(agent: str, skill_name: str, copy_all: bool):
    """Copy skills to an agent's directory.
    
    AGENT is the target agent (discovered from agents/ folder).
    
    Shows preview of both local and global paths, then asks which to use.
    Safe Copy: Never overwrites. Prompts for new name on conflict.
    
    Examples:
    
        ask copy codex --skill python-refactor
        
        ask copy gemini --skill my-skill
        
        ask copy claude --all
    """
    if not skill_name and not copy_all:
        console.print("[red]❌ Specify --skill <name> or --all[/red]")
        raise click.Abort()
    
    # Get skills to copy
    if copy_all:
        skills = [s for s in get_all_skills() if agent in s.get("agents", [])]
        if not skills:
            console.print(f"[yellow]No skills found compatible with {agent}[/yellow]")
            return
    else:
        skill = get_skill(skill_name)
        if not skill:
            console.print(f"[red]❌ Skill not found: {skill_name}[/red]")
            raise click.Abort()
        
        if agent not in skill.get("agents", []):
            console.print(f"[yellow]⚠️  Skill '{skill_name}' doesn't list '{agent}' as a supported agent.[/yellow]")
            if not click.confirm("Copy anyway?"):
                raise click.Abort()
        
        skills = [skill]
    
    # Get supported scopes for this agent
    scopes = get_agent_scopes().get(agent, {"local": True, "global": True})
    
    # Show dry run preview for available options
    console.print(f"\n[bold]📦 Preview: Copying {len(skills)} skill(s) to {agent}[/bold]\n")
    
    # Build preview table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Skill")
    
    if scopes["local"]:
        table.add_column("Local (project)", style="cyan")
    if scopes["global"]:
        table.add_column("Global (user)", style="green")
    
    for skill in skills:
        row = [skill["name"]]
        
        if scopes["local"]:
            adapter = get_adapter(agent, use_global=False)
            target = adapter.get_target_path(skill)
            exists = target.exists()
            status = f"[yellow](exists)[/yellow]" if exists else ""
            row.append(f"{target} {status}")
        
        if scopes["global"]:
            adapter = get_adapter(agent, use_global=True)
            target = adapter.get_target_path(skill)
            exists = target.exists()
            status = f"[yellow](exists)[/yellow]" if exists else ""
            row.append(f"{target} {status}")
        
        table.add_row(*row)
    
    console.print(table)
    console.print()
    
    # Ask user to choose scope with numbered options
    console.print("[bold]Choose destination:[/bold]")
    console.print("  [dim]0[/dim] Cancel")
    if scopes["global"]:
        console.print("  [green]1[/green] Global (user home directory)")
    if scopes["local"]:
        console.print("  [cyan]2[/cyan] Local (project directory)")
    
    # Build valid choices
    valid_choices = ["0"]
    if scopes["global"]:
        valid_choices.append("1")
    if scopes["local"]:
        valid_choices.append("2")
    
    default = "2" if scopes["local"] else "1"
    
    choice_num = Prompt.ask(
        "Enter choice",
        choices=valid_choices,
        default=default
    )
    
    # Map number to action
    if choice_num == "0":
        console.print("[yellow]Cancelled.[/yellow]")
        raise click.Abort()
    elif choice_num == "1":
        use_global = True
        scope_name = "global"
    else:  # "2"
        use_global = False
        scope_name = "local"
    
    # Get adapter for chosen scope
    adapter = get_adapter(agent, use_global=use_global)
    
    # Copy skills
    console.print(f"\n[bold]Copying to {scope_name}...[/bold]\n")
    
    success_count = 0
    skip_count = 0
    
    for skill in skills:
        try:
            result = adapter.copy_skill(skill)
            
            if result["status"] == "copied":
                console.print(f"  [green]✓[/green] {skill['name']} → {result['target']}")
                success_count += 1
            elif result["status"] == "conflict":
                # Prompt user for new name
                console.print(f"  [yellow]⚠️  '{skill['name']}' already exists[/yellow]")
                
                new_name = Prompt.ask(
                    "    Enter new name (or 'skip')",
                    default="skip"
                )
                
                if new_name.lower() == "skip":
                    console.print(f"  [yellow]○[/yellow] {skill['name']} skipped")
                    skip_count += 1
                else:
                    # Copy with new name
                    result = adapter.copy_skill(skill, new_name=new_name)
                    if result["status"] == "copied":
                        console.print(f"  [green]✓[/green] {skill['name']} → {result['target']}")
                        success_count += 1
                    else:
                        console.print(f"  [red]✗[/red] Failed: {result.get('error', 'Unknown')}")
                        
        except Exception as e:
            console.print(f"  [red]✗[/red] {skill['name']}: {e}")
    
    # Summary
    console.print()
    console.print(f"[green]Done![/green] {success_count} copied, {skip_count} skipped.")
