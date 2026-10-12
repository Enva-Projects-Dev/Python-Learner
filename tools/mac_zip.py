"""Das gestagte mac-bundle zippen, .command/.sh bleiben ausführbar."""
import os
import sys
import zipfile

STAGE = sys.argv[1]
OUT = sys.argv[2]

EXEC_EXT = (".command", ".sh")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(STAGE):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            if name.endswith(".pyc"):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, STAGE)
            zi = zipfile.ZipInfo(rel.replace(os.sep, "/"))
            zi.date_time = (2026, 1, 1, 0, 0, 0)
            mode = 0o755 if name.endswith(EXEC_EXT) else 0o644
            zi.external_attr = mode << 16
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(full, "rb") as f:
                z.writestr(zi, f.read())
print(OUT)
