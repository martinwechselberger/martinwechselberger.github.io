import requests
import os
import re

ORCID_ID = "0000-0003-2681-3440"
out_dir = "_publications"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

def clean_slug(text):
    # Remove LaTeX and special characters for the URL permalink
    text = re.sub(r'\$.*?\$', '', text) 
    return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-')

def get_orcid_works(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {"Accept": "application/orcid+json"}
    response = requests.get(url, headers=headers)
    return response.json()

data = get_orcid_works(ORCID_ID)
for work in data.get('group', []):
    summary = work.get('work-summary', [{}])[0]
    
    title = summary.get('title', {}).get('title', {}).get('value', 'Untitled')
    year = summary.get('publication-date', {}).get('year', {}).get('value', 'Unknown')
    
    # Create a URL-friendly version of the title
    safe_slug = clean_slug(title)
    filename = f"{year}-{safe_slug[:50]}.md"
    
    content = f"""---
title: "{title}"
collection: publications
category: manuscripts
permalink: /publication/{year}-{safe_slug[:50]}
date: {year}-01-01
venue: 'Journal Article'
---
Automatically synced from ORCID profile {ORCID_ID}.
"""
    with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)

print(f"Success! Created {len(data.get('group', []))} cleaned publication files.")
