
import os
import json
import pandas as pd
import zipfile
from datetime import datetime

FORCES_FILE = "forces.json"
def load_forces():
    if os.path.exists(FORCES_FILE):
        with open(FORCES_FILE, "r") as f:
            return json.load(f)
    return ["blue", "red"]

PROJECTS_DIR = "projects"
ARCHIVE_DIR = "archive"

os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

SIDES = load_forces()

DEFAULT_METADATA = {
    "name": "",
    "description": "",
    "status": "active",
    "created": "",
    "modified": ""
}

DEFAULT_STRUCTURE = {
    "metadata": DEFAULT_METADATA.copy(),
    "phases": [],
    "objectives": [],
    "dps": [],
    "tasks": [],
    "ko": {},
    "progress": {},
    "control": {}
}

def get_project_path(project_name, side):
    return os.path.join(PROJECTS_DIR, f"{project_name}_{side}.json")

def get_archive_path(project_name, side):
    return os.path.join(ARCHIVE_DIR, f"{project_name}_{side}.json")

def list_projects():
    files = os.listdir(PROJECTS_DIR)
    projects = set()
    for f in files:
        if f.endswith(".json"):
            name = f.split("_")[0]
            projects.add(name)
    return sorted(list(projects))

def load_project(project_name, side):
    path = get_project_path(project_name, side)
    if not os.path.exists(path):
        data = DEFAULT_STRUCTURE.copy()
        data["metadata"] = DEFAULT_METADATA.copy()
        data["metadata"]["name"] = project_name
        data["metadata"]["created"] = datetime.now().isoformat()
        save_project(project_name, side, data)
    with open(path, "r") as f:
        return json.load(f)

def save_project(project_name, side, data):
    data["metadata"]["modified"] = datetime.now().isoformat()
    path = get_project_path(project_name, side)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def archive_project(project_name):
    for side in SIDES:
        src = get_project_path(project_name, side)
        dst = get_archive_path(project_name, side)
        if os.path.exists(src):
            os.replace(src, dst)

def delete_project(project_name):
    for side in SIDES:
        path = get_project_path(project_name, side)
        if os.path.exists(path):
            os.remove(path)

def export_project_json(project_name, side):
    data = load_project(project_name, side)
    path = f"{project_name}_{side}_export.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def export_project_excel(project_name, side):
    data = load_project(project_name, side)
    writer = pd.ExcelWriter(f"{project_name}_{side}_export.xlsx", engine="openpyxl")
    for key in ["phases", "objectives", "dps", "tasks"]:
        df = pd.DataFrame(data.get(key, []))
        df.to_excel(writer, sheet_name=key.capitalize(), index=False)
    writer.save()
    return writer.path

def export_project_zip(project_name):
    files = []
    for side in SIDES:
        json_path = export_project_json(project_name, side)
        excel_path = export_project_excel(project_name, side)
        files.extend([json_path, excel_path])
    zip_path = f"{project_name}_export.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in files:
            zipf.write(f)
    for f in files:
        os.remove(f)
    return zip_path

def import_excel_to_project(project_name, side, excel_path):
    data = load_project(project_name, side)
    xls = pd.ExcelFile(excel_path)
    sheet_map = {
        "phases": ["Phases", "Phase", "phases", "phase"],
        "objectives": ["Objectives", "Objective", "objectives", "objective"],
        "dps": ["DPs", "DP", "dps", "dp"],
        "tasks": ["Tasks", "Task", "tasks", "task"]
    }
    for key, variants in sheet_map.items():
        found = None
        for sheet in xls.sheet_names:
            if sheet.lower() in [v.lower() for v in variants]:
                found = sheet
                break
        if found:
            df = pd.read_excel(xls, found)
            data[key] = df.to_dict(orient="records")
    save_project(project_name, side, data)

def compute_progress(data):
    # Aggregates DP, Objective, and Phase progress using task achieved % and intangible values
    dp_progress = {}
    for dp in data.get("dps", []):
        dp_no = dp.get("DP No")
        tasks = [t for t in data.get("tasks", []) if t.get("DP No") == dp_no]
        if not tasks:
            dp_progress[dp_no] = 0
            continue
        total = 0
        for t in tasks:
            achieved = t.get("Achieved %", 0)
            intangible = t.get("Intangible", "nil")
            if intangible == "complete":
                achieved = 100
            elif intangible == "partial":
                achieved = max(achieved, 50)
            total += achieved
        dp_progress[dp_no] = total / len(tasks)
    # Objective progress
    obj_progress = {}
    for obj in data.get("objectives", []):
        obj_name = obj.get("Name")
        dps = [dp for dp in data.get("dps", []) if dp.get("Objective") == obj_name]
        if not dps:
            obj_progress[obj_name] = 0
            continue
        total = sum([dp_progress.get(dp.get("DP No"), 0) for dp in dps])
        obj_progress[obj_name] = total / len(dps)
    # Phase progress
    phase_progress = {}
    for phase in data.get("phases", []):
        phase_name = phase.get("Name")
        objs = [obj for obj in data.get("objectives", []) if obj.get("Phase") == phase_name]
        if not objs:
            phase_progress[phase_name] = 0
            continue
        total = sum([obj_progress.get(obj.get("Name"), 0) for obj in objs])
        phase_progress[phase_name] = total / len(objs)
    return {
        "dp": dp_progress,
        "objective": obj_progress,
        "phase": phase_progress
    }
