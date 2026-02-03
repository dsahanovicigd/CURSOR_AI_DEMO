#!/usr/bin/env python3
"""
AI-Generated Improvement Recommendations
Analyzes QA results and generates actionable recommendations
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_dashboard_data():
    """Load dashboard data"""
    data_path = Path(__file__).parent / 'dashboard-data.json'
    if not data_path.exists():
        return None
    
    with open(data_path, 'r') as f:
        return json.load(f)

def generate_recommendations(data):
    """Generate AI-powered recommendations based on QA data"""
    recommendations = []
    priority_map = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
    
    # Test coverage recommendations
    if data.get('pytest'):
        pytest = data['pytest']
        if pytest['success_rate'] < 80:
            recommendations.append({
                'category': 'Testing',
                'priority': 'high',
                'title': 'Backend Test Coverage Below Target',
                'description': f"Current test success rate is {pytest['success_rate']:.1f}%. Target is 80%+.",
                'action': [
                    'Review failing tests in pytest-results.xml',
                    'Add unit tests for uncovered code paths',
                    'Fix flaky tests that are causing intermittent failures',
                    'Consider adding integration tests for critical workflows'
                ],
                'metrics': {
                    'current': pytest['success_rate'],
                    'target': 80
                }
            })
        elif pytest['failed'] > 0:
            recommendations.append({
                'category': 'Testing',
                'priority': 'medium',
                'title': 'Some Backend Tests Failing',
                'description': f"{pytest['failed']} test(s) are currently failing.",
                'action': [
                    'Investigate failing tests immediately',
                    'Check if failures are due to recent code changes',
                    'Review test fixtures and setup/teardown logic',
                    'Ensure database migrations are up to date'
                ]
            })
    
    if data.get('jest'):
        jest = data['jest']
        if jest.get('total', 0) == 0:
            recommendations.append({
                'category': 'Testing',
                'priority': 'high',
                'title': 'No Frontend Unit Tests Found',
                'description': 'Jest tests are not configured or no test files exist.',
                'action': [
                    'Create unit tests for React components',
                    'Add tests for utility functions and hooks',
                    'Set up Jest configuration (already created)',
                    'Aim for 70%+ code coverage'
                ]
            })
        elif jest['success_rate'] < 70:
            recommendations.append({
                'category': 'Testing',
                'priority': 'high',
                'title': 'Frontend Test Coverage Needs Improvement',
                'description': f"Current test success rate is {jest['success_rate']:.1f}%.",
                'action': [
                    'Add tests for components without coverage',
                    'Test edge cases and error handling',
                    'Mock external dependencies properly',
                    'Use React Testing Library best practices'
                ]
            })
    
    # Code quality recommendations
    if data.get('pylint'):
        pylint = data['pylint']
        if pylint['score'] < 7:
            recommendations.append({
                'category': 'Code Quality',
                'priority': 'high',
                'title': 'Backend Code Quality Below Standard',
                'description': f"Pylint score is {pylint['score']:.1f}/10. Target is 8.0+.",
                'action': [
                    f"Fix {pylint['errors']} error(s) and {pylint['warnings']} warning(s)",
                    'Review Pylint report for specific issues',
                    'Refactor complex functions (reduce cyclomatic complexity)',
                    'Add docstrings to classes and functions',
                    'Follow PEP 8 style guidelines'
                ],
                'metrics': {
                    'current': pylint['score'],
                    'target': 8.0
                }
            })
        elif pylint['warnings'] > 20:
            recommendations.append({
                'category': 'Code Quality',
                'priority': 'medium',
                'title': 'High Number of Code Quality Warnings',
                'description': f"{pylint['warnings']} warnings detected in codebase.",
                'action': [
                    'Address warnings incrementally',
                    'Focus on high-impact warnings first',
                    'Configure Pylint to ignore false positives',
                    'Set up pre-commit hooks to catch issues early'
                ]
            })
    
    # Security recommendations
    snyk_total = 0
    snyk_high = 0
    
    if data.get('snyk_frontend'):
        snyk_total += data['snyk_frontend']['total']
        snyk_high += data['snyk_frontend']['high']
    
    if data.get('snyk_backend'):
        snyk_total += data['snyk_backend']['total']
        snyk_high += data['snyk_backend']['high']
    
    if snyk_high > 0:
        recommendations.append({
            'category': 'Security',
            'priority': 'high',
            'title': 'Critical Security Vulnerabilities Detected',
            'description': f"{snyk_high} high-severity vulnerability(ies) found in dependencies.",
            'action': [
                'Review Snyk report for detailed vulnerability information',
                'Update vulnerable dependencies to patched versions',
                'Consider alternative packages if updates are not available',
                'Implement security patches immediately',
                'Set up automated dependency updates (Dependabot)'
            ]
        })
    elif snyk_total > 10:
        recommendations.append({
            'category': 'Security',
            'priority': 'medium',
            'title': 'Multiple Security Vulnerabilities Found',
            'description': f"{snyk_total} total vulnerability(ies) detected.",
            'action': [
                'Review and prioritize vulnerabilities by severity',
                'Create a security update plan',
                'Test updates in staging before production',
                'Monitor for new vulnerabilities regularly'
            ]
        })
    
    # Performance recommendations
    if data.get('lighthouse'):
        for result in data['lighthouse']:
            if result['performance'] < 80:
                recommendations.append({
                    'category': 'Performance',
                    'priority': 'high',
                    'title': f"Performance Score Below Target for {result['url']}",
                    'description': f"Lighthouse performance score is {result['performance']:.0f}/100.",
                    'action': [
                        'Optimize images (use WebP, lazy loading)',
                        'Implement code splitting and lazy loading',
                        'Minify and compress JavaScript/CSS',
                        'Use CDN for static assets',
                        'Enable browser caching',
                        'Reduce render-blocking resources',
                        'Optimize critical rendering path'
                    ],
                    'metrics': {
                        'current': result['performance'],
                        'target': 80
                    }
                })
            
            if result['accessibility'] < 90:
                recommendations.append({
                    'category': 'Accessibility',
                    'priority': 'medium',
                    'title': f"Accessibility Issues Detected for {result['url']}",
                    'description': f"Accessibility score is {result['accessibility']:.0f}/100.",
                    'action': [
                        'Add ARIA labels to interactive elements',
                        'Ensure proper heading hierarchy',
                        'Improve color contrast ratios',
                        'Add alt text to images',
                        'Test with screen readers',
                        'Ensure keyboard navigation works'
                    ]
                })
    
    if data.get('k6'):
        k6 = data['k6']
        if k6['failed_requests'] > 1:
            recommendations.append({
                'category': 'Performance',
                'priority': 'high',
                'title': 'High Error Rate Under Load',
                'description': f"Failed request rate is {k6['failed_requests']:.2f}% under load.",
                'action': [
                    'Investigate server errors and timeouts',
                    'Check database connection pooling',
                    'Review API rate limiting configuration',
                    'Optimize slow database queries',
                    'Consider horizontal scaling',
                    'Add retry logic for transient failures'
                ]
            })
        
        if k6['p95_response_time'] > 2000:
            recommendations.append({
                'category': 'Performance',
                'priority': 'medium',
                'title': 'Slow Response Times Under Load',
                'description': f"P95 response time is {k6['p95_response_time']:.0f}ms (target: <2000ms).",
                'action': [
                    'Profile slow endpoints',
                    'Optimize database queries (add indexes)',
                    'Implement caching for frequently accessed data',
                    'Consider using a CDN',
                    'Review and optimize API endpoints',
                    'Monitor database query performance'
                ],
                'metrics': {
                    'current': k6['p95_response_time'],
                    'target': 2000
                }
            })
    
    # General recommendations
    if not recommendations:
        recommendations.append({
            'category': 'General',
            'priority': 'low',
            'title': 'Excellent Quality Metrics!',
            'description': 'All quality metrics are within acceptable ranges.',
            'action': [
                'Continue maintaining high code quality standards',
                'Keep dependencies up to date',
                'Monitor metrics regularly',
                'Consider adding more edge case tests'
            ]
        })
    
    return recommendations

def generate_markdown_report(recommendations):
    """Generate markdown report"""
    markdown = "# 🤖 AI-Generated Quality Improvement Recommendations\n\n"
    markdown += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown += f"Total Recommendations: {len(recommendations)}\n\n"
    
    # Group by priority
    high_priority = [r for r in recommendations if r['priority'] == 'high']
    medium_priority = [r for r in recommendations if r['priority'] == 'medium']
    low_priority = [r for r in recommendations if r['priority'] == 'low']
    
    if high_priority:
        markdown += "## 🔴 High Priority\n\n"
        for rec in high_priority:
            markdown += f"### {rec['title']}\n\n"
            markdown += f"**Category:** {rec['category']}\n\n"
            markdown += f"**Description:** {rec['description']}\n\n"
            markdown += "**Recommended Actions:**\n"
            for action in rec['action']:
                markdown += f"- {action}\n"
            if 'metrics' in rec:
                markdown += f"\n**Metrics:** Current: {rec['metrics']['current']}, Target: {rec['metrics']['target']}\n"
            markdown += "\n---\n\n"
    
    if medium_priority:
        markdown += "## 🟡 Medium Priority\n\n"
        for rec in medium_priority:
            markdown += f"### {rec['title']}\n\n"
            markdown += f"**Category:** {rec['category']}\n\n"
            markdown += f"**Description:** {rec['description']}\n\n"
            markdown += "**Recommended Actions:**\n"
            for action in rec['action']:
                markdown += f"- {action}\n"
            if 'metrics' in rec:
                markdown += f"\n**Metrics:** Current: {rec['metrics']['current']}, Target: {rec['metrics']['target']}\n"
            markdown += "\n---\n\n"
    
    if low_priority:
        markdown += "## 🟢 Low Priority\n\n"
        for rec in low_priority:
            markdown += f"### {rec['title']}\n\n"
            markdown += f"**Category:** {rec['category']}\n\n"
            markdown += f"**Description:** {rec['description']}\n\n"
            markdown += "**Recommended Actions:**\n"
            for action in rec['action']:
                markdown += f"- {action}\n"
            markdown += "\n---\n\n"
    
    return markdown

def main():
    """Main function"""
    data = load_dashboard_data()
    
    if not data:
        print("⚠️  No dashboard data found. Run generate_dashboard.py first.")
        return
    
    recommendations = generate_recommendations(data)
    
    # Save JSON
    reports_dir = Path(__file__).parent
    reports_dir.mkdir(exist_ok=True)
    
    json_path = reports_dir / 'recommendations.json'
    with open(json_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(recommendations),
            'high_priority': len([r for r in recommendations if r['priority'] == 'high']),
            'medium_priority': len([r for r in recommendations if r['priority'] == 'medium']),
            'low_priority': len([r for r in recommendations if r['priority'] == 'low']),
            'recommendations': recommendations
        }, f, indent=2)
    
    # Save Markdown
    markdown = generate_markdown_report(recommendations)
    md_path = reports_dir / 'recommendations.md'
    with open(md_path, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Generated {len(recommendations)} recommendations")
    print(f"   - High priority: {len([r for r in recommendations if r['priority'] == 'high'])}")
    print(f"   - Medium priority: {len([r for r in recommendations if r['priority'] == 'medium'])}")
    print(f"   - Low priority: {len([r for r in recommendations if r['priority'] == 'low'])}")
    print(f"📄 Reports saved to: {reports_dir}")

if __name__ == '__main__':
    main()
