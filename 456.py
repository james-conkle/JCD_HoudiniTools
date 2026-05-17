# 456.py
# Runs automatically when a hip file is opened or created.
# Walks up the directory tree from $HIP to find the project cg/ root
# by locating sibling hip/ and hda/ folders. Sets $JOB to the cg/ root
# and recursively installs all HDAs from cg/hda/. Works on Mac and Windows.
# Compatible with HQueue farm rendering.

import hou
import os

CG_MARKERS = ("hda", "hip")
HDA_EXTS = (".hda", ".otl", ".hdalc", ".hdanc", ".otlnc")

def find_cg_root(start_path):
    current = os.path.abspath(start_path)
    while True:
        if all(os.path.isdir(os.path.join(current, m)) for m in CG_MARKERS):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent

hip = hou.getenv("HIP")
if not hip:
    print("456.py: HIP not set, skipping")
else:
    cg_root = find_cg_root(hip)
    if not cg_root:
        print("456.py: could not find cg root, no HDAs installed")
    else:
        cg_root_fwd = cg_root.replace("\\", "/")
        hou.putenv("JOB", cg_root_fwd)
        hou.hscript(f'setenv JOB="{cg_root_fwd}"')
        print(f"456.py: JOB set to {cg_root_fwd}")

        hda_path = os.path.join(cg_root, "hda")
        for root, _, files in os.walk(hda_path):
            for f in files:
                if f.lower().endswith(HDA_EXTS):
                    full_path = os.path.join(root, f).replace("\\", "/")
                    try:
                        hou.hda.installFile(full_path, force_use_assets=True)
                        print(f"456.py: installed {full_path}")
                    except hou.OperationFailed as e:
                        print(f"456.py: FAILED {full_path}: {e}")
