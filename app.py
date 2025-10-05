
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
import json
from ahp_backend import *

st.set_page_config(page_title="COPP AHP Military Planner", layout="wide")

FORCES_FILE = "forces.json"
def load_forces():
    if os.path.exists(FORCES_FILE):
        with open(FORCES_FILE, "r") as f:
            return json.load(f)
    return ["blue", "red"]

def save_forces(sides):
    with open(FORCES_FILE, "w") as f:
        json.dump(sides, f)

SIDES = load_forces()
FORCE_COLORS = {
    "blue": "#1e3a8a",
    "red": "#7f1d1d",
    "yellow": "#facc15",
    "orange": "#fb923c",
    "pink": "#ec4899",
    "magenta": "#a21caf",
    "green": "#22c55e",
    "purple": "#8b5cf6",
    "teal": "#14b8a6",
    "cyan": "#06b6d4",
    "lime": "#84cc16",
    "amber": "#f59e42",
    "indigo": "#6366f1",
    "gray": "#64748b",
    "brown": "#a16207",
    "olive": "#a3e635",
    "maroon": "#be123c",
    "silver": "#e5e7eb",
    "gold": "#fbbf24",
    "navy": "#0f172a"
}

# --- Custom CSS Injection ---
def inject_css(role):
    accent = FORCE_COLORS.get(role, "#0f172a")
    bg = "linear-gradient(135deg, #fbbf24 0%, #facc15 40%, #e3eafc 100%)" # bright gold/yellow gradient
    st.markdown(f"""
<style>
body {{ background: {bg}; }}
.tricolor-banner {{ background: linear-gradient(90deg, #1e3a8a 33%, #0f172a 34%, #7f1d1d 67%); height: 48px; }}
.footer {{ background: #0f172a; color: #fff; text-align: center; padding: 8px; font-size: 16px; }}
.sidebar .sidebar-content {{ background: {accent}; }}
.stButton>button {{ background: linear-gradient(90deg, #fbbf24 0%, {accent} 100%); color: #0f172a; font-weight:600; border-radius: 8px; box-shadow:0 2px 8px #0002; }}
.stTable, .stDataFrame, .stTable th, .stTable td, .stDataFrame th, .stDataFrame td {{
    color: black !important;
    background: #fffbe6 !important;
}}
.stTabs [data-baseweb="tab"] {{ background: {accent}; color: #fff; }}
h1, h2, h3, h4 {{ color: #0f172a; text-shadow: 0 2px 8px #fbbf24; }}
</style>
""", unsafe_allow_html=True)

# --- Banner & Footer ---
def show_banner():
    st.markdown('''
    <div class="tricolor-banner" style="position:relative;height:72px;">
        <div style="position:absolute;left:50%;top:0;transform:translateX(-50%);width:100%;height:72px;z-index:1;"></div>
        <div style="position:absolute;right:24px;top:16px;z-index:2;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6e/Indian_Navy_crest.png" height="48" style="margin-right:18px;vertical-align:middle;"/>
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/2e/Indian_Army_crest.png" height="48" style="margin-right:18px;vertical-align:middle;"/>
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/Indian_Air_Force_crest.png" height="48" style="vertical-align:middle;"/>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def show_footer():
    st.markdown('<div class="footer">⚓ NAVAL WING, DSSC Wellington</div>', unsafe_allow_html=True)

# --- Session State ---
def clear_session():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# --- Login System ---
def login():
    show_banner()
    st.markdown('<div class="footer">⚓ NAVAL WING, DSSC Wellington</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;font-size:3.5rem;margin-bottom:0;color:#fbbf24;text-shadow:0 2px 12px #0f172a;'>COPP AHP Military Planner</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:#0f172a;margin-top:0;font-size:2rem;text-shadow:0 2px 8px #fbbf24;'>Login</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;justify-content:center;align-items:center;gap:48px;margin-top:32px;margin-bottom:32px;'>
        <div style='display:flex;flex-direction:column;align-items:center;'>
            <span style='margin-top:12px;font-size:1.2rem;color:#0f172a;font-weight:600;'>Control</span>
        </div>
        <div style='display:flex;flex-direction:column;align-items:center;'>
            <span style='margin-top:12px;font-size:1.2rem;color:#1e3a8a;font-weight:600;'>Blue Force</span>
        </div>
        <div style='display:flex;flex-direction:column;align-items:center;'>
            <span style='margin-top:12px;font-size:1.2rem;color:#7f1d1d;font-weight:600;'>Red Force</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    force_cols = st.columns(len(SIDES)+1)
    with force_cols[0]:
        if st.button("🟢 Control", key="big_control_btn_login"):
            st.session_state["login_role"] = "control"
    for idx, side in enumerate(SIDES):
        with force_cols[idx+1]:
            color = FORCE_COLORS.get(side, "#0f172a")
            emoji = "🔵" if side == "blue" else ("🔴" if side == "red" else "⚡")
            if st.button(f"{emoji} {side.capitalize()}", key=f"big_{side}_btn_login"):
                st.session_state["login_role"] = side
    role = st.session_state.get("login_role")
    if role:
        pin = st.text_input(f"Enter PIN for {role.capitalize()}:", type="password")
        if st.button("Login"):
            valid = False
            if role == "control":
                valid = (pin == st.session_state.get("pin_control", "9999"))
            elif role in SIDES:
                valid = (pin == st.session_state.get(f"pin_{role}", "0000" if role not in ["blue", "red"] else ("2222" if role == "blue" else "1111")))
            if valid:
                st.session_state["role"] = role
                st.session_state["side"] = role if role != "control" else "blue"
                st.success(f"Logged in as {role.capitalize()}")
                st.rerun()
            else:
                st.error("Invalid PIN")
    st.markdown("<br><br>", unsafe_allow_html=True)
    # --- AHP Team Link ---
    # --- AHP Team Link & Password Setting (Control Only) ---
    st.markdown("<div style='text-align:center;margin-top:48px;'>", unsafe_allow_html=True)
    col_team, col_pwd = st.columns([2,1])
    with col_team:
        if st.button("AHP Team Credits", key="ahp_team_btn"):
            st.session_state["show_team_modal"] = True
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # Password Modal
    if st.session_state.get("show_pwd_modal"):
        st.markdown("<div style='background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px #0003;position:relative;z-index:100;'>", unsafe_allow_html=True)
        st.subheader("Set Force Passwords (Control Only)")
        pwd_control = st.text_input("Control PIN", value=st.session_state.get("pin_control", "9999"), type="password", key="pin_control")
        pwd_blue = st.text_input("Blue Force PIN", value=st.session_state.get("pin_blue", "2222"), type="password", key="pin_blue")
        pwd_red = st.text_input("Red Force PIN", value=st.session_state.get("pin_red", "1111"), type="password", key="pin_red")
        if st.button("Save PINs", key="save_pins"):
            st.session_state["pin_control"] = pwd_control
            st.session_state["pin_blue"] = pwd_blue
            st.session_state["pin_red"] = pwd_red
            st.success("PINs updated.")
        if st.button("Close", key="close_pwd_modal"):
            st.session_state["show_pwd_modal"] = False
        st.markdown("</div>", unsafe_allow_html=True)
    # Team Modal (Read-only view for all users)
    if st.session_state.get("show_team_modal"):
        st.markdown("<div style='background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px #0003;position:relative;z-index:100;'>", unsafe_allow_html=True)
        st.subheader("AHP Team Credits")
        # Default team data
        if "ahp_team" not in st.session_state:
            st.session_state["ahp_team"] = [
                {"name": "Cdr A Kumar", "role": "Lead Architect"},
                {"name": "Lt B Singh", "role": "Backend Developer"},
                {"name": "Lt C Sharma", "role": "Frontend Developer"},
                {"name": "Lt D Patel", "role": "Testing & QA"}
            ]
        team = st.session_state["ahp_team"]
        for member in team:
            st.write(f"**{member['name']}** — {member['role']}")
        st.info("To edit team credits, login as Control and go to Control Panel.")
        if st.button("Close", key="close_team_modal"):
            st.session_state["show_team_modal"] = False
        st.markdown("</div>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
def sidebar():
    role = st.session_state.get("role", "")
    inject_css(role)
    st.sidebar.title("Navigation")
    tabs = ["Phases", "Objectives", "Decisive Points", "Tasks", "KO Method"]
    if role == "control":
        tabs += ["Progress Entry", "Dashboard", "Control Panel", "Force Manager"]
    tabs += ["Project Management", "Logout"]
    selected = st.sidebar.radio("Go to:", tabs)
    return selected

# --- Project Management ---
def project_management():
    st.header("Project Management")
    projects = list_projects()
    selected = st.selectbox("Select Project", projects)
    if st.button("Switch Project"):
        st.session_state["project"] = selected
        st.success(f"Switched to {selected}")
        st.rerun()
    new_name = st.text_input("New Project Name")
    new_desc = st.text_area("Description")
    if st.button("Create Project") and new_name:
        for side in SIDES:
            save_project(new_name, side, DEFAULT_STRUCTURE)
        st.success(f"Project {new_name} created.")
        st.rerun()
    if st.button("Archive Project"):
        archive_project(selected)
        st.success(f"Project {selected} archived.")
        st.rerun()
    if st.button("Delete Project"):
        delete_project(selected)
        st.success(f"Project {selected} deleted.")
        st.rerun()
    st.write("Export:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Blue JSON"):
            path = export_project_json(selected, "blue")
            st.download_button("Download Blue JSON", open(path, "rb"), file_name=path)
    with col2:
        if st.button("Export Red JSON"):
            path = export_project_json(selected, "red")
            st.download_button("Download Red JSON", open(path, "rb"), file_name=path)
    with col3:
        if st.button("Export ZIP"):
            path = export_project_zip(selected)
            st.download_button("Download ZIP", open(path, "rb"), file_name=path)
    st.write("Upload Excel Sheets (Control Only):")
    if st.session_state.get("role") == "control":
        for side in SIDES:
            uploaded = st.file_uploader(f"Upload {side.capitalize()} Excel", type=["xlsx"], key=f"upload_{side}_excel")
            if uploaded:
                tmp_path = f"tmp_{side}.xlsx"
                with open(tmp_path, "wb") as f:
                    f.write(uploaded.read())
                import_excel_to_project(selected, side, tmp_path)
                st.success(f"Imported {side} Excel.")
                os.remove(tmp_path)
        # Show summary of uploaded data for each force
        st.markdown("### Project Data Summary")
        for side in SIDES:
            data = load_project(selected, side)
            st.subheader(f"{side.capitalize()} Data")
            st.write("Phases:")
            st.table(data.get("phases", []))
            st.write("Objectives:")
            st.table(data.get("objectives", []))
            st.write("DPs:")
            st.table(data.get("dps", []))
            st.write("Tasks:")
            st.table(data.get("tasks", []))

# --- Phases Tab ---
def phases_tab():
    st.header("Phases")
    side = st.session_state.get("side")
    project = st.session_state.get("project")
    data = load_project(project, side)
    phases = data.get("phases", [])
    # Group by unique phase names
    unique_phases = []
    seen = set()
    for p in phases:
        name = p.get("Name")
        if name and name not in seen:
            unique_phases.append(p)
            seen.add(name)
    st.table(unique_phases)
    if st.session_state.get("role") in ["control", side]:
        name = st.text_input("Phase Name")
        if st.button("Add Phase") and name:
            phases.append({"Name": name})
            data["phases"] = phases
            save_project(project, side, data)
            st.success(f"Phase '{name}' added.")
            st.rerun()

# --- Objectives Tab ---
def objectives_tab():
    st.header("Objectives")
    side = st.session_state.get("side")
    project = st.session_state.get("project")
    data = load_project(project, side)
    phases = [p["Name"] for p in data.get("phases", []) if "Name" in p]
    objectives = data.get("objectives", [])
    # Group by unique objective names
    unique_objectives = []
    seen = set()
    for o in objectives:
        name = o.get("Name")
        if name and name not in seen:
            unique_objectives.append(o)
            seen.add(name)
    st.table(unique_objectives)
    if st.session_state.get("role") in ["control", side]:
        name = st.text_input("Objective Name")
        phase = st.selectbox("Phase", phases)
        if st.button("Add Objective") and name:
            objectives.append({"Name": name, "Phase": phase})
            data["objectives"] = objectives
            save_project(project, side, data)
            st.success(f"Objective '{name}' added.")
            st.rerun()

# --- Decisive Points Tab ---
def dps_tab():
    st.header("Decisive Points (DPs)")
    side = st.session_state.get("side")
    project = st.session_state.get("project")
    data = load_project(project, side)
    objectives = [o["Name"] for o in data.get("objectives", []) if "Name" in o]
    phases = [p["Name"] for p in data.get("phases", []) if "Name" in p]
    dps = data.get("dps", [])
    st.table(dps)
    if st.session_state.get("role") in ["control", side]:
        dp_no = st.text_input("DP No")
        name = st.text_input("DP Name")
        objective = st.selectbox("Objective", objectives)
        phase = st.selectbox("Phase", phases)
        weight = st.slider("Weight", 1, 5, 3)
        force_group = st.text_input("Force Group")
        if st.button("Add DP") and dp_no and name:
            dps.append({"DP No": dp_no, "Name": name, "Objective": objective, "Phase": phase, "Weight": weight, "Force Group": force_group})
            data["dps"] = dps
            save_project(project, side, data)
            st.success(f"DP '{name}' added.")
            st.rerun()

# --- Tasks Tab ---
def tasks_tab():
    st.header("Tasks")
    side = st.session_state.get("side")
    project = st.session_state.get("project")
    data = load_project(project, side)
    dps = [dp["DP No"] for dp in data.get("dps", []) if "DP No" in dp]
    tasks = data.get("tasks", [])
    st.table(tasks)
    if st.session_state.get("role") in ["control", side]:
        task_no = st.text_input("Task No", key="add_task_no")
        desc = st.text_input("Description", key="add_desc")
        force_group = st.text_input("Force Group", key="add_fg")
        type_ = st.selectbox("Type", ["T", "I"], key="add_type")
        criteria = st.text_input("Criteria", key="add_criteria")
        stated = st.slider("Stated %", 0, 100, 0, key="add_stated")
        achieved = st.slider("Achieved %", 0, 100, 0, key="add_achieved") if st.session_state.get("role") == "control" else None
        intangible = st.selectbox("Intangible", ["nil", "partial", "complete"], key="add_intangible") if st.session_state.get("role") == "control" else None
        dp_no = st.selectbox("DP No", dps, key="add_dpno")
        if st.button("Add Task", key="add_task_btn") and task_no and desc:
            task = {"Task No": task_no, "Desc": desc, "Force Group": force_group, "Type": type_, "Criteria": criteria, "Stated %": stated, "DP No": dp_no}
            if achieved is not None:
                task["Achieved %"] = achieved
            if intangible is not None:
                task["Intangible"] = intangible
            tasks.append(task)
            data["tasks"] = tasks
            save_project(project, side, data)
            st.success(f"Task '{desc}' added.")
            st.rerun()
        if st.session_state.get("role") in ["control", side]:
            st.markdown("### Edit Tasks")
            for i, task in enumerate(tasks):
                with st.expander(f"Edit Task {task.get('Task No', i+1)}"):
                    task_no = st.text_input(f"Task No {i+1}", task.get("Task No", ""), key=f"edit_task_no_{i}")
                    desc = st.text_input(f"Description {i+1}", task.get("Desc", ""), key=f"edit_desc_{i}")
                    force_group = st.text_input(f"Force Group {i+1}", task.get("Force Group", ""), key=f"edit_fg_{i}")
                    type_ = st.selectbox(f"Type {i+1}", ["T", "I"], index=["T", "I"].index(task.get("Type", "T")), key=f"edit_type_{i}")
                    criteria = st.text_input(f"Criteria {i+1}", task.get("Criteria", ""), key=f"edit_criteria_{i}")
                    stated = st.slider(f"Stated % {i+1}", 0, 100, int(task.get("Stated %", 0)), key=f"edit_stated_{i}")
                    achieved = st.slider(f"Achieved % {i+1}", 0, 100, int(task.get("Achieved %", 0)), key=f"edit_achieved_{i}") if st.session_state.get("role") == "control" else None
                    intangible = st.selectbox(f"Intangible {i+1}", ["nil", "partial", "complete"], index=["nil", "partial", "complete"].index(task.get("Intangible", "nil")), key=f"edit_intangible_{i}") if st.session_state.get("role") == "control" else None
                    dp_no = st.selectbox(f"DP No {i+1}", dps, index=dps.index(task.get("DP No", dps[0])) if task.get("DP No") in dps else 0, key=f"edit_dpno_{i}")
                    if st.button(f"Save Task {i+1}", key=f"save_task_{i}"):
                        task["Task No"] = task_no
                        task["Desc"] = desc
                        task["Force Group"] = force_group
                        task["Type"] = type_
                        task["Criteria"] = criteria
                        task["Stated %"] = stated
                        if achieved is not None:
                            task["Achieved %"] = achieved
                        if intangible is not None:
                            task["Intangible"] = intangible
                        task["DP No"] = dp_no
                        tasks[i] = task
                        data["tasks"] = tasks
                        save_project(project, side, data)
                        st.success(f"Task {task_no} updated.")
            st.markdown("---")
            task_no = st.text_input("Task No")
            desc = st.text_input("Description")
            force_group = st.text_input("Force Group")
            type_ = st.selectbox("Type", ["T", "I"])
            criteria = st.text_input("Criteria")
            stated = st.slider("Stated %", 0, 100, 0)
            achieved = st.slider("Achieved %", 0, 100, 0) if st.session_state.get("role") == "control" else None
            intangible = st.selectbox("Intangible", ["nil", "partial", "complete"]) if st.session_state.get("role") == "control" else None
            dp_no = st.selectbox("DP No", dps)
            if st.button("Add Task") and task_no and desc:
                task = {"Task No": task_no, "Desc": desc, "Force Group": force_group, "Type": type_, "Criteria": criteria, "Stated %": stated, "DP No": dp_no}
                if achieved is not None:
                    task["Achieved %"] = achieved
                if intangible is not None:
                    task["Intangible"] = intangible
                tasks.append(task)
                data["tasks"] = tasks
                save_project(project, side, data)
                st.success(f"Task '{desc}' added.")
                st.rerun()

# --- KO Method Tab ---
def ko_tab():
    import itertools
    st.header("KO Method (Pairwise DP Weightage)")
    s = st.session_state
    project = s.get("project")
    side = s.get("side")
    data = load_project(project, side)
    dps = data.get("dps", [])
    # Support both 'DP No' and 'dp_no' keys
    def get_dp_no(dp):
        return dp.get("DP No") or dp.get("dp_no")
    if len(dps) < 2:
        st.info("Need at least 2 DPs for KO comparison. KO is optional.")
        return
    pairs = list(itertools.combinations(dps, 2))
    key_prefix = f"ko_{project}_{side}"
    # Initialize KO session state
    if f"{key_prefix}_idx" not in s:
        s[f"{key_prefix}_idx"] = 0
        s[f"{key_prefix}_scores"] = {get_dp_no(d): 1 for d in dps if get_dp_no(d) is not None}
    idx = s[f"{key_prefix}_idx"]
    scores = s[f"{key_prefix}_scores"]
    # KO Voting UI
    if idx < len(pairs):
        a, b = pairs[idx]
        st.write(f"Comparison {idx+1} of {len(pairs)}")
        colA, colB = st.columns(2)
        if colA.button(f"A: {a.get('Name', a.get('name', ''))}"):
            scores[get_dp_no(a)] += 1
            s[f"{key_prefix}_idx"] += 1
            st.rerun()
        if colB.button(f"B: {b.get('Name', b.get('name', ''))}"):
            scores[get_dp_no(b)] += 1
            s[f"{key_prefix}_idx"] += 1
            st.rerun()
    else:
        # All pairs compared, compute weights
        mx = max(scores.values()) if scores else 1
        for d in dps:
            dp_no = get_dp_no(d)
            if dp_no in scores:
                d["Weight"] = round((scores[dp_no] / mx) * 5, 2)
        save_project(project, side, data)
        st.success("KO complete! DP Weights updated (scaled to max 5).")
        st.write("DP Weights:", {d.get("Name", d.get("name", "")): d["Weight"] for d in dps if "Weight" in d})
        if st.button("Restart KO"):
            s[f"{key_prefix}_idx"] = 0
            s[f"{key_prefix}_scores"] = {get_dp_no(d): 1 for d in dps if get_dp_no(d) is not None}
            st.rerun()

# --- Progress Entry Tab (Control Only) ---
def progress_entry_tab():
    st.header("Progress Entry (Control Only)")
    project = st.session_state.get("project")
    for side in SIDES:
        data = load_project(project, side)
        tasks = data.get("tasks", [])
        for i, task in enumerate(tasks):
            st.write(f"{side.capitalize()} Task {task.get('Task No')}: {task.get('Desc')}")
            achieved = st.slider(f"Achieved % ({side} Task {i+1})", 0, 100, int(task.get("Achieved %", 0)), key=f"ach_{side}_{i}")
            weight = st.slider(f"Weight % ({side} Task {i+1})", 0, 100, 100, key=f"wgt_{side}_{i}")
            intangible = st.selectbox(f"Intangible ({side} Task {i+1})", ["nil", "partial", "complete"], index=["nil", "partial", "complete"].index(task.get("Intangible", "nil")), key=f"int_{side}_{i}")
            override = st.slider(f"Override % ({side} Task {i+1})", 0, 100, int(task.get("Override %", 0)), key=f"ovr_{side}_{i}")
            if st.button(f"Save {side} Task {i+1}"):
                task["Achieved %"] = achieved
                task["Weight %"] = weight
                task["Intangible"] = intangible
                task["Override %"] = override
                tasks[i] = task
                data["tasks"] = tasks
                save_project(project, side, data)
                st.success(f"Task {task.get('Task No')} updated.")

# --- Dashboard Tab (Control Only) ---
def dashboard_tab():
    st.header("Dashboard (Control Only)")
    project = st.session_state.get("project")
    rag = st.session_state.get("rag", {"red": 40, "amber": 70})
    col1, col2 = st.columns(2)
    for idx, side in enumerate(SIDES):
        data = load_project(project, side)
        progress = compute_progress(data)
        with [col1, col2][idx]:
            st.subheader(f"{side.capitalize()} Force")
            # DP Bar Chart
            dp_vals = list(progress["dp"].values())
            dp_names = list(progress["dp"].keys())
            colors = ["#7f1d1d" if v < rag["red"] else "#f59e42" if v < rag["amber"] else "#1e3a8a" for v in dp_vals]
            fig = go.Figure([go.Bar(x=dp_names, y=dp_vals, marker_color=colors)])
            fig.update_layout(title="DP Progress", yaxis_title="%", xaxis_title="DP No")
            st.plotly_chart(fig, use_container_width=True, key=f"dp_chart_{side}")
            # Objective Pie Chart
            obj_vals = list(progress["objective"].values())
            obj_names = list(progress["objective"].keys())
            fig2 = go.Figure([go.Pie(labels=obj_names, values=obj_vals)])
            fig2.update_layout(title="Objective Progress")
            st.plotly_chart(fig2, use_container_width=True, key=f"obj_chart_{side}")
            # Phase Line Chart
            phase_vals = list(progress["phase"].values())
            phase_names = list(progress["phase"].keys())
            fig3 = go.Figure([go.Scatter(x=phase_names, y=phase_vals, mode="lines+markers")])
            fig3.update_layout(title="Phase Progress", yaxis_title="%", xaxis_title="Phase")
            st.plotly_chart(fig3, use_container_width=True, key=f"phase_chart_{side}")
            # Mini Gauges for Objectives
            for obj, val in progress["objective"].items():
                st.metric(label=f"Objective: {obj}", value=f"{val:.1f}%")

# --- Control Panel Tab ---
def control_panel_tab():
    st.header("Control Panel")
    rag = st.session_state.get("rag", {"red": 40, "amber": 70})
    red = st.slider("Red Threshold", 0, 100, rag["red"])
    amber = st.slider("Amber Threshold", 0, 100, rag["amber"])
    st.session_state["rag"] = {"red": red, "amber": amber}
    project = st.session_state.get("project")
    for side in SIDES:
        data = load_project(project, side)
        dps = data.get("dps", [])
        for i, dp in enumerate(dps):
            weight = st.slider(f"{side.capitalize()} DP {dp.get('DP No')} Weight", 1, 5, int(dp.get("Weight", 3)), key=f"wgt_{side}_{i}")
            btn_key = f"save_{side}_{dp.get('DP No')}_{i}"
            if st.button(f"Save {side} DP {dp.get('DP No')}", key=btn_key):
                dp["Weight"] = weight
                dps[i] = dp
                data["dps"] = dps
                save_project(project, side, data)
                st.success(f"DP {dp.get('DP No')} weight updated.")
    
    st.markdown("---")
    st.subheader("Set Force Passwords (Control Only)")
    pwd_control = st.text_input("Control PIN", value=st.session_state.get("pin_control", "9999"), type="password", key="pin_control_panel_cp")
    pwd_blue = st.text_input("Blue Force PIN", value=st.session_state.get("pin_blue", "2222"), type="password", key="pin_blue_panel_cp")
    pwd_red = st.text_input("Red Force PIN", value=st.session_state.get("pin_red", "1111"), type="password", key="pin_red_panel_cp")
    # Add password fields for all other forces
    for force in SIDES:
        if force not in ["blue", "red"]:
            st.session_state.setdefault(f"pin_{force}", "0000")
            pin_val = st.text_input(f"{force.capitalize()} PIN", value=st.session_state.get(f"pin_{force}", "0000"), type="password", key=f"pin_{force}_panel_cp")
            if st.button(f"Save {force.capitalize()} PIN", key=f"save_pin_{force}_panel_cp"):
                st.session_state[f"pin_{force}"] = pin_val
                st.success(f"{force.capitalize()} PIN updated.")
    if st.button("Save All PINs", key="save_all_pins_panel_cp"):
        st.session_state["pin_control"] = pwd_control
        st.session_state["pin_blue"] = pwd_blue
        st.session_state["pin_red"] = pwd_red
        st.success("All PINs updated.")

    # --- AHP Team Credits Edit ---
    st.markdown("---")
    st.subheader("AHP Team Credits")
    if "ahp_team" not in st.session_state:
        st.session_state["ahp_team"] = [
            {"name": "Cdr A Kumar", "role": "Lead Architect"},
            {"name": "Lt B Singh", "role": "Backend Developer"},
            {"name": "Lt C Sharma", "role": "Frontend Developer"},
            {"name": "Lt D Patel", "role": "Testing & QA"}
        ]
    team = st.session_state["ahp_team"]
    for i, member in enumerate(team):
        name = st.text_input(f"Name {i+1}", member["name"], key=f"team_name_cp_{i}")
        role_ = st.text_input(f"Role {i+1}", member["role"], key=f"team_role_cp_{i}")
        team[i]["name"] = name
        team[i]["role"] = role_
    if st.button("Add Member", key="add_team_member_cp"):
        team.append({"name": "", "role": ""})
    if st.button("Save Credits", key="save_team_credits_cp"):
        st.session_state["ahp_team"] = team
        st.success("Team credits updated.")

# --- Force Manager Tab ---
def force_manager_tab():
    st.header("Force Manager")
    global SIDES
    st.write("Current Forces:")
    cols = st.columns(len(SIDES))
    for idx, side in enumerate(SIDES):
        color = FORCE_COLORS.get(side, "#0f172a")
        with cols[idx]:
            st.markdown(f"<div style='background:{color};color:#fff;padding:8px;border-radius:8px;text-align:center;'>{side.capitalize()}</div>", unsafe_allow_html=True)
            if side not in ["blue", "red"]:
                if st.button(f"Remove {side.capitalize()}", key=f"remove_{side}"):
                    SIDES.remove(side)
                    save_forces(SIDES)
                    st.success(f"Removed {side.capitalize()} force.")
                    st.rerun()
    st.markdown("---")
    st.subheader("Add New Force")
    new_force = st.text_input("Force Name (lowercase, e.g. yellow)")
    color = st.color_picker("Force Color", FORCE_COLORS.get(new_force, "#0f172a"))
    if st.button("Add Force") and new_force and new_force not in SIDES:
        SIDES.append(new_force)
        save_forces(SIDES)
        FORCE_COLORS[new_force] = color
        # Create project structure for new force in all projects
        for proj in list_projects():
            save_project(proj, new_force, DEFAULT_STRUCTURE)
        st.success(f"Added {new_force.capitalize()} force.")
        st.rerun()

# --- Main Routing ---
def main():
    if "role" not in st.session_state:
        login()
        return
    show_banner()
    if "project" not in st.session_state:
        projects = list_projects()
        if projects:
            st.session_state["project"] = projects[0]
        else:
            st.session_state["project"] = "Demo"
            for side in SIDES:
                save_project("Demo", side, DEFAULT_STRUCTURE)
    selected = sidebar()
    if selected == "Phases":
        phases_tab()
    elif selected == "Objectives":
        objectives_tab()
    elif selected == "Decisive Points":
        dps_tab()
    elif selected == "Tasks":
        tasks_tab()
    elif selected == "KO Method":
        ko_tab()
    elif selected == "Progress Entry":
        progress_entry_tab()
    elif selected == "Dashboard":
        dashboard_tab()
    elif selected == "Control Panel":
        control_panel_tab()
    elif selected == "Force Manager":
        force_manager_tab()
    elif selected == "Project Management":
        project_management()
    elif selected == "Logout":
        clear_session()
    show_footer()

if __name__ == "__main__":
    main()
