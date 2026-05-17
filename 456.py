# 456.py
# Runs automatically when a hip file is opened or created.
# Walks up from $HIP to find the project cg/ root, sets $JOB,
# and installs all HDAs from the cg/hda/ folder recursively.

import hou
import os

def find_cg_root(start_path):
    current = start_path
    while True:
        parent = os.path.dirname(current)
        if parent == current:
            return None
        if os.path.isdir(os.path.join(parent, "hda")) and \
           os.path.isdir(os.path.join(parent, "hip")):
            return parent
        current = parent

hip = hou.getenv("HIP")
if not hip:
    print("456.py: HIP not set, skipping")
else:
    cg_root = find_cg_root(hip)

    if cg_root:
        hda_path = os.path.join(cg_root, "hda")
        hou.hscript(f'setenv JOB="{cg_root}"')
        print(f"456.py: JOB set to {cg_root}")
        for root, dirs, files in os.walk(hda_path):
            for f in files:
                if f.endswith(".hda") or f.endswith(".otl") or f.endswith(".hdalc"):
                    full_path = os.path.join(root, f)
                    hou.hda.installFile(full_path)
                    print(f"456.py: installed {full_path}")
    else:
        print("456.py: could not find cg root, no HDA folder installed")
