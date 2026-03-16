---
description: Translate technical Markdown documents from English to Vietnamese (Expert Style)
---

## Objective

Translate technical Markdown files ensuring high professional standards and natural flow (Localization), while strictly preserving the logical structure and source code.

## STRICT CONSTRAINTS

### 1. Terminology & Headers

- **Mixed Headers:** For headers (H1, H2, H3), use the format `English Title: Vietnamese Translation` or keep the English version if it's an architecture/pattern name (e.g., `## Phase 1: The Baseline - Một Agent 'Generalist' Monolithic`).
- **Terminology Preservation:** KEEP core technical terms in English (e.g., API, Backend, LLM, Agent, ReAct, Node, Graph, Sub-task, Workflow, Persona, Metadata). Do not attempt to transliterate or translate these if it reduces professional accuracy.

### 2. Naturalness & Flow

- **Persona:** Act as an **AI Specialist/Software Engineer** explaining documentation to a colleague.
- **Localization:** Do not translate word-for-word. Use appropriate Vietnamese technical terminology (e.g., "division of labor" -> "phân công lao động", "high-level workflow" -> "quy trình cấp cao"). Avoid passive voice structures or awkward machine-translation-style phrasing.

### 3. Integrity of Structure & Code

- **1:1 Structure:** Do not merge sections or change the order of paragraphs. One block of content in the source must correspond to exactly one block in the output.
- **Original Code Logic:** Absolutely no changes to code logic, variable names, or the structure of code blocks.
- **Translate Comments in Code:** Translating comments inside code blocks into Vietnamese is encouraged to help learners follow along, but executable code must remain untouched.
- **100% Completeness:** Do not truncate, summarize, or omit any bullet points or sentences.

## Output

Save translated files with the suffix **\_vi.md** (e.g., `architecture.md` -> `architecture_vi.md`).
