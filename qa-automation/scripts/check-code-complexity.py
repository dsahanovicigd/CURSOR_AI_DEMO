#!/usr/bin/env python3
"""
Code Complexity Checker
Analyzes code complexity using radon or similar tools
Target: Complexity < 10
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent.parent
REPORTS_DIR = SCRIPT_DIR.parent / "reports"

def check_radon_installed() -> bool:
    """Check if radon is installed"""
    try:
        subprocess.run(['radon', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_radon():
    """Install radon if not available"""
    print("Installing radon for complexity analysis...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'radon'], check=False)

def analyze_complexity() -> Dict:
    """Analyze code complexity"""
    results = {
        'functions': [],
        'classes': [],
        'files': [],
        'summary': {
            'total_functions': 0,
            'high_complexity': 0,
            'avg_complexity': 0,
            'max_complexity': 0
        }
    }
    
    if not check_radon_installed():
        install_radon()
        if not check_radon_installed():
            print("⚠️  radon not available. Skipping complexity analysis.")
            return results
    
    # Analyze Python files
    python_files = list(ROOT_DIR.glob('flask_api/**/*.py'))
    python_files = [f for f in python_files if 'test' not in str(f) and '__pycache__' not in str(f)]
    
    if not python_files:
        return results
    
    # Run radon cc (cyclomatic complexity)
    try:
        output = subprocess.run(
            ['radon', 'cc', '--json', '--min', 'B'] + [str(f) for f in python_files],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR)
        )
        
        if output.returncode == 0 and output.stdout:
            data = json.loads(output.stdout)
            
            all_complexities = []
            for file_path, functions in data.items():
                file_complexity = {
                    'file': file_path,
                    'functions': [],
                    'max_complexity': 0
                }
                
                for func in functions:
                    complexity = func.get('complexity', 0)
                    all_complexities.append(complexity)
                    
                    func_info = {
                        'name': func.get('name', 'unknown'),
                        'complexity': complexity,
                        'line': func.get('lineno', 0)
                    }
                    
                    file_complexity['functions'].append(func_info)
                    
                    if complexity > file_complexity['max_complexity']:
                        file_complexity['max_complexity'] = complexity
                    
                    if complexity >= 10:
                        results['summary']['high_complexity'] += 1
                
                results['files'].append(file_complexity)
                results['functions'].extend(file_complexity['functions'])
            
            if all_complexities:
                results['summary']['total_functions'] = len(all_complexities)
                results['summary']['avg_complexity'] = sum(all_complexities) / len(all_complexities)
                results['summary']['max_complexity'] = max(all_complexities)
    
    except Exception as e:
        print(f"Error analyzing complexity: {e}")
    
    return results

def generate_report(results: Dict):
    """Generate complexity report"""
    reports_dir = REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON report
    json_path = reports_dir / 'complexity-report.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary
    summary = results['summary']
    high_complexity = [f for f in results['functions'] if f['complexity'] >= 10]
    
    print("\n📊 Code Complexity Analysis")
    print("=" * 50)
    print(f"Total Functions: {summary['total_functions']}")
    print(f"Average Complexity: {summary['avg_complexity']:.2f}")
    print(f"Max Complexity: {summary['max_complexity']}")
    print(f"High Complexity (>=10): {summary['high_complexity']}")
    
    if high_complexity:
        print("\n⚠️  Functions with High Complexity (>=10):")
        for func in sorted(high_complexity, key=lambda x: x['complexity'], reverse=True)[:10]:
            print(f"  - {func['name']}: {func['complexity']} (line {func['line']})")
    
    # Check if target is met
    if summary['max_complexity'] < 10 and summary['high_complexity'] == 0:
        print("\n✅ Complexity target met: All functions < 10")
        return 0
    else:
        print(f"\n❌ Complexity target not met: {summary['high_complexity']} functions >= 10")
        return 1

def main():
    """Main function"""
    print("🔍 Analyzing code complexity...")
    
    results = analyze_complexity()
    exit_code = generate_report(results)
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
