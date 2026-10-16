
from src.validate import validate_brief


VALID_BRIEF = """\
## Snapshot
Revenue increased [S1].
## Bull case
Order book grew [S2].
## Bear case
Margins declined [S1].
## Open questions
Revenue figures conflict [S1] [S2].
## Sources
- S1: Filing https://example.com/filing
- S2: Transcript https://example.com/transcript
"""


def test_valid_brief_passes():
    assert validate_brief(VALID_BRIEF, {"S1", "S2"}) == []


def test_unknown_citation_is_detected():
    brief = VALID_BRIEF.replace(
        "Revenue increased [S1]",
        "Revenue increased [S99]",
    )
    errors = validate_brief(brief, {"S1", "S2"})
    assert any("Unknown citation IDs: S99" in e for e in errors)


def test_missing_source_entry_is_detected():
    brief = VALID_BRIEF.replace(
        "- S2: Transcript https://example.com/transcript\n",
        "",
    )
    errors = validate_brief(brief, {"S1", "S2"})
    assert any(
        "missing from Sources section: S2" in e for e in errors
    )


def test_missing_section_is_detected():
    brief = VALID_BRIEF.replace("## Bull case\nOrder book grew [S2].\n", "")
    errors = validate_brief(brief, {"S1", "S2"})
    assert any("Missing required section: Bull case" in e for e in errors)

def test_headings_with_descriptive_suffixes_are_recognized():
    brief = VALID_BRIEF.replace(
        "## Snapshot",
        "## SRVCABLE – Snapshot (as of 23 September 2026)",
    ).replace(
        "## Bull case",
        "## Bull case (evidence-based positives)",
    )
    assert validate_brief(brief, {"S1", "S2"}) == []
