"""
Run this from inside your RehabSense-main folder:
    python debug_login.py

It will tell you exactly what is wrong.
"""
import os, json, glob

print("=" * 60)
print("RehabSense Login Debugger")
print("=" * 60)

# Where is this script running from?
cwd = os.getcwd()
print(f"\n1. You are running from:\n   {cwd}")

# Try to find the patients folder
candidates = [
    os.path.join(cwd, "data", "patients"),
    os.path.join(cwd, "..", "data", "patients"),
    os.path.join(os.path.dirname(__file__), "data", "patients"),
    os.path.join(os.path.dirname(__file__), "..", "data", "patients"),
]

found_patients_dir = None
for c in candidates:
    c = os.path.abspath(c)
    if os.path.exists(c):
        found_patients_dir = c
        break

print(f"\n2. Patient data folder found at:\n   {found_patients_dir or '❌ NOT FOUND'}")

if not found_patients_dir:
    print("\n❌ PROBLEM: Cannot find the data/patients folder.")
    print("   Make sure you are running this script from inside RehabSense-main/")
    input("\nPress Enter to exit...")
    exit()

# List all patient files and their passwords
print(f"\n3. Patient credentials in the files:")
print(f"   {'Name':<22} {'ID':<16} {'Password'}")
print(f"   {'-'*22} {'-'*16} {'-'*20}")

files = sorted(glob.glob(os.path.join(found_patients_dir, "*.json")))
if not files:
    print("   ❌ No patient JSON files found!")
else:
    for f in files:
        try:
            p = json.load(open(f, encoding='utf-8'))
            name = p.get('name', '?')
            pid  = p.get('patient_id', '?')
            pw   = p.get('password', 'MISSING')
            print(f"   {name:<22} {pid:<16} {pw}")
        except Exception as e:
            print(f"   ❌ Error reading {f}: {e}")

# Test specific login
print(f"\n4. Testing login for 7D42PL2...")
patient_file = os.path.join(found_patients_dir, "patient_B.json")
if os.path.exists(patient_file):
    p = json.load(open(patient_file, encoding='utf-8'))
    stored_pw = p.get('password', '')
    print(f"   Stored password: '{stored_pw}'")
    print(f"   Test 'neww@342217': {'✅ MATCH' if stored_pw == 'neww@342217' else '❌ NO MATCH'}")
    print(f"   Test 'newp@117789': {'✅ MATCH' if stored_pw == 'newp@117789' else '❌ NO MATCH'}")
else:
    print(f"   ❌ patient_B.json not found at {patient_file}")

# Check which app.py is being used by Flask
print(f"\n5. Checking backend/app.py path resolution...")
backend_app = os.path.join(cwd, "backend", "app.py")
if os.path.exists(backend_app):
    # Read and find the PROJECT_ROOT line
    content = open(backend_app, encoding='utf-8').read()
    if '_BACKEND_DIR' in content:
        print("   ✅ NEW version of backend/app.py (path fix applied)")
    elif "os.path.join(os.path.dirname(__file__), '..')" in content:
        print("   ⚠️  OLD version of backend/app.py (path fix NOT applied yet)")
    # Simulate what it would compute
    this_file = os.path.abspath(backend_app)
    backend_dir = os.path.dirname(this_file)
    project_root = os.path.dirname(backend_dir)
    data_dir = os.path.join(project_root, 'data', 'patients')
    print(f"   Computed DATA_DIR: {data_dir}")
    print(f"   DATA_DIR exists: {os.path.exists(data_dir)}")
else:
    print(f"   ❌ backend/app.py not found at {backend_app}")
    print(f"   Are you running from inside RehabSense-main/?")

print("\n" + "=" * 60)
print("Copy and send the output above to diagnose the issue.")
print("=" * 60)
input("\nPress Enter to exit...")