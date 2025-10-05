import os
import json
import zipfile
from datetime import datetime

# Default project structure
DEFAULT_STRUCTURE = {
    "phases": [],
    "objectives": [],
    "dps": [],
    "tasks": []
}

# Project directory
PROJECTS_DIR = "projects"

def ensure_projects_dir():
    """Ensure projects directory exists"""
    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

def list_projects():
    """List all available projects"""
    ensure_projects_dir()
    projects = set()
    if os.path.exists(PROJECTS_DIR):
        for filename in os.listdir(PROJECTS_DIR):
            if filename.endswith('.json'):
                # Extract project name from filename (format: projectname_side.json)
                project_name = '_'.join(filename.split('_')[:-1])
                if project_name:
                    projects.add(project_name)
    return sorted(list(projects)) if projects else ["Demo"]

def load_project(project_name, side):
    """Load project data for a specific side"""
    ensure_projects_dir()
    filepath = os.path.join(PROJECTS_DIR, f"{project_name}_{side}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return DEFAULT_STRUCTURE.copy()

def save_project(project_name, side, data):
    """Save project data for a specific side"""
    ensure_projects_dir()
    filepath = os.path.join(PROJECTS_DIR, f"{project_name}_{side}.json")
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def archive_project(project_name):
    """Archive a project by moving it to archive folder"""
    ensure_projects_dir()
    archive_dir = os.path.join(PROJECTS_DIR, "archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    
    # Move all project files to archive
    for filename in os.listdir(PROJECTS_DIR):
        if filename.startswith(project_name + "_"):
            src = os.path.join(PROJECTS_DIR, filename)
            dst = os.path.join(archive_dir, filename)
            os.rename(src, dst)

def delete_project(project_name):
    """Delete a project and all its files"""
    ensure_projects_dir()
    # Delete all project files
    for filename in os.listdir(PROJECTS_DIR):
        if filename.startswith(project_name + "_"):
            filepath = os.path.join(PROJECTS_DIR, filename)
            os.remove(filepath)

def export_project_json(project_name, side):
    """Export project data as JSON file"""
    ensure_projects_dir()
    export_dir = os.path.join(PROJECTS_DIR, "exports")
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    data = load_project(project_name, side)
    export_path = os.path.join(export_dir, f"{project_name}_{side}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(export_path, 'w') as f:
        json.dump(data, f, indent=2)
    return export_path

def export_project_zip(project_name):
    """Export entire project as ZIP file"""
    ensure_projects_dir()
    export_dir = os.path.join(PROJECTS_DIR, "exports")
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    zip_path = os.path.join(export_dir, f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for filename in os.listdir(PROJECTS_DIR):
            if filename.startswith(project_name + "_"):
                filepath = os.path.join(PROJECTS_DIR, filename)
                zipf.write(filepath, filename)
    return zip_path

def import_excel_to_project(project_name, side, excel_path):
    """Import data from Excel file to project"""
    try:
        import pandas as pd
        
        # Read all sheets from Excel
        excel_data = pd.read_excel(excel_path, sheet_name=None)
        
        data = DEFAULT_STRUCTURE.copy()
        
        # Import phases
        if 'Phases' in excel_data:
            phases_df = excel_data['Phases']
            data['phases'] = phases_df.to_dict('records')
        
        # Import objectives
        if 'Objectives' in excel_data:
            objectives_df = excel_data['Objectives']
            data['objectives'] = objectives_df.to_dict('records')
        
        # Import DPs
        if 'DPs' in excel_data:
            dps_df = excel_data['DPs']
            data['dps'] = dps_df.to_dict('records')
        
        # Import tasks
        if 'Tasks' in excel_data:
            tasks_df = excel_data['Tasks']
            data['tasks'] = tasks_df.to_dict('records')
        
        save_project(project_name, side, data)
    except Exception as e:
        print(f"Error importing Excel: {e}")
