# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

This repository currently contains only planning material — no source code has been written yet:
- `.llm/prd.md` — product requirements (in Portuguese)
- `picture/tela_de_captura.png` — reference screenshot for the UI design

There is no build, lint, or test tooling set up yet. When implementation begins, this file should be updated with the actual commands (e.g., `streamlit run ...`, `pytest`, etc.) and architecture notes.

## Project requirements (from .llm/prd.md)

This is an educational Python project: a "bolão" (prediction pool) for the 2026 World Cup.

- **Stack**: Python, using **Streamlit** for the UI.
- **Persistence**: Participant picks must be saved to a database.
- **UI design**: Base the layout on `picture/tela_de_captura.png` (a World Cup group-stage simulator screen showing groups, standings, and a knockout bracket).
- **Registration**: When a person joins the pool, collect their **name, phone number, and email**.
- **Predictions scope**: Users only pick the **1st and 2nd place team in each group**. The 8 best third-placed teams that advance are chosen **randomly** to keep the logic simple — this is intentional simplification, not a bug.
- Keep the architecture simple, consistent with the educational nature of the project.
