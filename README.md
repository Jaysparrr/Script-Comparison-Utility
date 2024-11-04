
---
# Python Script Comparator Utility (SCU)

**SCU** is a standalone utility designed to compare differences between multiple files in a folder, such as Python files or files of other specified extensions. This tool is ideal for tracking changes in sequential versions of files, highlighting additions and removals for easy comparison.

## Features

- **Sequential File Comparison**: Compares each file in a folder to the previous one, tracking only adjacent changes.
- **Visual Difference Display**: Highlights additions in green and removals in red for quick and clear differentiation.
- **Filter Options**: Allows users to selectively view only additions, only removals, or both.
- **Log Output and Export**: Displays a detailed comparison log with an option to save it as a `.txt` file.
- **Graphical Interface**: User-friendly GUI with easy navigation for selecting folders, filtering results, and saving logs.

## Installation

No installation is required! Simply download the executable (`scu.exe`) and double-click to run the utility. **No Python environment is needed** to use this tool.

## Usage

1. **Open the Application**: Double-click `scu.exe` to launch the GUI.
2. **Select Folder**: Use the folder selection option to choose a directory containing the files you want to compare.
3. **Choose File Extension**: Use the dropdown menu to specify the file extension to compare (e.g., `.py`, `.txt`, `.md`).
4. **Set Filtering Options**: Select your preference to show additions, removals, or both.
5. **View Differences**: SCU will display differences in a new window, color-coded for easy reference.
6. **Save Log**: Optionally, click "Save Log" to export the comparison results as a `.txt` file.

## Example Workflow

1. **Launch SCU** by double-clicking the executable.
2. **Choose the Folder**: Select the folder containing files to compare.
3. **Select Options**:
   - File Extension: Choose the file type you want to compare.
   - Filtering: Set whether to show additions, removals, or both.
4. **Save the Comparison Log** if needed, for easy reference later.

## Troubleshooting

- **No Differences Found**: If no differences are detected, make sure the files have sequential changes, as SCU only compares each file to the immediately previous one.

## License

This project is licensed under the MIT License.

---
