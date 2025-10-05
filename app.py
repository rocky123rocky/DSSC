
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
    st.markdown("<div style='text-align:center;margin-top:48px;'>", unsafe_allow_html=True)
    col_team, col_pwd = st.columns([2,1])
    with col_team:
        if st.button("AHP Team Credits", key="ahp_team_btn"):
            st.session_state["show_team_modal"] = True
    st.markdown("</div>", unsafe_allow_html=True)
    # Team Modal
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
        role = st.session_state.get("login_role")
        for i, member in enumerate(team):
            if role == "control":
                name = st.text_input(f"Name {i+1}", member["name"], key=f"team_name_{i}")
                role_ = st.text_input(f"Role {i+1}", member["role"], key=f"team_role_{i}")
                team[i]["name"] = name
                team[i]["role"] = role_
            else:
                st.write(f"**{member['name']}** — {member['role']}")
        if role == "control":
            if st.button("Add Member", key="add_team_member"):
                team.append({"name": "", "role": ""})
            if st.button("Save Credits", key="save_team_credits"):
                st.session_state["ahp_team"] = team
                st.success("Team credits updated.")
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

# --- Phases Tab ---
def phases_tab():
    st.header("Phases")
    project = st.session_state.get("project")
    role = st.session_state.get("role")
    if role == "control":
        st.subheader("All Forces - Phases Comparison")
        for force in SIDES:
            color = FORCE_COLORS.get(force, "#0f172a")
            data = load_project(project, force)
            phases = data.get("phases", [])
            df = pd.DataFrame({
                "Phase No": [idx + 1 for idx in range(len(phases))],
                "Phase Name": [p.get("Name") or p.get("Phase") for p in phases]
            })
            st.markdown(f"<div style='color:{color};font-weight:bold'>{force.capitalize()} Phases:</div>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
    else:
        side = st.session_state.get("side")
        color = FORCE_COLORS.get(side, "#0f172a")
        data = load_project(project, side)
        phases = data.get("phases", [])
        df = pd.DataFrame({
            "Phase No": [idx + 1 for idx in range(len(phases))],
            "Phase Name": [p.get("Name") or p.get("Phase") for p in phases]
        })
        st.markdown(f"<div style='color:{color};font-weight:bold'>{side.capitalize()} Phases:</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
    # Add phase (for control or current side)
    if role == "control" or role in SIDES:
        name = st.text_input("Phase Name")
        if st.button("Add Phase") and name:
            if role == "control":
                for force in SIDES:
                    data = load_project(project, force)
                    data["phases"].append({"Name": name})
                    save_project(project, force, data)
                st.success(f"Phase '{name}' added to all forces.")
            else:
                side = role
                data = load_project(project, side)
                data["phases"].append({"Name": name})
                save_project(project, side, data)
                st.success(f"Phase '{name}' added.")
            st.rerun()

# --- Objectives Tab ---
def objectives_tab():
    st.header("Objectives")
    project = st.session_state.get("project")
    role = st.session_state.get("role")
    if role == "control":
        st.subheader("All Forces - Objectives Comparison")
        for force in SIDES:
            data = load_project(project, force)
            objectives = data.get("objectives", [])
            df = pd.DataFrame({
                "Objective No": [idx + 1 for idx in range(len(objectives))],
                "Objective Name": [o.get("Name") or o.get("Objective") for o in objectives],
                "Phase": [o.get("Phase") for o in objectives]
            })
            st.write(f"{force.capitalize()} Objectives:")
            st.dataframe(df, use_container_width=True)
    else:
        side = st.session_state.get("side")
        data = load_project(project, side)
        objectives = data.get("objectives", [])
        df = pd.DataFrame({
            "Objective No": [idx + 1 for idx in range(len(objectives))],
            "Objective Name": [o.get("Name") or o.get("Objective") for o in objectives],
            "Phase": [o.get("Phase") for o in objectives]
        })
        st.dataframe(df, use_container_width=True)
    # Add objective (for control or current side)
    if role in ["control"] + SIDES:
        name = st.text_input("Objective Name")
        # Collect all phases for selectbox
        all_phases = []
        for force in SIDES:
            data = load_project(project, force)
            all_phases.extend([p.get("Name") or p.get("Phase") for p in data.get("phases", [])])
        all_phases = list(set([p for p in all_phases if p]))
        phase = st.selectbox("Phase", all_phases) if all_phases else st.text_input("Phase")
        if st.button("Add Objective") and name:
            # Add to all forces if control, else just current side
            if role == "control":
                for force in SIDES:
                    data = load_project(project, force)
                    data["objectives"].append({"Name": name, "Phase": phase})
                    save_project(project, force, data)
                st.success(f"Objective '{name}' added to all forces.")
            else:
                side = st.session_state.get("side")
                data = load_project(project, side)
                data["objectives"].append({"Name": name, "Phase": phase})
                save_project(project, side, data)
                st.success(f"Objective '{name}' added.")
            st.rerun()

# --- Decisive Points Tab ---
def dps_tab():
    st.header("Decisive Points (DPs)")
    project = st.session_state.get("project")
    role = st.session_state.get("role")
    if role == "control":
        st.subheader("All Forces - DP Comparison")
        for force in SIDES:
            color = FORCE_COLORS.get(force, "#0f172a")
            data = load_project(project, force)
            dps = data.get("dps", [])
            st.markdown(f"<div style='color:{color};font-weight:bold'>{force.capitalize()} DPs:</div>", unsafe_allow_html=True)
            st.table(dps)
    else:
        side = st.session_state.get("side")
        color = FORCE_COLORS.get(side, "#0f172a")
        data = load_project(project, side)
        dps = data.get("dps", [])
        st.markdown(f"<div style='color:{color};font-weight:bold'>{side.capitalize()} DPs:</div>", unsafe_allow_html=True)
        # Organize DP table
        if dps:
            # Ensure DP No is unique and auto-generated
            for idx, dp in enumerate(dps):
                dp["DP No"] = idx + 1
            # Standardize column names and order
            def normalize(dp):
                return {
                    "DP No": dp.get("DP No"),
                    "Name": dp.get("Name") or dp.get("name"),
                    "Objective": dp.get("Objective") or dp.get("objective"),
                    "Phase": dp.get("Phase") or dp.get("phase"),
                    "Weight": dp.get("Weight") or dp.get("weight"),
                    "Force Group": dp.get("Force Group") or dp.get("force_group"),
                }
            df = pd.DataFrame([normalize(dp) for dp in dps])
            df = df.dropna(axis=1, how="all")
            st.dataframe(df, use_container_width=True)

            # Edit DP dropdown
            dp_names = [dp.get("Name") or dp.get("name") for dp in dps]
            selected_dp = st.selectbox("Select DP to edit", dp_names, key=f"edit_dp_{side}")
            if selected_dp:
                dp_idx = dp_names.index(selected_dp)
                edit_dp = dps[dp_idx]
                st.write("Edit DP:")
                new_name = st.text_input("Name", value=edit_dp.get("Name") or "", key=f"dp_name_{side}")
                new_objective = st.text_input("Objective", value=edit_dp.get("Objective") or "", key=f"dp_obj_{side}")
                new_phase = st.text_input("Phase", value=edit_dp.get("Phase") or "", key=f"dp_phase_{side}")
                new_weight = st.number_input("Weight", min_value=1, max_value=10, value=int(edit_dp.get("Weight") or 1), key=f"dp_weight_{side}")
                new_force_group = st.text_input("Force Group", value=edit_dp.get("Force Group") or "", key=f"dp_fg_{side}")
                if st.button("Save DP", key=f"save_dp_{side}"):
                    edit_dp["Name"] = new_name
                    edit_dp["Objective"] = new_objective
                    edit_dp["Phase"] = new_phase
                    edit_dp["Weight"] = new_weight
                    edit_dp["Force Group"] = new_force_group
                    save_project(project, side, data)
                    st.success("DP updated!")
                    st.rerun()
        else:
            st.info("No DPs found for this force.")
    # Add DP (for control or current side)
    if role in ["control"] + SIDES:
        dp_no = st.text_input("DP No")
        name = st.text_input("DP Name")
        # Collect all objectives and phases for selectbox
        all_objectives = []
        all_phases = []
        for force in SIDES:
            data = load_project(project, force)
            all_objectives.extend([o.get("Name") for o in data.get("objectives", []) if o.get("Name")])
            all_phases.extend([p.get("Name") or p.get("Phase") for p in data.get("phases", [])])
        all_objectives = list(set(all_objectives))
        all_phases = list(set([p for p in all_phases if p]))
        objective = st.selectbox("Objective", all_objectives) if all_objectives else st.text_input("Objective")
        phase = st.selectbox("Phase", all_phases) if all_phases else st.text_input("Phase")
        weight = st.slider("Weight", 1, 5, 3)
        force_group = st.text_input("Force Group")
        if st.button("Add DP") and dp_no and name:
            if role == "control":
                for force in SIDES:
                    data = load_project(project, force)
                    data["dps"].append({"DP No": dp_no, "Name": name, "Objective": objective, "Phase": phase, "Weight": weight, "Force Group": force_group})
                    save_project(project, force, data)
                st.success(f"DP '{name}' added to all forces.")
            else:
                side = st.session_state.get("side")
                data = load_project(project, side)
                data["dps"].append({"DP No": dp_no, "Name": name, "Objective": objective, "Phase": phase, "Weight": weight, "Force Group": force_group})
                save_project(project, side, data)
                st.success(f"DP '{name}' added.")
            st.rerun()

# --- Tasks Tab ---
def tasks_tab():
    st.header("Tasks")
    project = st.session_state.get("project")
    role = st.session_state.get("role")
    if role == "control":
        st.subheader("All Forces - Tasks Comparison")
        for force in SIDES:
            color = FORCE_COLORS.get(force, "#0f172a")
            data = load_project(project, force)
            tasks = data.get("tasks", [])
            df = pd.DataFrame({
                "Task No": [idx + 1 for idx in range(len(tasks))],
                "Task Name": [t.get("Desc") or t.get("Task Name") or t.get("name") for t in tasks],
                "DP No": [t.get("DP No") for t in tasks],
                "Weight": [t.get("Weight") or t.get("weight") for t in tasks],
                "Progress (%)": [t.get("Achieved %") or t.get("progress") or 0 for t in tasks]
            })
            st.markdown(f"<div style='color:{color};font-weight:bold'>{force.capitalize()} Tasks:</div>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
    else:
        side = st.session_state.get("side")
        color = FORCE_COLORS.get(side, "#0f172a")
        data = load_project(project, side)
        tasks = data.get("tasks", [])
        df = pd.DataFrame({
            "Task No": [idx + 1 for idx in range(len(tasks))],
            "Task Name": [t.get("Desc") or t.get("Task Name") or t.get("name") for t in tasks],
            "DP No": [t.get("DP No") for t in tasks],
            "Weight": [t.get("Weight") or t.get("weight") for t in tasks],
            "Progress (%)": [t.get("Achieved %") or t.get("progress") or 0 for t in tasks]
        })
        st.markdown(f"<div style='color:{color};font-weight:bold'>{side.capitalize()} Tasks:</div>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
    # Add task (for control or current side)
    if role in ["control"] + SIDES:
        # Collect all DPs for selectbox
        all_dps = []
        for force in SIDES:
            data = load_project(project, force)
            all_dps.extend([dp.get("DP No") for dp in data.get("dps", []) if dp.get("DP No")])
        all_dps = list(set([dp for dp in all_dps if dp]))
        task_no = st.text_input("Task No", key="add_task_no")
        desc = st.text_input("Description", key="add_desc")
        force_group = st.text_input("Force Group", key="add_fg")
        type_ = st.selectbox("Type", ["T", "I"], key="add_type")
        criteria = st.text_input("Criteria", key="add_criteria")
        stated = st.slider("Stated %", 0, 100, 0, key="add_stated")
        achieved = st.slider("Achieved %", 0, 100, 0, key="add_achieved") if role == "control" else None
        intangible = st.selectbox("Intangible", ["nil", "partial", "complete"], key="add_intangible") if role == "control" else None
        dp_no = st.selectbox("DP No", all_dps, key="add_dpno") if all_dps else st.text_input("DP No", key="add_dpno_text")
        if st.button("Add Task", key="add_task_btn") and task_no and desc:
            if role == "control":
                for force in SIDES:
                    data = load_project(project, force)
                    task = {"Task No": task_no, "Desc": desc, "Force Group": force_group, "Type": type_, "Criteria": criteria, "Stated %": stated, "DP No": dp_no}
                    if achieved is not None:
                        task["Achieved %"] = achieved
                    if intangible is not None:
                        task["Intangible"] = intangible
                    data["tasks"].append(task)
                    save_project(project, force, data)
                st.success(f"Task '{desc}' added to all forces.")
            else:
                side = st.session_state.get("side")
                data = load_project(project, side)
                task = {"Task No": task_no, "Desc": desc, "Force Group": force_group, "Type": type_, "Criteria": criteria, "Stated %": stated, "DP No": dp_no}
                if achieved is not None:
                    task["Achieved %"] = achieved
                if intangible is not None:
                    task["Intangible"] = intangible
                data["tasks"].append(task)
                save_project(project, side, data)
                st.success(f"Task '{desc}' added.")
            st.rerun()

# --- KO Method Tab ---
def ko_tab():
    st.header("KO Method")
    project = st.session_state.get("project")
    side = st.session_state.get("side")
    data = load_project(project, side)
    
    def get_dp_no(dp):
        return dp.get("DP No") or dp.get("dp_no")
    
    st.write("KO Method analysis placeholder")

# --- Progress Entry Tab ---
def progress_entry_tab():
    st.header("Progress Entry (Control Only)")
    project = st.session_state.get("project")
    for force in SIDES:
        st.subheader(f"{force.capitalize()} Force")
        data = load_project(project, force)
        tasks = data.get("tasks", [])
        for idx, task in enumerate(tasks):
            task_name = task.get("Desc") or task.get("Task Name") or f"Task {idx+1}"
            progress = st.slider(f"{task_name}", 0, 100, int(task.get("Achieved %", 0)), key=f"progress_{force}_{idx}")
            task["Achieved %"] = progress
        if st.button(f"Save {force.capitalize()} Progress", key=f"save_progress_{force}"):
            save_project(project, force, data)
            st.success(f"{force.capitalize()} progress saved!")

# --- Dashboard Tab ---
def dashboard_tab():
    st.header("Dashboard (Control Only)")
    project = st.session_state.get("project")
    rag = st.session_state.get("rag", {"red": 40, "amber": 70})
    col1, col2 = st.columns(2)
    for idx, side in enumerate(SIDES):
        data = load_project(project, side)
        progress = compute_progress(data)
        with [col1, col2][idx % 2]:
            st.subheader(f"{side.capitalize()} Force")
            # DP Bar Chart
            dp_vals = list(progress["dp"].values())
            dp_names = list(progress["dp"].keys())
            colors = ["#7f1d1d" if v < rag["red"] else "#f59e42" if v < rag["amber"] else "#1e3a8a" for v in dp_vals]
            fig = go.Figure([go.Bar(x=dp_names, y=dp_vals, marker_color=colors)])
            fig.update_layout(title="DP Progress", yaxis_title="%", xaxis_title="DP No")
            st.plotly_chart(fig, use_container_width=True)

# --- Control Panel Tab ---
def control_panel_tab():
    st.header("Control Panel")
    rag = st.session_state.get("rag", {"red": 40, "amber": 70})
    red = st.slider("Red Threshold", 0, 100, rag["red"])
    amber = st.slider("Amber Threshold", 0, 100, rag["amber"])
    st.session_state["rag"] = {"red": red, "amber": amber}
    project = st.session_state.get("project")
    st.subheader("Set Force Passwords (Control Only)")
    pwd_control = st.text_input("Control PIN", value=st.session_state.get("pin_control", "9999"), type="password", key="pin_control_panel_cp")
    pwd_blue = st.text_input("Blue Force PIN", value=st.session_state.get("pin_blue", "2222"), type="password", key="pin_blue_panel_cp")
    pwd_red = st.text_input("Red Force PIN", value=st.session_state.get("pin_red", "1111"), type="password", key="pin_red_panel_cp")
    for force in SIDES:
        if force not in ["control", "blue", "red"]:
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

    # --- AHP Team Credits Edit (Moved from login modal) ---
    st.markdown("---")
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
    for i, member in enumerate(team):
        name = st.text_input(f"Name {i+1}", member["name"], key=f"team_name_cp_{i}")
        role_ = st.text_input(f"Role {i+1}", member["role"], key=f"team_role_cp_{i}")
        team[i]["name"] = name
        team[i]["role"] = role_
    if st.button("Add Member", key="add_team_member_cp"):
        team.append({"name": "", "role": ""})
        st.rerun()
    if st.button("Save Credits", key="save_team_credits_cp"):
        st.session_state["ahp_team"] = team
        st.success("Team credits updated.")

# --- Force Manager Tab ---
def force_manager_tab():
    st.header("Force Manager")
    st.write("Current Forces:")
    for force in SIDES:
        st.write(f"- {force.capitalize()}")
    
    st.subheader("Add New Force")
    new_force = st.text_input("Force Name").lower()
    color = st.color_picker("Force Color", "#0f172a")
    
    if st.button("Add Force") and new_force and new_force not in SIDES:
        SIDES.append(new_force)
        save_forces(SIDES)
        FORCE_COLORS[new_force] = color
        # Create project structure for new force in all projects
        for proj in list_projects():
            save_project(proj, new_force, DEFAULT_STRUCTURE)
        st.success(f"Added {new_force.capitalize()} force.")
        st.rerun()

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
            with open(path, "rb") as f:
                st.download_button("Download Blue JSON", f, file_name=os.path.basename(path))
    with col2:
        if st.button("Export Red JSON"):
            path = export_project_json(selected, "red")
            with open(path, "rb") as f:
                st.download_button("Download Red JSON", f, file_name=os.path.basename(path))
    with col3:
        if st.button("Export ZIP"):
            path = export_project_zip(selected)
            with open(path, "rb") as f:
                st.download_button("Download ZIP", f, file_name=os.path.basename(path))
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
            if data.get("phases"):
                st.table(data.get("phases", []))
            st.write("Objectives:")
            if data.get("objectives"):
                st.table(data.get("objectives", []))
            st.write("DPs:")
            if data.get("dps"):
                st.table(data.get("dps", []))
            st.write("Tasks:")
            if data.get("tasks"):
                st.table(data.get("tasks", []))

# --- Main Routing ---
def main():
    if "project" not in st.session_state:
        st.session_state["project"] = "Default"
    
    if "role" not in st.session_state:
        login()
    else:
        show_banner()
        tab = sidebar()
        if tab == "Phases":
            phases_tab()
        elif tab == "Objectives":
            objectives_tab()
        elif tab == "Decisive Points":
            dps_tab()
        elif tab == "Tasks":
            tasks_tab()
        elif tab == "KO Method":
            ko_tab()
        elif tab == "Progress Entry":
            progress_entry_tab()
        elif tab == "Dashboard":
            dashboard_tab()
        elif tab == "Control Panel":
            control_panel_tab()
        elif tab == "Force Manager":
            force_manager_tab()
        elif tab == "Project Management":
            project_management()
        elif tab == "Logout":
            clear_session()
        show_footer()

if __name__ == "__main__":
    main()
