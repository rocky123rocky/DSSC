import json
import os
import shutil
from datetime import datetime

# Default structure for a new project/force
DEFAULT_STRUCTURE = {
    "phases": [],
    "objectives": [],
    "dps": [],
    "tasks": []
}

def list_projects():
    """List all available projects."""
    projects_dir = "projects"
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)
        # Create a default project
        for side in ["blue", "red"]:
            save_project("Default", side, DEFAULT_STRUCTURE)
    projects = set()
    for filename in os.listdir(projects_dir):
        if filename.endswith(".json"):
            project_name = filename.rsplit("_", 1)[0]
            projects.add(project_name)
    return sorted(list(projects)) if projects else ["Default"]

def load_project(name, side):
    """Load project data for a specific side."""
    filepath = f"projects/{name}_{side}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return DEFAULT_STRUCTURE.copy()

def save_project(name, side, data):
    """Save project data for a specific side."""
    if not os.path.exists("projects"):
        os.makedirs("projects")
    filepath = f"projects/{name}_{side}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def archive_project(name):
    """Archive a project."""
    archive_dir = "projects/archive"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for filename in os.listdir("projects"):
        if filename.startswith(name + "_") and filename.endswith(".json"):
            src = f"projects/{filename}"
            dst = f"{archive_dir}/{timestamp}_{filename}"
            shutil.move(src, dst)

def delete_project(name):
    """Delete a project."""
    for filename in os.listdir("projects"):
        if filename.startswith(name + "_") and filename.endswith(".json"):
            os.remove(f"projects/{filename}")

def export_project_json(name, side):
    """Export project data as JSON."""
    filepath = f"projects/{name}_{side}.json"
    return filepath

def export_project_zip(name):
    """Export entire project as ZIP."""
    import zipfile
    zip_path = f"projects/{name}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for filename in os.listdir("projects"):
            if filename.startswith(name + "_") and filename.endswith(".json"):
                zipf.write(f"projects/{filename}", filename)
    return zip_path

def import_excel_to_project(name, side, excel_path):
    """Import Excel data to project."""
    # Placeholder implementation
    # In real implementation, you would parse Excel and update project data
    pass

def compute_progress(data):
    """Compute progress metrics for a project."""
    progress = {"dp": {}, "objective": {}, "phase": {}}
    
    # Compute DP progress
    for dp in data.get("dps", []):
        dp_no = dp.get("DP No")
        tasks = [t for t in data.get("tasks", []) if t.get("DP No") == dp_no]
        if tasks:
            total_progress = sum([t.get("Achieved %", 0) for t in tasks])
            progress["dp"][dp_no] = total_progress / len(tasks)
        else:
            progress["dp"][dp_no] = 0
    
    return progress
