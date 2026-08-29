"""Legacy entry point redirecting to root main.py."""
import os
import sys

# Add repository root to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from main import main

if __name__ == "__main__":
    main()
