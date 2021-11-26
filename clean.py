import os

try:
    os.remove("example.pdf")
except Exception:
    pass
try:
    os.remove("example.html")
except Exception:
    pass
try:
    os.remove("report.pdf")
except Exception:
    pass