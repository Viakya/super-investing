"""Load research documents and preserve their source metadata."""

from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESEARCH_DIR = PROJECT_ROOT / "research_pack"

# This file contains assignment instructions, not company research.
EXCLUDED_FILES = {"README.md"}


def parse_document(path: Path) -> dict:
    """Extract the document's text and source metadata."""
    text = path.read_text(encoding="utf-8")

    metadata = {}
    frontmatter = re.match(
        r"\A---\s*\n(.*?)\n---\s*\n?",
        text,
        flags=re.DOTALL,
    )

    if frontmatter:
        for line in frontmatter.group(1).splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key.strip().lower()] = value.strip()

        content = text[frontmatter.end():].strip()
    else:
        content = text.strip()

    return {
        "filename": path.name,
        "source": metadata.get("source", "Unknown source"),
        "url": metadata.get("url", ""),
        "published": metadata.get("published", "Unknown date"),
        "type": metadata.get("type", "Unknown type"),
        "content": content,
    }


def load_documents(directory: Path = DEFAULT_RESEARCH_DIR) -> list[dict]:
    """Load Markdown research files in a deterministic order."""
    if not directory.is_dir():
        raise FileNotFoundError(f"Research directory not found: {directory}")

    paths = sorted(
        path for path in directory.glob("*.md")
        if path.name not in EXCLUDED_FILES
    )

    if not paths:
        raise ValueError(f"No research documents found in {directory}")

    return [parse_document(path) for path in paths]


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} research documents.\n")

    for index, document in enumerate(documents, start=1):
        print(f"[S{index}] {document['filename']}")
        print(f"  Source: {document['source']}")
        print(f"  Date:   {document['published']}")
        print(f"  URL:    {document['url']}")
        print()
