
"""Structural, citation, and source-list validation for research briefs."""

import re

REQUIRED_SECTIONS = [
    "Snapshot",
    "Bull case",
    "Bear case",
    "Open questions",
    "Sources",
]

DEFAULT_MAX_WORDS = 500


def validate_brief(
    text: str,
    valid_source_ids: set[str] | None = None,
    max_words: int = DEFAULT_MAX_WORDS,
) -> list[str]:
    """Return validation errors; an empty list means the brief passed."""
    if not text or not text.strip():
        return ["Brief is empty."]

    errors = []

    # Extract Markdown headings, including headings with descriptive suffixes.
    headings = re.findall(r"(?m)^#{1,3}\s+([^\n]+?)\s*$", text)

    normalized_headings = [
        re.sub(r"^\d+[\.\)]\s*", "", heading).strip().lower()
        for heading in headings
    ]

    for section in REQUIRED_SECTIONS:
        pattern = rf"\b{re.escape(section.lower())}\b"
        if not any(
            re.search(pattern, heading)
            for heading in normalized_headings
        ):
            errors.append(f"Missing required section: {section}")

    # IMPORTANT: [^\n]* matches only the heading line.
    # Using .* with DOTALL here would consume the entire document.
    sources_match = re.search(
        r"(?ims)^#{1,3}\s+Sources\b[^\n]*\n"
        r"(.*?)(?=^#{1,3}\s+|\Z)",
        text,
    )

    if sources_match:
        sources_text = sources_match.group(1)
        body_text = text[:sources_match.start()]
    else:
        sources_text = ""
        body_text = text

    # Accept ordinary URLs and URLs inside Markdown links.
    if sources_match and not re.search(
        r"https?://[^\s)>\]]+",
        sources_text,
    ):
        errors.append("Sources section contains no URL.")

    # Find source citations in the brief, excluding the Sources section.
    cited_numbers = set(
        re.findall(r"\[S(\d+)\]", body_text)
    )

    if not cited_numbers:
        errors.append("No source citations like [S1] were found.")

    # Accept both:
    # - [S1] Source title, https://example.com
    # - S1: Source title, https://example.com
    listed_numbers = set()

    for match in re.finditer(
        r"(?m)^\s*[-*]\s*(?:\[S(\d+)\]|S(\d+)\s*:)",
        sources_text,
    ):
        number = match.group(1) or match.group(2)
        listed_numbers.add(number)

    missing_entries = cited_numbers - listed_numbers

    if missing_entries:
        formatted = ", ".join(
            f"S{number}"
            for number in sorted(missing_entries, key=int)
        )
        errors.append(
            f"Cited sources missing from Sources section: {formatted}"
        )

    # Check that every citation refers to a supplied document.
    if valid_source_ids is not None:
        valid_numbers = {
            source_id.removeprefix("S")
            for source_id in valid_source_ids
        }

        unknown_numbers = cited_numbers - valid_numbers

        if unknown_numbers:
            formatted = ", ".join(
                f"S{number}"
                for number in sorted(unknown_numbers, key=int)
            )
            errors.append(f"Unknown citation IDs: {formatted}")

    word_count = len(text.split())

    if word_count > max_words:
        errors.append(
            f"Brief is too long: {word_count} words "
            f"(maximum {max_words})."
        )

    return errors


if __name__ == "__main__":
    sample = """\
## Snapshot
Revenue increased [S1].

## Bull case
Order book grew [S2].

## Bear case
Margins declined [S1].

## Open questions
Revenue figures conflict [S1] [S2].

## Sources
- [S1] Example filing, https://example.com/filing
- S2: Example transcript, https://example.com/transcript
"""

    issues = validate_brief(
        sample,
        valid_source_ids={"S1", "S2"},
    )

    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Validation passed.")
