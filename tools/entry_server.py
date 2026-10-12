"""Frozen-einstieg für den dev/browser-server (console exe)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.server import main

if __name__ == "__main__":
    main()
