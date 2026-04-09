#!/usr/bin/env python3
"""
Research Knowledge Base Management Tool

Manages the research/ directory for the WAT framework research agent.
Handles saving, loading, searching, and appending research files in Markdown format.

Usage:
    python tools/research_utils.py list                     # List all research topics
    python tools/research_utils.py find "topic"             # Find related research
    python tools/research_utils.py load "topic-slug"        # Load a research file
    python tools/research_utils.py save "topic" "content"   # Save/create research file
    python tools/research_utils.py append "slug" "section" "content"  # Append to section
    python tools/research_utils.py log "slug" "type" "queries" "findings"  # Add log entry
"""

import os
import re
import sys
import json
from datetime import datetime
from pathlib import Path

RESEARCH_DIR = Path(os.environ.get("RESEARCH_DIR", "research"))


def generate_slug(topic: str) -> str:
    """Generate a clean URL-safe slug from a topic string."""
    slug = topic.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:80]


def list_all_research() -> list[dict]:
    """List all research topics with their summaries and metadata."""
    results = []
    if not RESEARCH_DIR.exists():
        return results

    for f in sorted(RESEARCH_DIR.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        content = f.read_text(encoding="utf-8")
        title = ""
        summary = ""
        metadata = ""

        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)

        # Extract metadata line
        meta_match = re.search(r'^> (.+)$', content, re.MULTILINE)
        if meta_match:
            metadata = meta_match.group(1)

        # Extract executive summary
        summary_match = re.search(
            r'## Executive Summary\s*\n(.*?)(?=\n## |\Z)',
            content, re.DOTALL
        )
        if summary_match:
            summary = summary_match.group(1).strip()[:300]

        results.append({
            "slug": f.stem,
            "title": title,
            "metadata": metadata,
            "summary": summary,
            "path": str(f)
        })

    return results


def find_related_research(topic: str) -> list[dict]:
    """Search all research files for related topics using keyword matching."""
    all_research = list_all_research()
    if not all_research:
        return []

    topic_lower = topic.lower()
    topic_words = set(re.findall(r'\w+', topic_lower))
    topic_slug = generate_slug(topic)

    scored = []
    for r in all_research:
        score = 0

        # Exact slug match
        if r["slug"] == topic_slug:
            score += 100

        # Slug overlap
        slug_words = set(r["slug"].split("-"))
        slug_overlap = len(topic_words & slug_words)
        score += slug_overlap * 20

        # Title overlap
        title_words = set(re.findall(r'\w+', r["title"].lower()))
        title_overlap = len(topic_words & title_words)
        score += title_overlap * 15

        # Summary keyword match
        summary_lower = r["summary"].lower()
        for word in topic_words:
            if len(word) > 3 and word in summary_lower:
                score += 5

        if score > 0:
            scored.append({**r, "relevance_score": score})

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored


def load_research(slug: str) -> str | None:
    """Load a research file by its slug."""
    filepath = RESEARCH_DIR / f"{slug}.md"
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    # Try fuzzy match
    for f in RESEARCH_DIR.glob("*.md"):
        if slug in f.stem or f.stem in slug:
            return f.read_text(encoding="utf-8")
    return None


def save_research(topic: str, content: str) -> str:
    """Save or create a research file. Returns the file path."""
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    slug = generate_slug(topic)
    filepath = RESEARCH_DIR / f"{slug}.md"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def append_to_research(slug: str, section: str, new_content: str) -> bool:
    """Append content to a specific section of a research file."""
    filepath = RESEARCH_DIR / f"{slug}.md"
    if not filepath.exists():
        return False

    content = filepath.read_text(encoding="utf-8")

    # Find the section header and the next section
    pattern = rf'(## {re.escape(section)}\s*\n)(.*?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        section_header = match.group(1)
        section_body = match.group(2)
        updated_section = section_header + section_body.rstrip() + "\n" + new_content + "\n"
        content = content[:match.start()] + updated_section + content[match.end():]
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def update_research_log(slug: str, session_type: str, queries: str, findings: str) -> bool:
    """Add a new entry to the Research Log table in a research file."""
    date = datetime.now().strftime("%Y-%m-%d")
    new_row = f"| {date} | {session_type} | {queries} | {findings} |"
    return append_to_research(slug, "Research Log", new_row)


def update_metadata(slug: str) -> bool:
    """Update the metadata line (last updated date and session count)."""
    filepath = RESEARCH_DIR / f"{slug}.md"
    if not filepath.exists():
        return False

    content = filepath.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")

    # Count sessions from Research Log
    log_entries = re.findall(r'^\| \d{4}-\d{2}-\d{2}', content, re.MULTILINE)
    session_count = len(log_entries)

    # Update or create metadata line
    meta_pattern = r'^> Last updated:.*$'
    new_meta = f"> Last updated: {today} | Sessions: {session_count} | Status: actionable"

    if re.search(meta_pattern, content, re.MULTILINE):
        content = re.sub(meta_pattern, new_meta, content, flags=re.MULTILINE)
    else:
        # Insert after title
        content = re.sub(r'^(# .+\n)', rf'\1{new_meta}\n', content, flags=re.MULTILINE)

    filepath.write_text(content, encoding="utf-8")
    return True


# --- CLI Interface ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/research_utils.py <command> [args]")
        print("Commands: list, find, load, save, append, log")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        results = list_all_research()
        if not results:
            print("No research files found.")
        else:
            for r in results:
                print(f"\n--- {r['title']} ---")
                print(f"  Slug: {r['slug']}")
                print(f"  {r['metadata']}")
                if r['summary']:
                    print(f"  Summary: {r['summary'][:150]}...")

    elif command == "find":
        if len(sys.argv) < 3:
            print("Usage: python tools/research_utils.py find \"topic\"")
            sys.exit(1)
        topic = sys.argv[2]
        results = find_related_research(topic)
        if not results:
            print(f"No research found related to: {topic}")
        else:
            for r in results:
                match_type = "EXACT MATCH" if r["relevance_score"] >= 100 else "RELATED"
                print(f"\n[{match_type}] {r['title']} (score: {r['relevance_score']})")
                print(f"  Slug: {r['slug']}")
                print(f"  {r['metadata']}")
                if r['summary']:
                    print(f"  Summary: {r['summary'][:150]}...")

    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: python tools/research_utils.py load \"slug\"")
            sys.exit(1)
        content = load_research(sys.argv[2])
        if content:
            print(content)
        else:
            print(f"Research file not found for: {sys.argv[2]}")

    elif command == "save":
        if len(sys.argv) < 4:
            print("Usage: python tools/research_utils.py save \"topic\" \"content\"")
            sys.exit(1)
        path = save_research(sys.argv[2], sys.argv[3])
        print(f"Saved to: {path}")

    elif command == "append":
        if len(sys.argv) < 5:
            print("Usage: python tools/research_utils.py append \"slug\" \"section\" \"content\"")
            sys.exit(1)
        success = append_to_research(sys.argv[2], sys.argv[3], sys.argv[4])
        print("Appended successfully." if success else "Failed to append.")

    elif command == "log":
        if len(sys.argv) < 6:
            print("Usage: python tools/research_utils.py log \"slug\" \"type\" \"queries\" \"findings\"")
            sys.exit(1)
        success = update_research_log(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print("Log entry added." if success else "Failed to add log entry.")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
