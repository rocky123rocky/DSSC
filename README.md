# DSSC - COPP AHP Military Planner

## Important Information

This is the DSSC (Defence Services Staff College) COPP AHP Military Planner application.

## Overview

DSSC is a Streamlit-based military planning application designed for COPP (Combined Operational Planning Process) using AHP (Analytical Hierarchy Process) methodology. It provides comprehensive tools for military planning across multiple forces.

## Features

- **Multi-Force Planning**: Support for Blue Force and Red Force planning
- **Phase Management**: Define and manage operational phases
- **Objectives Tracking**: Set and monitor objectives across forces
- **Decisive Points (DPs)**: Identify and manage decisive points
- **Task Management**: Create and track tasks with progress monitoring
- **KO Method Analysis**: Apply Knockout method for decision making
- **Control Panel**: Centralized control for administrators
  - PIN management for all forces
  - AHP Team Credits editing
  - RAG (Red/Amber/Green) threshold configuration
- **Project Management**: Create, archive, and export projects
- **Dashboard**: Real-time monitoring and analytics

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/rocky123rocky/DSSC.git
cd DSSC

# Install dependencies
pip install -r requirements.txt
```

### Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Default Login Credentials

- **Control**: PIN `9999`
- **Blue Force**: PIN `2222`
- **Red Force**: PIN `1111`

**Note**: Change these PINs immediately in the Control Panel after first login.

## Application Structure

### User Roles

1. **Control**: Administrator role with full access
   - All force data visibility
   - PIN management
   - Team credits management
   - Progress entry
   - Dashboard access

2. **Blue Force**: Blue team planning access
   - Own force data management
   - KO method analysis

3. **Red Force**: Red team planning access
   - Own force data management
   - KO method analysis

### Key Features

#### Control Panel (Control Role Only)

The Control Panel provides administrative functions:

- **RAG Thresholds**: Configure Red/Amber/Green performance thresholds
- **PIN Management**: Set and update PINs for all forces
- **AHP Team Credits**: Manage team member information
  - Add/edit team members
  - Update roles and names
  - Save changes to persistent storage

#### Project Management

- Create new projects
- Switch between projects
- Archive existing projects
- Delete projects
- Export project data (JSON/ZIP)

## Development

### Project Structure

```
DSSC/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── projects/          # Project data storage (auto-created)
```

### Data Storage

Project data is stored in JSON format under `projects/{project_name}/{force}.json`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Please see the LICENSE file for details.

## Contact

For questions or support, please open an issue in this repository.

## Credits

**AHP Team** (Editable in Control Panel):
- Cdr A Kumar - Lead Architect
- Lt B Singh - Backend Developer
- Lt C Sharma - Frontend Developer
- Lt D Patel - Testing & QA

---

⚓ NAVAL WING, DSSC Wellington