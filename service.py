import streamlit as st
import sqlite3
import random

# ---------- DATABASE CONNECTION ----------
conn = sqlite3.connect("itsm.db", check_same_thread=False)
c = conn.cursor()

# ---------- TABLES ----------
c.execute("CREATE TABLE IF NOT EXISTS assets(id INTEGER PRIMARY KEY, name TEXT, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY, user TEXT, issue TEXT, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS changes(id INTEGER PRIMARY KEY, title TEXT, approval TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY, system TEXT, severity TEXT)")
conn.commit()

# ---------- TITLE ----------
st.title("🖥️ IT Infrastructure Service Management System")

menu = [
    "Asset Management",
    "Service Desk",
    "Employee Management",
    "Change Management",
    "Incident Management",
    "Infrastructure Monitoring"
]

choice = st.sidebar.selectbox("Select Module", menu)

# ================= ASSET MANAGEMENT =================
if choice == "Asset Management":
    st.header("💻 IT Asset Management")

    asset = st.text_input("Asset Name")

    if st.button("Add Asset"):
        c.execute("INSERT INTO assets(name,status) VALUES(?,?)", (asset,"Active"))
        conn.commit()
        st.success("Asset Added")

    asset_id = st.number_input("Asset ID", min_value=1, step=1, format="%d")
    status = st.selectbox("Update Status", ["Active","Maintenance","Retired"])

    if st.button("Update Asset"):
        c.execute("UPDATE assets SET status=? WHERE id=?", (status,asset_id))
        conn.commit()
        st.success("Asset Updated")

    data = c.execute("SELECT * FROM assets").fetchall()
    st.table(data)

# ================= SERVICE DESK =================
elif choice == "Service Desk":
    st.header("🎫 Service Desk Ticket System")

    user = st.text_input("Employee Name")
    issue = st.text_input("Issue Description")

    if st.button("Create Ticket"):
        c.execute("INSERT INTO tickets(user,issue,status) VALUES(?,?,?)",
                  (user,issue,"Open"))
        conn.commit()
        st.success("Ticket Created")

    ticket_id = st.number_input("Ticket ID", min_value=1, step=1, format="%d")
    ticket_status = st.selectbox("Ticket Status",["Open","In Progress","Resolved"])

    if st.button("Update Ticket"):
        c.execute("UPDATE tickets SET status=? WHERE id=?",
                  (ticket_status,ticket_id))
        conn.commit()
        st.success("Ticket Updated")

    data = c.execute("SELECT * FROM tickets").fetchall()
    st.table(data)

# ================= EMPLOYEE MANAGEMENT =================
elif choice == "Employee Management":
    st.header("👨‍💼 Employee Management")

    name = st.text_input("Employee Name")
    dept = st.text_input("Department")

    if st.button("Add Employee"):
        c.execute("INSERT INTO employees(name,department) VALUES(?,?)",
                  (name,dept))
        conn.commit()
        st.success("Employee Added")

    data = c.execute("SELECT * FROM employees").fetchall()
    st.table(data)

# ================= CHANGE MANAGEMENT =================
elif choice == "Change Management":
    st.header("🔄 Change Management")

    title = st.text_input("Change Title")

    if st.button("Request Change"):
        c.execute("INSERT INTO changes(title,approval) VALUES(?,?)",
                  (title,"Pending"))
        conn.commit()
        st.success("Change Requested")

    change_id = st.number_input("Change ID", min_value=1, step=1, format="%d")
    decision = st.selectbox("Approval",["Approved","Rejected"])

    if st.button("Update Change"):
        c.execute("UPDATE changes SET approval=? WHERE id=?",
                  (decision,change_id))
        conn.commit()
        st.success("Change Updated")

    data = c.execute("SELECT * FROM changes").fetchall()
    st.table(data)

# ================= INCIDENT MANAGEMENT =================
elif choice == "Incident Management":
    st.header("🚨 Incident Management")

    system = st.text_input("Affected System")
    severity = st.selectbox("Severity",["Low","Medium","High","Critical"])

    if st.button("Report Incident"):
        c.execute("INSERT INTO incidents(system,severity) VALUES(?,?)",
                  (system,severity))
        conn.commit()
        st.success("Incident Reported")

    data = c.execute("SELECT * FROM incidents").fetchall()
    st.table(data)

# ================= INFRASTRUCTURE MONITORING =================
elif choice == "Infrastructure Monitoring":
    st.header("📡 Infrastructure Health Monitoring")

    cpu = random.randint(20,95)
    ram = random.randint(30,95)
    network = random.randint(10,100)

    st.write("CPU Usage:", cpu, "%")
    st.write("RAM Usage:", ram, "%")
    st.write("Network Load:", network, "%")

    if cpu > 85 or ram > 85 or network > 90:
        st.error("⚠️ Infrastructure Overload Detected")
    else:
        st.success("✅ Systems Operating Normally")