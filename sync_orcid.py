import requests
import os

ORCID_ID = "0000-0003-2681-3440"
out_dir = "_publications"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def get_orcid_works(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {"Accept": "application/orcid+json"}
    response = requests.get(url, headers=headers)
    return response.json()

data = get_orcid_works(ORCID_ID)
for work in data.get('group', []):
    summary = work.get('work-summary', [{}])[0]
    
    # Extract details
    title = summary.get('title', {}).get('title', {}).get('value', 'Untitled')
    year = summary.get('publication-date', {}).get('year', {}).get('value', 'Unknown')
    path_title = title.replace(" ", "-").replace("/", "-")[:50]
    filename = f"{year}-{path_title}.md"
    
    # Create the Markdown file for the AcademicPages theme
    content = f"""---
title: "{title}"
collection: publications
permalink: /publication/{year}-{path_title}
date: {year}-01-01
venue: 'Journal Name (Syncing...)'
---
Automatically synced from ORCID.
"""
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Success! Created {len(data.get('group', []))} publication files.")
