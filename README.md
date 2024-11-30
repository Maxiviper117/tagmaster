# TagMaster

## Description

TagMaster is an interactive CLI tool for managing project tags.

TagMaster aggregates empty tag files within your code projects, making it easier to find and organize projects by those tags using tools like fzf or the Everything search tool.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Maxiviper117/tagmaster.git
    ```
2. Navigate to the project directory:
    ```bash
    cd tagmaster
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start TagMaster, run:
```bash
python tagger.py
```

**Important:** Before running the CLI, ensure you have navigated to your project's root directory:
```bash
cd /path/to/your/project
python tagger.py
```

## Building the Executable

To build the executable, run the build script:

```bash
python build-scripts/build.py
```

### Prerequisites

Ensure that `auto-py-to-exe` is installed:

```bash
pip install auto-py-to-exe
```

### Steps

1. **Navigate to the Project Directory**:
    ```bash
    cd tagmaster
    ```

2. **Activate Your Virtual Environment** (if applicable):
    ```bash
    source .venv/bin/activate  # On Unix or macOS
    .venv\Scripts\activate     # On Windows
    ```

3. **Run the Build Script**:
    ```bash
    python build-scripts/build.py
    ```

4. **Locate the Executable**:
    The executable will be generated in the `dist` directory.

    ```bash
    ls dist/
    ```

5. **Add to System PATH** (optional):
    Follow the existing instructions to add the executable to your system's PATH for easy access.

### Adding to System PATH

1. **Locate the Executable**: Find the `tagger.exe` file in the `dist` folder.
2. **Add to PATH**:
    - **Windows**:
        - Open the Start menu and search for "Environment Variables".
        - Click on "Edit the system environment variables".
        - In the System Properties window, click the "Environment Variables" button.
        - Under "System variables", find and select the `Path` variable, then click "Edit".
        - Click "New" and add the path to the `dist` directory.
        - Click "OK" on all windows to apply the changes.
    - **macOS/Linux**:
        - Open your terminal.
        - Edit your shell profile file (e.g., `.bashrc`, `.zshrc`) and add the following line:
            ```bash
            export PATH="$PATH:/path/to/project-tagger/dist"
            ```
        - Save the file and run `source ~/.bashrc` or `source ~/.zshrc` to apply changes.

3. **Verify**: Open a new terminal window and run `tagger` to ensure it's accessible from anywhere.

## Features

- **Add Tag**: Add a new tag to your project.
  When you add a tag, an empty tag file is created in the `tags` directory, allowing you to organize and manage project tags effectively.
- **List Tags**: View all existing tags.
- **Remove Tag**: Delete a specific tag.
- **Clear All Tags**: Remove all tags from the project.
- **Exit**: Exit the application.

## License

MIT License
