# Quick Start Guide - COPP AHP Military Planner

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

## Default Credentials

- **Control**: PIN `9999`
- **Blue Force**: PIN `2222`
- **Red Force**: PIN `1111`

## Accessing AHP Team Credits

### Method 1: Control Panel (Recommended for Editing)
1. Login as Control (PIN: 9999)
2. Click "Control Panel" in the sidebar
3. Scroll to "AHP Team Credits" section
4. Edit team member names and roles
5. Click "Add Member" to add new members
6. Click "Save Credits" to save changes

### Method 2: Login Modal (Quick View)
1. On the login page, click "AHP Team Credits" button
2. View/edit team credits in the popup modal
3. Control users can edit, others see read-only view

## Key Features Implemented

✅ AHP Team Credits in Control Panel
- Visual separator line
- Clear "AHP Team Credits" subheader
- Editable name and role fields
- Add new team members
- Save changes to session state

✅ Default Team Members
- Cdr A Kumar - Lead Architect
- Lt B Singh - Backend Developer
- Lt C Sharma - Frontend Developer
- Lt D Patel - Testing & QA

## File Structure

```
DSSC/
├── app.py                      # Main Streamlit application
├── ahp_backend.py             # Backend helper functions
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore patterns
├── IMPLEMENTATION_SUMMARY.md  # Detailed documentation
├── QUICK_START.md            # This file
└── README.md                 # Project readme
```

## Navigation Menu

### For All Users:
- Phases
- Objectives
- Decisive Points
- Tasks
- KO Method
- Project Management
- Logout

### Control Users Only:
- Progress Entry
- Dashboard
- Control Panel ← **AHP Team Credits is here**
- Force Manager

## Troubleshooting

**Q: I can't see the Control Panel menu option**
A: Make sure you logged in with Control credentials (PIN: 9999)

**Q: Changes to team credits are not saving**
A: Click the "Save Credits" button after making changes

**Q: I see duplicate widget errors**
A: The implementation uses unique keys (_cp suffix) to prevent conflicts

## Support

For issues or questions, please refer to IMPLEMENTATION_SUMMARY.md for detailed technical documentation.
