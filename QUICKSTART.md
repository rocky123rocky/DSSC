# Quick Start Guide - DSSC COPP AHP Military Planner

## Installation & First Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Access the Application**
   - Open your browser to: http://localhost:8501
   - You should see the login page with three force options

## First Login

### Default Credentials
- **Control**: PIN `9999` (Administrator access)
- **Blue Force**: PIN `2222` (Blue team access)
- **Red Force**: PIN `1111` (Red team access)

⚠️ **Security Note**: Change these default PINs immediately in the Control Panel!

## Control Panel Features

After logging in as Control, navigate to "Control Panel" from the sidebar.

### Available Features:

1. **RAG Threshold Configuration**
   - Red Threshold slider (0-100)
   - Amber Threshold slider (0-100)
   - Used for performance monitoring

2. **PIN Management**
   - Control PIN input field
   - Blue Force PIN input field
   - Red Force PIN input field
   - "Save All PINs" button to update

3. **AHP Team Credits Management** *(NEW!)*
   - Edit team member names
   - Edit team member roles
   - Add new members with "Add Member" button
   - Save changes with "Save Credits" button

### How to Edit Team Credits

1. Log in with Control credentials (default PIN: 9999)
2. Select "Control Panel" from the sidebar
3. Scroll down to "AHP Team Credits" section
4. Edit existing member names and roles in the text fields
5. Click "Add Member" to add a new team member
6. Click "Save Credits" to persist your changes

### Default Team Members
- Cdr A Kumar - Lead Architect
- Lt B Singh - Backend Developer
- Lt C Sharma - Frontend Developer
- Lt D Patel - Testing & QA

## Navigation Overview

### Control User Navigation
- Phases
- Objectives
- Decisive Points
- Tasks
- Progress Entry
- Dashboard
- **Control Panel** ⭐
- Force Manager
- Project Management
- Logout

### Blue/Red Force Navigation
- Phases
- Objectives
- Decisive Points
- Tasks
- KO Method
- Project Management
- Logout

## Project Management

All users can access Project Management to:
- Switch between projects
- Create new projects
- Archive/delete projects
- Export project data (JSON/ZIP)

## Data Storage

- Projects are stored in the `projects/` directory
- Each force has its own JSON file: `{project_name}/{force}.json`
- Data includes: phases, objectives, decisive points (DPs), and tasks

## Tips

1. **Create a New Project**: Use Project Management to create projects for different operations
2. **Multi-Force Planning**: Control users can see all forces' data for comparison
3. **Regular Backups**: Export projects regularly using the export feature
4. **Update PINs**: Change default PINs for security
5. **Team Credits**: Keep team information up-to-date in the Control Panel

## Troubleshooting

**Issue**: Application won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Can't login
- **Solution**: Check you're using the correct default PINs (9999, 2222, 1111)

**Issue**: Data not saving
- **Solution**: Ensure the `projects/` directory has write permissions

**Issue**: Changes not appearing
- **Solution**: Click the appropriate "Save" button after making changes

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/rocky123rocky/DSSC/issues
- Check the README.md for detailed documentation

---

⚓ NAVAL WING, DSSC Wellington
