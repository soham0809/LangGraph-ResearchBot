"""Setup script for the dual-agent research system."""
import os
import sys
from pathlib import Path

def ensure_directory_structure():
    """Ensure all required directories exist."""
    # Define the directories to create
    directories = [
        "agents",
        "graph",
        "utils",
    ]
    
    # Create directories if they don't exist
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Directory structure created successfully.")
    
if __name__ == "__main__":
    ensure_directory_structure() 