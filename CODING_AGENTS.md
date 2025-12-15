# Coding Agent Guidelines

This document defines how AI coding tools should work in this repository to keep the codebase clear, modular, and future‑proof.

### 1. General principles

- Prioritize **clarity over cleverness**.
- Favor **small, composable functions/modules**.
- Assume future **interoperability** with other tools and languages.


### 2. Project structure

- Keep files organized by purpose (e.g., `src/`, `tests/`, `docs/`).
- Avoid duplicating logic; factor shared pieces into utilities.
- Do not create new top‑level folders without a clear reason and a short comment in the PR/commit message.


### 3. Code style

- Use consistent naming:
    - Descriptive, lowercase_with_underscores or lowerCamelCase (pick one per language and stick to it).
    - Avoid abbreviations unless they are standard (e.g., `url`, `id`).
- Write **self‑documenting** code:
    - Prefer clear variable names over inline comments explaining bad names.
- Respect language‑idiomatic style (e.g., PEP 8 for Python).


### 4. Documentation and comments

- Every public function/class should have a short docstring:
    - What it does.
    - Inputs and outputs.
    - Any assumptions or side effects.
- Use comments for **why**, not **what**, when the intent might not be obvious.
- Update `README.md` and `docs/` when adding or changing major functionality.


### 5. Modularity and interoperability

- Design modules so they:
    - Have a clear, single responsibility.
    - Communicate via simple, well‑typed inputs/outputs (e.g., JSON‑serializable structures).
- Avoid hard‑coding:
    - Paths, credentials, or environment‑specific values.
    - Instead, use config files or environment variables.
- When adding new functionality, think about:
    - How another tool or language could call this (API boundaries, CLI interfaces).


### 6. Testing and validation

- For non‑trivial logic, create or extend tests under `tests/`:
    - Prefer small, fast unit tests.
    - Include at least one test for edge cases or failure modes.
- Do not introduce breaking changes without:
    - Updating tests.
    - Noting the change in a changelog or commit message.


### 7. Git and cleanliness

- Use meaningful commit messages:
    - `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...` style is preferred.
- Do not commit:
    - Large data files.
    - Secrets, tokens, or local environment configs.
    - Generated artifacts (build outputs, `.pyc`, etc.)—respect `.gitignore`.
- When making automated edits:
    - Group related changes in one commit; avoid touching unrelated files.


### 8. Respect project intent

- This repository’s primary goal is **SPM and SPM Defense**, with emphasis on:
    - Detecting and mitigating manipulation.
    - Transparency and explainability.
- Do not add code whose primary purpose is optimizing persuasion or covert influence.

