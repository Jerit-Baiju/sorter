Here's the updated README with your contact information and GitHub link:

---

# Sorter

Sorter is a Python-based automation tool designed to organize files from a source directory into structured folders based on file types and date patterns in their filenames. This tool is ideal for managing large volumes of unsorted files, such as images, videos, documents, and chat logs.

## Overview

The Sorter project automates the process of organizing files by scanning filenames for recognizable patterns and categorizing them accordingly. This helps users efficiently maintain organized folders, particularly when dealing with a high volume of media files with various naming conventions.

### Purpose

The main purpose of Sorter is to streamline file management by:
- Identifying common date patterns within filenames.
- Categorizing files into specific types (e.g., images, screenshots, documents).
- Organizing files by year and month for easy retrieval.

This project can be helpful for anyone looking to automate their file organization workflow, especially for media-heavy or documentation-intensive environments.

## Features

- **Automated Organization**: Moves files from a source directory into destination folders based on patterns in their filenames.
- **Date-Based Sorting**: Extracts dates from filenames and organizes files into a structured year/month directory layout.
- **File Type Detection**: Identifies and categorizes files based on common file extensions and naming conventions (e.g., screenshots, documents, call records).
- **Chat Log Organization**: Special handling for `.txt` files assumed to contain chat logs, breaking down messages by date for easy review.

## How It Works

The script works by iterating over each file in a specified source directory (`SOURCE_DIR`). Here’s a step-by-step of the main logic:

1. **File Identification**: For each file in `SOURCE_DIR`, Sorter:
   - Skips hidden files and non-standard files.
   - Applies predefined date patterns and file type checks.
   
2. **Date Parsing and Directory Creation**:
   - Extracts the date from each file’s name using a series of predefined patterns.
   - Creates folders based on the year and month of the extracted date.

3. **File Categorization**:
   - Determines the type of file (e.g., "Screenshots," "Videos") based on extensions and keywords.
   - Moves each file to its designated folder within a structured layout in `DESTINATION_DIR`.

4. **Chat File Handling**:
   - For `.txt` files, Sorter assumes they are chat logs.
   - Organizes messages within the chat file by date and saves each date’s messages into a separate file.

5. **Logging and Summary**:
   - At the end, Sorter provides a summary of files moved, files already existing in destination folders, file types processed, and months processed.

## Setup and Usage

### Prerequisites

- Python 3.x
- `shutil` and `os` (included in Python's standard library)

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/Jerit-Baiju/sorter.git
cd sorter
```

### Configurations

In the script, adjust the following variables based on your needs:

- `SOURCE_DIR`: Path to the folder containing unsorted files.
- `DESTINATION_DIR`: Path to the folder where files will be organized.

### Running the Script

To execute the sorting script, run:

```bash
python sorter.py
```

The script will:
- Move files from `SOURCE_DIR` to `DESTINATION_DIR`.
- Print a summary of files moved, duplicates encountered, file types sorted, and months organized.

### Example Folder Structure

Once the script is executed, files will be organized in the following structure:

```
DESTINATION_DIR/
├── 2024/
│   ├── January/
│   │   ├── Screenshots/
│   │   ├── Documents/
│   │   └── .p/
│   └── February/
│       ├── Videos/
│       └── Voice Notes/
└── 2023/
    └── ...
```

## Documentation

### Customization

You can customize the script further by editing the `timestamp` variables to add or modify filename patterns. For example, if you have a unique naming convention for certain files, add those patterns to the `timestamp` lists.

### Error Handling

- The script catches and logs common errors, such as missing date patterns or incorrect file types, without terminating the entire sorting process.

### Debugging

If you encounter an "unknown error" in the logs, check for unsupported file naming conventions and modify the script accordingly to recognize new patterns.

## Contributions

If you'd like to contribute:
1. Fork the repository.
2. Create a new branch with your feature or bug fix.
3. Submit a pull request detailing your changes.

## Contact

For any questions or support, please contact Jerit Baiju:

- **Email**: [sorter@jerit.in](mailto:sorter@jerit.in)
- **Website**: [https://Jerit.in](https://Jerit.in)

--- 

This README now includes all essential information, project overview, usage instructions, and your contact details for easy access by contributors and users.