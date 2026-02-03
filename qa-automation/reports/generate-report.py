#!/usr/bin/env python3
"""
Consolidated Quality Report Generator
Combines dashboard generation and recommendations generation
"""

import sys
import os
import subprocess
from pathlib import Path

# Check if jinja2 is installed, install if needed
def ensure_dependencies():
    """Ensure required Python dependencies are installed"""
    try:
        import jinja2
        return True
    except ImportError:
        print("⚠️  jinja2 not found. Attempting to install...")
        try:
            # Try user install first (safer for macOS)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--user", "jinja2>=3.0.0"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ jinja2 installed successfully")
                # Try importing again
                try:
                    import jinja2
                    return True
                except ImportError:
                    print("⚠️  Installation succeeded but import failed.")
                    print("   The package may need a Python restart to be recognized.")
                    print("   Please run the script again.")
                    return False
            else:
                # Check if it's the externally-managed-environment error
                if "externally-managed-environment" in result.stderr:
                    print("\n❌ Python environment is externally managed (macOS/Homebrew).")
                    print("\n📋 Please install jinja2 manually using one of these methods:\n")
                    print("   1. User install (recommended):")
                    print("      python3 -m pip install --user jinja2\n")
                    print("   2. System install (requires --break-system-packages):")
                    print("      python3 -m pip install --break-system-packages jinja2\n")
                    print("   3. Using virtual environment:")
                    print("      python3 -m venv venv")
                    print("      source venv/bin/activate")
                    print("      pip install jinja2\n")
                    return False
                else:
                    print(f"❌ Installation failed: {result.stderr}")
                    print("   Please install manually: python3 -m pip install --user jinja2")
                    return False
        except Exception as e:
            print(f"❌ Failed to install jinja2: {e}")
            print("   Please install manually: python3 -m pip install --user jinja2")
            return False

# Ensure dependencies before importing
if not ensure_dependencies():
    sys.exit(1)

# Add parent directory to path to import modules
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import the existing generators
from generate_dashboard import main as generate_dashboard_main
from generate_recommendations import main as generate_recommendations

def main():
    """Generate both dashboard and recommendations"""
    print("📊 Generating Quality Dashboard...")
    try:
        generate_dashboard_main()
        print("✅ Dashboard generated successfully")
    except Exception as e:
        print(f"❌ Dashboard generation failed: {e}")
        return 1
    
    print("\n💡 Generating Recommendations...")
    try:
        generate_recommendations()
        print("✅ Recommendations generated successfully")
    except Exception as e:
        print(f"❌ Recommendations generation failed: {e}")
        return 1
    
    print("\n✅ Quality reports generated successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
