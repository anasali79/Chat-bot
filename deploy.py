import os
import sys
from pathlib import Path

def prepare_for_deployment():
    """Prepare the project for cloud deployment"""
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    
    print("✅ Deployment preparation complete!")
    print("Next steps:")
    print("1. git init")
    print("2. git add .")
    print("3. git commit -m 'Initial commit'")
    print("4. Push to GitHub")
    print("5. Deploy to Streamlit Cloud")

if __name__ == "__main__":
    prepare_for_deployment()