# Spawner Auto-Discovery Fix

## Problem
Auto-discovery loads ALL task files, not just the specified one.

## Solution
### Code Fix for Grind Spawner Unified

To address the issue of dangerous auto-discovery in the grind spawner, we will modify the `grind_spawner_unified.py` script to respect the `--tasks-file` option and disable auto-discovery by default. We will also introduce an optional `--auto-discover` flag for users who want to load all tasks.

#### Current Behavior

The current behavior is not explicitly shown in the provided snippet. However, based on the description, we can assume that the auto-discovery mechanism is currently implemented as follows:
```python
import glob

# Auto-discovery happens somewhere in the code
task_files = glob.glob('grind_tasks_*.json')
```
#### Modified Behavior

To fix the issue, we will modify the script to use the `--tasks-file` option as the primary source of tasks and disable auto-discovery by default. We will also add an optional `--auto-discover` flag.

```python
import argparse
import glob

def main():
    parser = argparse.ArgumentParser(description='Grind Spawner Unified')
    parser.add_argument('--tasks-file', help='Specify a task file to load')
    parser.add_argument('--auto-discover', action='store_true', help='Enable auto-discovery of task files')
    args = parser.parse_args()

    if args.tasks_file:
        # If --tasks-file is specified, ONLY load that file
        task_files = [args.tasks_file]
    elif args.auto_discover:
        # If --auto-discover is specified, load all task files
        task_files = glob.glob('grind_tasks_*.json')
    else:
        # Default behavior: load no tasks if no file is specified and auto-discovery is disabled
        task_files = []

    # Load and process tasks from the specified files
    for task_file in task_files:
        # Load and process tasks from the file
        print(f"Loading tasks from {task_file}")

if __name__ == "__main__":
    main()
```
#### What to Change and Where

1.  **Add `argparse` for argument parsing**: We use the `argparse` library to parse command-line arguments. This allows us to define the `--tasks-file` and `--auto-discover` options.
2.  **Define the `--tasks-file` and `--auto-discover` options**: We add these options to the `ArgumentParser` instance to enable users to specify a task file and toggle auto-discovery.
3.  **Modify the task file loading logic**: We update the code to load task files based on the provided options. If `--tasks-file` is specified, we only load that file. If `--auto-discover` is enabled, we load all task files. Otherwise, we load no tasks by default.
4.  **Remove auto-discovery by default**: By setting `task_files` to an empty list when no file is specified and auto-discovery is disabled, we ensure that the script does not load any tasks by default.

#### Example Usage

To load a specific task file:
```bash
python grind_spawner_unified.py --tasks-file grind_tasks_dashboard.json
```
To enable auto-discovery and load all task files:
```bash
python grind_spawner_unified.py --auto-discover
```
By making these changes, we have made the grind spawner unified script safer and more predictable, while also providing users with the flexibility to choose between loading a specific task file and enabling auto-discovery.