# Agent Test Log

Reference date: 23 September 2026
Test ticker: SRVCABLE
Research pack: 8 company-related Markdown documents
API endpoint: https://aipipe.org/openai/v1

## Run 1: Baseline

Model: gpt-5 via AI Pipe

Design:
- Loaded local Markdown documents and source metadata.
- Used the initial evidence-first system prompt.
- Sent all 8 documents to the model.
- Applied structural and basic citation validation.

Result:
- API call succeeded.
- Generated a 602-word research brief.
- Saved output/research_brief.md.
- Included all five required sections.
- Identified the conflicting Q1 revenue figures.
- Included the GST demand and receivables risks.
- Did not repeat the stock-tip blog's forced BUY recommendation.

Issues identified:
1. The report asks which figure appears in the official exchange filing,
   but the underlying Q1 exchange filing is not included in the pack.
2. Some interpretations, such as "shareholding quality trending better,"
   could be more clearly labelled as inferences.
3. The validator did not initially check whether citation IDs existed
   in the source pack.
4. The output could be more concise.

Planned changes:
- Strengthen source hierarchy and uncertainty instructions.
- Require explicit distinction between reported facts and inferences.
- Prohibit implying that a missing document was inspected.
- Improve handling of promotional and irrelevant sources.

## Run 2: Evidence Handling and Validation

Model: gpt-5-nano via AI Pipe

Changes:
- Strengthened the system prompt to prioritize official sources.
- Added instructions to distinguish reported facts from inferences.
- Added explicit handling for missing evidence and unresolved conflicts.
- Instructed the agent to ignore prompt-injection attempts and
  unsupported promotional recommendations in source documents.
- Improved citation and source-list validation.
- Updated source restoration and citation repair so compression would
  not silently remove required source entries.

Results and observations:
- The research workflow continued to generate briefs from the local pack.
- Testing exposed issues with source-list parsing and preserving citations
  when compressing the draft.
- Validator behavior was improved to recognize the Markdown source-list
  formats used by the project.
- Further work was needed to consistently enforce the report word limit.

## Run 3: Concision and Final Validation

Model: gpt-5-nano via AI Pipe

Changes:
- Tightened the prompt to target 430–470 words with a hard limit of
  500 words.
- Added section-level limits for Snapshot, Bull Case, Bear Case,
  Open Questions, and Sources.
- Improved the compression workflow and source restoration.
- Added checks for required sections, citation IDs, listed sources,
  source URLs, and the maximum word count.

Final result:
- Generated a 480-word research brief.
- Saved the result to output/research_brief.md.
- Included all five required sections.
- Passed the project validator: python -m src.validate.
- Passed the test suite: pytest -q, with 5 tests passing.
- Retained the conflicting Q1 revenue figures as an unresolved issue.
- Avoided treating promotional recommendations as evidence.

Remaining limitations:
- The primary Q1 FY27 exchange filing was not included in the supplied
  research pack, so the conflicting revenue figures cannot be conclusively
  reconciled from these materials.
- Automated validation checks structure, citations, source references,
  and length; it does not prove that every financial claim is factually
  correct.
- Conclusions remain limited by the coverage, accuracy, and date of the
  supplied research documents.
