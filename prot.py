"""
KLIEN — Clinical Intelligence & Interaction Engine (Full PoC)
File Name: prot.py
Features: Comprehensive Module 1 Restore, Dosage Details, Clearance Clocks, Dynamic Removal.
"""

import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta

# ───────────────────────────────────────────────────────────
# THEME CONFIGURATION & BRAND GRADIENT CSS
# ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KLIEN · Clinical Engine",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── KLIEN Logo Gradient Tokens ── */
:root {
    --bg:          #050b14;
    --surface:     #0d1524;
    --border:      #004d52; 
    --accent-grad: linear-gradient(135deg, #012042 0%, #006B70 50%, #00978E 100%);
    --nav-grad-active: linear-gradient(90deg, #006B70 0%, #00978E 100%);
    --mint:        #00978E; 
    --teal:        #006B70;
    --text:        #e2e8f0;
    --muted:       #50727b;
    --danger:      #ef4444;
    --danger-bg:   #1f0a0a;
    --ok:          #10b981;
    --serif:       'DM Serif Display', serif;
    --sans:        'DM Sans', sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem 2rem !important; max-width: 1400px !important; }

/* Sidebar Design */
[data-testid="stSidebar"] { 
    background: var(--surface) !important; 
    border-right: 1px solid var(--border) !important; 
}
.sidebar-fallback-logo {
    font-family: var(--serif); font-size: 2.2rem; font-weight: bold;
    background: linear-gradient(90deg, #006B70, #00978E);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; padding-top: 0.5rem;
}
.sidebar-tagline { font-size: 0.65rem; color: var(--muted) !important; text-align: center; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 1.5rem; }

/* Headings & Text UI */
.page-title { 
    font-family: var(--serif); font-size: 2.5rem; 
    background: linear-gradient(90deg, #e2e8f0, #00978E);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.1rem; 
}
.portal-hero-title {
    font-family: var(--serif); font-size: 3.5rem;
    background: linear-gradient(90deg, #ffffff 30%, #00978E 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-top: 1rem;
}
.page-subtitle { font-size: 0.78rem; color: var(--muted) !important; letter-spacing: 0.08em; margin-bottom: 1.5rem; text-transform: uppercase; font-family: var(--mono); }
.section-title { font-family: var(--mono); font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--mint) !important; margin: 1.8rem 0 0.8rem 0; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); }

/* Custom Components */
.patient-badge { display: flex; align-items: center; gap: 1rem; background: linear-gradient(135deg, #050b14 0%, #0d1524 100%); border: 1px solid var(--mint); border-radius: 10px; padding: 1.2rem 1.5rem; margin-bottom: 1.25rem; }
.patient-avatar { width: 52px; height: 52px; background: var(--accent-grad); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--serif); font-size: 1.3rem; color: #fff !important; box-shadow: 0 0 10px rgba(0, 151, 142, 0.3); }
.patient-name { font-family: var(--serif); font-size: 1.4rem; color: #fff; }
.patient-meta { font-size: 0.8rem; color: var(--muted) !important; font-family: var(--mono); }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; }
.med-pill { display: inline-block; background: #02161a; border: 1px solid var(--teal); color: #00978E !important; border-radius: 20px; padding: 0.25rem 0.9rem; font-size: 0.78rem; font-family: var(--mono); margin: 0.2rem 0.3rem 0.2rem 0; font-weight: 500; }
.status-text { font-family: var(--mono); font-size: 0.75rem; color: var(--mint) !important; }

/* CRITICAL ALERT */
.critical-alert { background: var(--danger-bg); border: 2px solid var(--danger); border-radius: 10px; padding: 1.5rem; margin: 1rem 0; animation: pulse-border 1.5s infinite; }
.critical-alert-title { font-family: var(--mono); font-size: 0.75rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--danger) !important; margin-bottom: 0.5rem; }
.critical-alert-body { font-size: 1rem; color: var(--text) !important; line-height: 1.6; }
.critical-alert-desc { margin-top: 0.75rem; padding: 0.5rem 0.85rem; background: #2d0a0a; border-left: 3px solid var(--danger); font-family: var(--mono); font-size: 0.82rem; color: #fca5a5 !important; }

@keyframes pulse-border {
    0%, 100% { border-color: var(--danger); box-shadow: 0 0 0 0 rgba(239,68,68,0.3); }
    50%       { border-color: #fca5a5;     box-shadow: 0 0 0 6px rgba(239,68,68,0); }
}

[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }
[data-testid="stDataFrame"] * { color: var(--text) !important; font-family: var(--mono) !important; font-size: 0.8rem !important; }

/* Inputs and Buttons */
[data-baseweb="input"] input { background: #050b14 !important; color: var(--text) !important; border-radius: 6px !important; border-color: var(--border) !important; }
.stButton > button { 
    background: var(--accent-grad) !important; color: #fff !important; border: 1px solid var(--mint) !important; 
    border-radius: 6px !important; padding: 0.5rem 1.2rem !important; font-weight: 500 !important; width: 100%; 
}
.stButton > button:hover { box-shadow: 0 0 12px rgba(0, 151, 142, 0.5) !important; border-color: #fff !important; }

label { color: var(--muted) !important; font-size: 0.78rem !important; font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.05em; }

/* File Uploader styling */
[data-testid="stFileUploader"] { background-color: var(--surface) !important; border: 1px dashed var(--border) !important; border-radius: 8px !important; padding: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────
# PERSISTENT STORAGE ENGINE
# ───────────────────────────────────────────────────────────
DB_FILE = "klien_db_v2.json"

def load_local_database():
    if not os.path.exists(DB_FILE):
        default_db = {
            "users": {
                "doctor@klien.com": {"password": "password123", "role": "Doctor"},
                "admin@klien.com": {"password": "admin123", "role": "Medical Data Specialist"}
            },
            "patients": {
                "ABHA-1234": {
                    "name": "John Doe", "age": 54, "diagnosis": "Type 2 Diabetes, Hypertension",
                    "medications": ["Metformin", "Lisinopril"], "prescriptions": []
                }
            },
            "interaction_rules": [
                {"medicine_a": "Metformin", "medicine_b": "Contrast Dye", "description": "High Risk of Metformin-associated Lactic Acidosis."},
                {"medicine_a": "Aspirin", "medicine_b": "Warfarin", "description": "Severe Risk of Internal Bleeding due to antiplatelet amplification."}
            ]
        }
        with open(DB_FILE, "w") as f:
            json.dump(default_db, f, indent=4)

    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_local_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_local_database()

# Session State Keys Initialization
if "authenticated_user" not in st.session_state: st.session_state.authenticated_user = None
if "user_role" not in st.session_state: st.session_state.user_role = None
if "active_patient_key" not in st.session_state: st.session_state.active_patient_key = None
if "alert_triggered" not in st.session_state: st.session_state.alert_triggered = False
if "intercepted_payload" not in st.session_state: st.session_state.intercepted_payload = {}

# ───────────────────────────────────────────────────────────
# MODULE 3 PROTECTION ENGINE SCANNER (WITH CLEARANCE CHECKS)
# ───────────────────────────────────────────────────────────
def execute_background_verification(new_med_name: str, patient_profile: dict) -> dict | None:
    target = new_med_name.strip().lower()
    now = datetime.now()
    
    # Filter down active track parameters only to drugs whose clock is not expired
    active_meds = []
    for med in patient_profile["medications"]:
        is_cleared = False
        for rx in patient_profile.get("prescriptions", []):
            if rx["medicine"].lower() == med.lower() and "clearance_time" in rx:
                try:
                    expiry_time = datetime.strptime(rx["clearance_time"], "%Y-%m-%d %H:%M")
                    if now >= expiry_time:
                        is_cleared = True
                except:
                    pass
        if not is_cleared:
            active_meds.append(med)

    active_chart_lower = [m.lower() for m in active_meds]
    
    # Evaluate Active Conflict Rules Map
    for rule in db["interaction_rules"]:
        a = rule["medicine_a"].lower()
        b = rule["medicine_b"].lower()
        if (target == a and b in active_chart_lower) or (target == b and a in active_chart_lower):
            matched_offending_drug = next(m for m in active_meds if m.lower() == (b if target == a else a))
            return {
                "verdict": f"this medication is reactive with patients active medication {matched_offending_drug}",
                "new_drug": new_med_name.strip(), "offending_drug": matched_offending_drug, "description": rule["description"]
            }
    return None

# ───────────────────────────────────────────────────────────
# SIDEBAR RENDERING SYSTEM
# ───────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = "klien logo.jpeg"
    if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)
    else: st.markdown('<div class="sidebar-fallback-logo">KLIEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Clinical Intelligence Engine</div>', unsafe_allow_html=True)
    
    if st.session_state.authenticated_user:
        st.markdown('<div class="section-title">Session Authorization</div>', unsafe_allow_html=True)
        st.markdown(f'<span style="font-size:0.85rem;color:#fff;">👤 {st.session_state.authenticated_user}</span><br>'
                    f'<span style="font-size:0.75rem;color:var(--mint);font-family:var(--mono);">Role: {st.session_state.user_role}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Logout / Exit Session"):
            st.session_state.authenticated_user = None
            st.session_state.user_role = None
            st.session_state.active_patient_key = None
            st.rerun()
            
    st.markdown('<div class="section-title">System Metrics</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="status-text">● Storage: {DB_FILE} Linked</span><br>'
                f'<span class="status-text">● Profiles Ledger: {len(db["patients"])} patients</span><br>'
                f'<span class="status-text">● Safety Registry: {len(db["interaction_rules"])} rules</span>', unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────
# MAIN LOGIC ROUTER GATEWAY
# ───────────────────────────────────────────────────────────

# SCREEN A: ACCESS INITIALIZATION PORTAL (NOT AUTHENTICATED)
if not st.session_state.authenticated_user:
    st.markdown('<div class="portal-hero-title">KLIEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle" style="text-align:center; letter-spacing:0.2em;">Distributed Medical Logic & Security Interceptor</div>', unsafe_allow_html=True)
    
    _, col_panel, _ = st.columns([1.5, 2, 1.5])
    
    with col_panel:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        mode_tab1, mode_tab2 = st.tabs(["🔐 Authorized Access Login", "📝 Create Security Account"])
        
        with mode_tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            login_email = st.text_input("Username / Email Address", key="login_email_input").strip()
            login_pass = st.text_input("Security Password", type="password", key="login_pass_input").strip()
            selected_role = st.selectbox("Intended Work Environment Role Router", ["Doctor", "Medical Data Specialist"])
            
            if st.button("Initialize Secure Login Tunnel", key="execute_login_btn"):
                if login_email in db["users"] and db["users"][login_email]["password"] == login_pass:
                    if db["users"][login_email]["role"] == selected_role:
                        st.session_state.authenticated_user = login_email
                        st.session_state.user_role = selected_role
                        st.success("Authorization Verified. Tunnel opened.")
                        st.rerun()
                    else: st.error("Role Ambiguity Error: Account mismatch with selected workspace role.")
                else: st.error("Access Refused: Invalid credentials configuration.")
                    
        with mode_tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            reg_email = st.text_input("Register Email Address", key="reg_email_input").strip()
            reg_pass = st.text_input("Create Security Password", type="password", key="reg_pass_input").strip()
            reg_role = st.selectbox("Assign Professional Role Layer Matrix", ["Doctor", "Medical Data Specialist"], key="reg_role_select")
            
            if st.button("Register & Request Access Credentials", key="execute_reg_btn"):
                if not reg_email or not reg_pass: st.warning("All input areas must be declared.")
                elif reg_email in db["users"]: st.error("Account Fault: Email configuration already linked.")
                else:
                    db["users"][reg_email] = {"password": reg_pass, "role": reg_role}
                    save_local_database(db)
                    st.success("Registration success! Open the Login tab to authenticate.")
                    
        st.markdown('</div>', unsafe_allow_html=True)

# SCREEN B: SYSTEM ACTIVE WORKSPACES (LOGGED IN)
else:
    # 👤 WORKSPACE VIEW 1: DOCTOR INTERFACE (MODULE 1)
    if st.session_state.user_role == "Doctor":
        st.markdown('<div class="page-title">Clinical Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Module 1 & 3 · Prescriptions Workspace & Clearance Controllers</div>', unsafe_allow_html=True)
        
        # MODULE 3 PROTECTION FAULT BANNERS
        if st.session_state.alert_triggered:
            payload = st.session_state.intercepted_payload
            st.markdown(f"""
            <div class="critical-alert">
                <div class="critical-alert-title">🚨 Module 3 Engine Intercept: Active Conflict Exception</div>
                <div class="critical-alert-body">
                    Execution Terminated: <b>{payload['verdict']}</b>.<br>
                    Attempted prescription of <b>{payload['new_drug']}</b> compromises patient baseline safety margins.
                </div>
                <div class="critical-alert-desc">Contraindication Rules Profile: {payload['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_cancel, col_override, _ = st.columns([1.5, 1.5, 4])
            with col_cancel:
                if st.button("✕ Cancel Prescription Process", key="cancel_rx_intercept"):
                    st.session_state.alert_triggered = False
                    st.session_state.intercepted_payload = {}
                    st.rerun()
            with col_override:
                if st.button("✓ Force Override Save", key="force_rx_intercept"):
                    pid = st.session_state.active_patient_key
                    db["patients"][pid]["medications"].append(payload["new_drug"])
                    db["patients"][pid]["prescriptions"].append({
                        "medicine": payload["new_drug"], "dosage": "N/A", "frequency": "Override Action",
                        "status": "⚠ Clinical Override Issued", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "clearance_time": (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
                    })
                    save_local_database(db)
                    st.session_state.alert_triggered = False
                    st.session_state.intercepted_payload = {}
                    st.rerun()
            st.divider()

        # PATIENT SEARCH LOOKUP
        st.markdown('<div class="section-title">Patient Lookup</div>', unsafe_allow_html=True)
        col_search, col_search_btn = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("Search Input", placeholder="Search via Name or unique ABHA ID...", label_visibility="collapsed").strip()
        with col_search_btn:
            st.markdown('<div style="padding-top:1px;">', unsafe_allow_html=True)
            execute_search = st.button("Fetch Patient Record")
            st.markdown('</div>', unsafe_allow_html=True)
            
        if execute_search and search_query:
            found_key = None
            query_lower = search_query.lower()
            for p_id, p_data in db["patients"].items():
                if query_lower == p_id.lower() or query_lower == p_data["name"].lower():
                    found_key = p_id
                    break
            if found_key:
                st.session_state.active_patient_key = found_key
                st.rerun()
            else:
                st.session_state.active_patient_key = None
                st.warning("No tracking configuration matches that entry.")

        # NEW PATIENT DIRECT ENTRY REGISTER
        st.markdown('<div class="section-title">Onboard New Patient Record</div>', unsafe_allow_html=True)
        with st.expander("📝 Open New Patient Intake Matrix Form", expanded=not bool(st.session_state.active_patient_key)):
            with st.form("onboarding_form", clear_on_submit=True):
                col_id, col_name = st.columns(2)
                with col_id: new_id = st.text_input("Assign Unique Patient ID / ABHA ID", placeholder="e.g., ABHA-5678").strip().upper()
                with col_name: new_name = st.text_input("Patient Full Name", placeholder="e.g., Jane Smith").strip()
                col_age, col_diag = st.columns([1, 3])
                with col_age: new_age = st.number_input("Age", min_value=0, max_value=120, value=30)
                with col_diag: new_diag = st.text_input("Primary Diagnostic Notes", placeholder="Clinical classifications summary...")
                new_meds_raw = st.text_area("Past / Active Medications List (Comma Separated)")
                
                if st.form_submit_button("Commit New Profile"):
                    if not new_id or not new_name: st.error("Validation Error: Missing tracking identifiers.")
                    elif new_id in db["patients"]: st.error("Data integrity fault: ID configuration collision detected.")
                    else:
                        processed_meds = [m.strip() for m in new_meds_raw.split(",") if m.strip()]
                        db["patients"][new_id] = {
                            "name": new_name, "age": int(new_age), "diagnosis": new_diag,
                            "medications": processed_meds, "prescriptions": []
                        }
                        save_local_database(db)
                        st.session_state.active_patient_key = new_id
                        st.success("Profile saved directly to local database payload repository.")
                        st.rerun()

        # RUN TIME FILE RENDERING ARCHITECTURE
        current_patient = st.session_state.active_patient_key
        if current_patient and current_patient in db["patients"]:
            p_profile = db["patients"][current_patient]
            initials = "".join(part[0].upper() for part in p_profile["name"].split()[:2])
            
            st.markdown('<div class="section-title">Active Clinical Work File</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="patient-badge">
                <div class="patient-avatar">{initials}</div>
                <div>
                    <div class="patient-name">{p_profile['name']}</div>
                    <div class="patient-meta">ID: {current_patient} &nbsp;·&nbsp; Age: {p_profile['age']} &nbsp;·&nbsp; Dx: {p_profile['diagnosis']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- INTERACTIVE DEPRESCRIBE/REMOVAL COMPONENT ---
            st.markdown('**Active Medication Baseline Chart (Click [✕] to Deprescribe/Remove):**')
            if p_profile["medications"]:
                med_cols = st.columns(6)
                for idx, med_name in enumerate(p_profile["medications"]):
                    with med_cols[idx % 6]:
                        if st.button(f"✕ {med_name}", key=f"del_{med_name}_{idx}", help=f"Remove {med_name} from chart"):
                            p_profile["medications"].remove(med_name)
                            save_local_database(db)
                            st.success(f"Removed: {med_name}")
                            st.rerun()
            else:
                st.markdown('<div class="card" style="color:var(--muted);">No active baseline medications tracking on file.</div>', unsafe_allow_html=True)

            # --- DETAILED NEW PRESCRIPTION SCRIPT FORM ---
            st.markdown('<div class="section-title">Formulate New Script Execution</div>', unsafe_allow_html=True)
            with st.form("prescription_form", clear_on_submit=True):
                col_rx1, col_rx2, col_rx3, col_rx4 = st.columns([2, 1, 1, 1])
                with col_rx1:
                    rx_med = st.text_input("Medicine Name", placeholder="e.g. Contrast Dye").strip()
                with col_rx2:
                    rx_dosage = st.text_input("Dosage Parameters", placeholder="e.g. 500 mg").strip()
                with col_rx3:
                    rx_freq = st.text_input("Frequency Parameters", placeholder="e.g. Twice Daily").strip()
                with col_rx4:
                    rx_clear_hrs = st.number_input("Clearance Effect Duration (Hours)", min_value=1, max_value=168, value=12)
                
                col_rx_submit = st.columns([3, 1])[1]
                with col_rx_submit:
                    issue_rx = st.form_submit_button("Evaluate & Issue Script")
                    
                if issue_rx:
                    if not rx_med or not rx_dosage or not rx_freq:
                        st.warning("All core script configuration fields must be specified.")
                    else:
                        verification_result = execute_background_verification(rx_med, p_profile)
                        if verification_result:
                            st.session_state.alert_triggered = True
                            st.session_state.intercepted_payload = verification_result
                            st.rerun()
                        else:
                            calc_expiry = (datetime.now() + timedelta(hours=int(rx_clear_hrs))).strftime("%Y-%m-%d %H:%M")
                            p_profile["medications"].append(rx_med)
                            p_profile["prescriptions"].append({
                                "medicine": rx_med, "dosage": rx_dosage, "frequency": rx_freq,
                                "status": "✓ you could give this medication",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "clearance_time": calc_expiry
                            })
                            save_local_database(db)
                            st.success(f"Verified Clear: Action committed safely.")
                            st.rerun()

            # --- SESSION PRESCRIPTION HISTORIC MATRIX WITH CONTRAST TIMEOUTS ---
            if p_profile.get("prescriptions", []):
                st.markdown('<div class="section-title">Session Prescription Ledger & Safe Contrast Window Clock</div>', unsafe_allow_html=True)
                
                ledger_data = []
                for rx in p_profile["prescriptions"]:
                    now = datetime.now()
                    exp = datetime.strptime(rx["clearance_time"], "%Y-%m-%d %H:%M")
                    
                    if now >= exp:
                        time_status = "⏱ Effect Over — Safe to administer contrasting drug variants"
                    else:
                        remaining = exp - now
                        hours_left = int(remaining.total_seconds() // 3600)
                        mins_left = int((remaining.total_seconds() % 3600) // 60)
                        time_status = f"⏳ Active ({hours_left}h {mins_left}m remaining until cleared)"
                    
                    ledger_data.append({
                        "Medication": rx["medicine"],
                        "Dosage": rx["dosage"],
                        "Frequency": rx["frequency"],
                        "Engine Clearance Status": rx["status"],
                        "Prescribed Clock": rx["timestamp"],
                        "Effect Over Target Time": rx["clearance_time"],
                        "Dynamic Safety Monitor": time_status
                    })
                    
                st.dataframe(pd.DataFrame(ledger_data), use_container_width=True, hide_index=True)

            # --- CONTINUOUS SEAMLESS ADDITIONAL RUN QUEUE ---
            st.markdown("---")
            st.markdown('<div class="section-title">🔄 Queue Additional Medication Run</div>', unsafe_allow_html=True)
            with st.form("continuous_script_form", clear_on_submit=True):
                col_next1, col_next2, col_next3, col_next4 = st.columns([2, 1, 1, 1])
                with col_next1: next_rx_med = st.text_input("Next Medicine Name", placeholder="e.g. Aspirin").strip()
                with col_next2: next_rx_dosage = st.text_input("Next Dosage", placeholder="e.g. 75 mg").strip()
                with col_next3: next_rx_freq = st.text_input("Next Frequency", placeholder="e.g. Once Daily").strip()
                with col_next4: next_rx_clear = st.number_input("Next Clearance Hours", min_value=1, max_value=168, value=24, key="next_clear_input")
                
                col_next_submit = st.columns([3, 1])[1]
                with col_next_submit:
                    process_next_rx = st.form_submit_button("Verify & Queue Next Item")
                    
                if process_next_rx:
                    if not next_rx_med or not next_rx_dosage or not next_rx_freq:
                        st.warning("Execution Halted: Complete all parameters.")
                    else:
                        verify_additional = execute_background_verification(next_rx_med, p_profile)
                        if verify_additional:
                            st.session_state.alert_triggered = True
                            st.session_state.intercepted_payload = verify_additional
                            st.rerun()
                        else:
                            calc_next_expiry = (datetime.now() + timedelta(hours=int(next_rx_clear))).strftime("%Y-%m-%d %H:%M")
                            db["patients"][current_patient]["medications"].append(next_rx_med)
                            db["patients"][current_patient]["prescriptions"].append({
                                "medicine": next_rx_med, "dosage": next_rx_dosage, "frequency": next_rx_freq,
                                "status": "✓ you could give this medication (Added via Multi-Script Run)",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "clearance_time": calc_next_expiry
                            })
                            save_local_database(db)
                            st.success(f"Clearance Status Granted: Item added to history list.")
                            st.rerun()

    # 📊 WORKSPACE VIEW 2: MEDICAL DATA SPECIALIST (MODULE 2)
    elif st.session_state.user_role == "Medical Data Specialist":
        st.markdown('<div class="page-title">Medical Knowledge Directory</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-subtitle">Module 2 · Clinical Registry Base & Bulk Data File Acquisition Stream</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">📊 Bulk Load Medication Interaction Rules via File</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Excel Sheet (.xlsx) or Flat File (.csv)", type=["xlsx", "csv"])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.xlsx'): imported_df = pd.read_excel(uploaded_file)
                else: imported_df = pd.read_csv(uploaded_file)
                
                required_cols = ["medicine_a", "medicine_b", "description"]
                if not all(col in imported_df.columns for col in required_cols):
                    st.error("Schema Error: Columns must match headers 'medicine_a', 'medicine_b', and 'description' exactly.")
                else:
                    st.markdown("**Previewing Upload File Blueprint Schema Data Layout:**")
                    st.dataframe(imported_df.head(5), use_container_width=True)
                    
                    if st.button("Merge Payload Snapshot with Persistent Database File"):
                        added_counter = 0
                        skipped_counter = 0
                        
                        for _, row in imported_df.iterrows():
                            m_a = str(row['medicine_a']).strip()
                            m_b = str(row['medicine_b']).strip()
                            desc = str(row['description']).strip()
                            
                            if not m_a or not m_b or not desc or m_a.lower() == m_b.lower():
                                skipped_counter += 1
                                continue
                                
                            is_dup = any((m_a.lower() == r["medicine_a"].lower() and m_b.lower() == r["medicine_b"].lower()) or 
                                         (m_a.lower() == r["medicine_b"].lower() and m_b.lower() == r["medicine_a"].lower()) for r in db["interaction_rules"])
                            
                            if not is_dup:
                                db["interaction_rules"].append({"medicine_a": m_a, "medicine_b": m_b, "description": desc})
                                added_counter += 1
                            else: skipped_counter += 1
                                
                        if added_counter > 0:
                            save_local_database(db)
                            st.success(f"Ingestion Stream Completed: Integrated {added_counter} unique safety configurations.")
                            st.rerun()
                        else: st.warning("No new elements were found inside the data object matrix array.")
            except Exception as e:
                st.error(f"Incompatible Pipeline Error: Unable to read file trace details: {e}")

        st.markdown('<div class="section-title">Configure Drug Reactivity Rule Manually</div>', unsafe_allow_html=True)
        with st.form("add_rule_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a: med_a = st.text_input("Medicine A Name", placeholder="e.g., Aspirin").strip()
            with col_b: med_b = st.text_input("Medicine B (Reactive Variant)", placeholder="e.g., Warfarin").strip()
            severity_desc = st.text_input("Severity / Clinical Consequence Description", placeholder="Clinical analysis summary notes...")
            
            col_btn_rule = st.columns([3, 1])[1]
            with col_btn_rule: submit_rule = st.form_submit_button("Save Safety Rule")
                
            if submit_rule:
                if not med_a or not med_b or not severity_desc: st.error("Fields incomplete.")
                elif med_a.lower() == med_b.lower(): st.error("Logical contradiction structural exception.")
                else:
                    is_duplicate = any((med_a.lower() == r["medicine_a"].lower() and med_b.lower() == r["medicine_b"].lower()) or 
                                       (med_a.lower() == r["medicine_b"].lower() and med_b.lower() == r["medicine_a"].lower()) for r in db["interaction_rules"])
                    if is_duplicate: st.warning("Configuration link relationship block already verified.")
                    else:
                        db["interaction_rules"].append({"medicine_a": med_a, "medicine_b": med_b, "description": severity_desc})
                        save_local_database(db)
                        st.success("Successfully logged database data records updates.")
                        st.rerun()

        st.markdown('<div class="section-title">Active Rules Directory</div>', unsafe_allow_html=True)
        if db["interaction_rules"]:
            df_rules = pd.DataFrame(db["interaction_rules"])
            df_rules.columns = ["Medicine A", "Medicine B", "Clinical Risk Description"]
            df_rules.insert(0, "Rule Reference ID", [f"DDI-{1000+i}" for i in range(len(df_rules))])
            st.dataframe(df_rules, use_container_width=True, hide_index=True)