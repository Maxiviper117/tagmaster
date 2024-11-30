import os
import sys
import subprocess
import click
import questionary
from colorama import Fore, Style, init

# Set the console code page to UTF-8 on Windows to handle emojis
if os.name == 'nt':
    import ctypes
    # Set the console output and input code page to UTF-8
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    ctypes.windll.kernel32.SetConsoleCP(65001)

# Initialize Colorama
init(autoreset=True)

# Constants
TAGS_FOLDER = "tags"
TAG_EXTENSION = ".tag"

# Define default tags
DEFAULT_TAGS = [
    "local-git-repo",
    "published-git-repo",
    "python",
    "typescript",
    "react",
    "nodejs"
]

# Define menu options with emojis
MENU_OPTIONS = [
    "✨ Add Tag",
    "📋 List Tags",
    "❌ Remove Tag",
    "🧹 Clear All Tags",
    "🚪 Exit"
]

def get_tags_folder(path):
    """
    Ensure the tags folder exists and return its absolute path.
    """
    tags_path = os.path.join(os.path.abspath(path), TAGS_FOLDER)
    if not os.path.exists(tags_path):
        os.makedirs(tags_path)
    return tags_path

def add_tag(tags_path, tag):
    """
    Add a new tag by creating an empty tag file.
    """
    tag_file = os.path.join(tags_path, f"{tag}{TAG_EXTENSION}")
    if not os.path.exists(tag_file):
        with open(tag_file, 'w', encoding='utf-8') as f:
            pass  # Create an empty file
        click.echo(f"{Fore.GREEN}✅ Tag '{tag}' added successfully.")
    else:
        click.echo(f"{Fore.YELLOW}⚠️  Tag '{tag}' already exists.")

def list_tags(tags_path):
    """
    List all existing tags and pause before returning to the menu.
    """
    try:
        tags = [f[:-len(TAG_EXTENSION)] for f in os.listdir(tags_path) if f.endswith(TAG_EXTENSION)]
    except FileNotFoundError:
        tags = []

    if tags:
        click.echo(f"{Fore.CYAN}📋 Tags found in '{TAGS_FOLDER}':")
        for tag in tags:
            click.echo(f"{Fore.BLUE}- {tag}")
    else:
        click.echo(f"{Fore.RED}❌ No tags found in '{TAGS_FOLDER}'.")

    # Pause to allow the user to read the tags
    input(f"\n{Fore.GREEN}Press Enter to return to the main menu...")

def remove_tag(tags_path, tag):
    """
    Remove a specific tag by deleting its tag file.
    """
    tag_file = os.path.join(tags_path, f"{tag}{TAG_EXTENSION}")
    if os.path.exists(tag_file):
        os.remove(tag_file)
        click.echo(f"{Fore.GREEN}✅ Tag '{tag}' removed successfully.")
    else:
        click.echo(f"{Fore.RED}❌ Tag '{tag}' does not exist.")

def clear_tags(tags_path):
    """
    Clear all tags by deleting all tag files in the tags folder.
    """
    try:
        tag_files = [f for f in os.listdir(tags_path) if f.endswith(TAG_EXTENSION)]
    except FileNotFoundError:
        tag_files = []

    if not tag_files:
        click.echo(f"{Fore.RED}❌ No tags to clear in '{TAGS_FOLDER}'.")
        return

    # Confirmation prompt
    confirm = questionary.confirm(
        f"Are you sure you want to delete all {len(tag_files)} tag(s)? This action cannot be undone."
    ).ask()

    if confirm:
        for tag_file in tag_files:
            os.remove(os.path.join(tags_path, tag_file))
        click.echo(f"{Fore.GREEN}✅ Cleared {len(tag_files)} tag(s).")
    else:
        click.echo(f"{Fore.YELLOW}⚠️  Clear tags operation canceled.")

def use_fzf(options, multi=False):
    """
    Use fzf for selecting options. Fallback to Questionary if fzf is unavailable.
    Supports single or multiple selections based on the 'multi' parameter.
    """
    try:
        fzf_command = ["fzf"]
        if multi:
            fzf_command.append("--multi")  # Enable multi-selection

        result = subprocess.run(
            fzf_command,
            input="\n".join(options),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',  # Explicitly set encoding to UTF-8
            errors='replace'    # Replace characters that can't be encoded/decoded
        )
        if result.returncode == 0:
            selections = result.stdout.strip().split('\n') if multi else [result.stdout.strip()]
            # Remove any empty selections
            selections = [sel for sel in selections if sel]
            return selections
        else:
            return []
    except FileNotFoundError:
        if multi:
            # For multi-selection fallback, use questionary's checkbox
            click.echo(f"{Fore.YELLOW}⚠️  fzf not found. Falling back to Questionary for multi-selection.")
            return questionary.checkbox("Select tags to add:", choices=options).ask() or []
        else:
            click.echo(f"{Fore.YELLOW}⚠️  fzf not found. Falling back to Questionary.")
            selection = questionary.select("Select an option:", choices=options).ask()
            return [selection] if selection else []

def add_tags(tags_path):
    """
    Handle adding tags with a sub-menu to choose between custom or default tags.
    """
    # Define sub-menu options with emojis
    ADD_TAG_OPTIONS = [
        "🆕 Add a Custom Tag",
        "📌 Select from Default Tags",
        "🔙 Return to Main Menu"
    ]

    # Prompt user to choose between adding custom or selecting default tags
    choice = questionary.select(
        "How would you like to add a tag?",
        choices=ADD_TAG_OPTIONS
    ).ask()

    if not choice or choice == "🔙 Return to Main Menu":
        return

    if choice == "🆕 Add a Custom Tag":
        while True:
            custom_tag = questionary.text("Enter the name of the custom tag (or leave empty to stop):").ask()
            if custom_tag:
                custom_tag = custom_tag.strip()
                if custom_tag:
                    add_tag(tags_path, custom_tag)
                else:
                    click.echo(f"{Fore.RED}❌ Tag name cannot be empty.")
            else:
                break

    elif choice == "📌 Select from Default Tags":
        # Prompt user to select multiple tags using fzf or Questionary
        selected_tags = use_fzf(DEFAULT_TAGS, multi=True)
        if not selected_tags:
            click.echo(f"{Fore.RED}❌ No tags selected.")
            return

        for tag in selected_tags:
            add_tag(tags_path, tag)

def remove_tags(tags_path):
    """
    Handle removing tags using fzf or Questionary.
    """
    try:
        tags = [f[:-len(TAG_EXTENSION)] for f in os.listdir(tags_path) if f.endswith(TAG_EXTENSION)]
    except FileNotFoundError:
        tags = []

    if not tags:
        click.echo(f"{Fore.RED}❌ No tags available to remove.")
        return

    # Prompt user to select tags to remove using fzf or Questionary (multi-select enabled)
    tags_to_remove = use_fzf(tags, multi=True)
    if not tags_to_remove:
        click.echo(f"{Fore.RED}❌ No tags selected for removal.")
        return

    # Remove selected tags
    for tag in tags_to_remove:
        remove_tag(tags_path, tag)

@click.command()
@click.option('--path', default='.', help="Path to the project directory.")
def cli(path):
    """
    Interactive CLI tool for managing project tags.
    """
    tags_path = get_tags_folder(path)

    while True:
        # Display the interactive menu using Questionary's select with emojis
        action = questionary.select(
            "Select an action:",
            choices=MENU_OPTIONS
        ).ask()

        if not action:
            click.echo(f"{Fore.RED}❌ No selection made. Exiting...")
            sys.exit(0)

        if action == "✨ Add Tag":
            add_tags(tags_path)

        elif action == "📋 List Tags":
            list_tags(tags_path)  # List tags directly, no fzf integration here

        elif action == "❌ Remove Tag":
            remove_tags(tags_path)

        elif action == "🧹 Clear All Tags":
            clear_tags(tags_path)

        elif action == "🚪 Exit":
            click.echo(f"{Fore.GREEN}👋 Goodbye!")
            sys.exit(0)

        else:
            click.echo(f"{Fore.RED}❌ Invalid action selected.")

if __name__ == '__main__':
    cli()
