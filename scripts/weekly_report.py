#!/usr/bin/env python3
"""
Weekly Report Generator for NACA Airfoil Kit Pro
Collects download statistics and user feedback from GitHub releases
"""

import json
import os
from datetime import datetime, timedelta
import subprocess
from pathlib import Path

def get_github_token():
    """Retrieve GitHub token from environment"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    return token

def run_gh_command(command):
    """Execute a GitHub CLI command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            env={**os.environ, 'GITHUB_TOKEN': get_github_token()}
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def get_release_stats():
    """Fetch release download statistics from GitHub"""
    repo = "Ali-Marandi/naca-airfoil-kit"
    
    # Get all releases
    cmd = f'gh release list --repo {repo} --json tagName,name,publishedAt,assets --limit 100'
    output = run_gh_command(cmd)
    
    if not output:
        return None
    
    try:
        releases = json.loads(output)
    except json.JSONDecodeError:
        print("Failed to parse GitHub releases")
        return None
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'repository': repo,
        'total_releases': len(releases),
        'releases': []
    }
    
    total_downloads = 0
    
    for release in releases:
        release_info = {
            'tag': release.get('tagName'),
            'name': release.get('name'),
            'published_at': release.get('publishedAt'),
            'assets': []
        }
        
        assets = release.get('assets', [])
        for asset in assets:
            asset_info = {
                'name': asset.get('name'),
                'download_count': asset.get('downloadCount', 0),
                'size': asset.get('size', 0)
            }
            release_info['assets'].append(asset_info)
            total_downloads += asset.get('downloadCount', 0)
        
        stats['releases'].append(release_info)
    
    stats['total_downloads'] = total_downloads
    return stats

def get_repository_stats():
    """Fetch repository statistics"""
    repo = "Ali-Marandi/naca-airfoil-kit"
    
    # Get repository info
    cmd = f'gh repo view {repo} --json stargazerCount,forkCount,watchers,description'
    output = run_gh_command(cmd)
    
    if not output:
        return None
    
    try:
        repo_data = json.loads(output)
    except json.JSONDecodeError:
        print("Failed to parse repository data")
        return None
    
    return {
        'stars': repo_data.get('stargazerCount', 0),
        'forks': repo_data.get('forkCount', 0),
        'watchers': repo_data.get('watchers', 0),
        'description': repo_data.get('description', '')
    }

def get_issues_and_discussions():
    """Fetch open issues and discussions"""
    repo = "Ali-Marandi/naca-airfoil-kit"
    
    # Get open issues
    cmd = f'gh issue list --repo {repo} --state open --json number,title,createdAt'
    issues_output = run_gh_command(cmd)
    
    issues = []
    if issues_output:
        try:
            issues = json.loads(issues_output)
        except json.JSONDecodeError:
            pass
    
    return {
        'open_issues': len(issues),
        'recent_issues': issues[:5] if issues else []
    }

def generate_report():
    """Generate comprehensive weekly report"""
    report = {
        'report_type': 'Weekly Statistics',
        'generated_at': datetime.now().isoformat(),
        'week_ending': (datetime.now() + timedelta(days=1)).isoformat(),
        'repository': 'Ali-Marandi/naca-airfoil-kit'
    }
    
    print("Fetching release statistics...")
    release_stats = get_release_stats()
    if release_stats:
        report['releases'] = release_stats
    
    print("Fetching repository statistics...")
    repo_stats = get_repository_stats()
    if repo_stats:
        report['repository_stats'] = repo_stats
    
    print("Fetching issues and feedback...")
    issues = get_issues_and_discussions()
    if issues:
        report['community'] = issues
    
    return report

def save_report(report, output_dir='reports'):
    """Save report to JSON file"""
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/weekly_report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {filename}")
    return filename

def format_report_summary(report):
    """Format report as human-readable summary"""
    summary = []
    summary.append("=" * 60)
    summary.append("NACA AIRFOIL KIT PRO - WEEKLY REPORT")
    summary.append("=" * 60)
    summary.append(f"Generated: {report['generated_at']}")
    summary.append(f"Week Ending: {report['week_ending']}")
    summary.append("")
    
    if 'releases' in report:
        releases = report['releases']
        summary.append("📊 RELEASE STATISTICS")
        summary.append("-" * 60)
        summary.append(f"Total Releases: {releases['total_releases']}")
        summary.append(f"Total Downloads: {releases['total_downloads']}")
        summary.append("")
        
        for release in releases['releases'][:3]:  # Top 3 releases
            summary.append(f"Release: {release['tag']}")
            summary.append(f"  Published: {release['published_at']}")
            for asset in release['assets']:
                summary.append(f"  - {asset['name']}: {asset['download_count']} downloads")
            summary.append("")
    
    if 'repository_stats' in report:
        repo = report['repository_stats']
        summary.append("⭐ REPOSITORY METRICS")
        summary.append("-" * 60)
        summary.append(f"Stars: {repo['stars']}")
        summary.append(f"Forks: {repo['forks']}")
        summary.append(f"Watchers: {repo['watchers']}")
        summary.append("")
    
    if 'community' in report:
        community = report['community']
        summary.append("💬 COMMUNITY FEEDBACK")
        summary.append("-" * 60)
        summary.append(f"Open Issues: {community['open_issues']}")
        summary.append("")
        
        if community['recent_issues']:
            summary.append("Recent Issues:")
            for issue in community['recent_issues']:
                summary.append(f"  #{issue['number']}: {issue['title']}")
        summary.append("")
    
    summary.append("=" * 60)
    summary.append("End of Report")
    summary.append("=" * 60)
    
    return "\n".join(summary)

def main():
    """Main execution"""
    print("Starting weekly report generation...")
    
    try:
        report = generate_report()
        
        # Save JSON report
        report_file = save_report(report)
        
        # Print summary
        summary = format_report_summary(report)
        print("\n" + summary)
        
        # Save summary as text
        summary_file = report_file.replace('.json', '.txt')
        with open(summary_file, 'w') as f:
            f.write(summary)
        print(f"Summary saved to {summary_file}")
        
        return 0
    except Exception as e:
        print(f"Error generating report: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
