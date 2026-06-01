# Galgame Translation Roadmap

## Goal

Add offline galgame script extraction, translation, and patched export to the existing document workflow. This should stay aligned with ContextWeave's import -> glossary/context -> translate -> export model rather than becoming a live process-hooking or overlay translator.

## Non-Goals

- Do not build live text hooks, process injection, or memory patching as the first implementation.
- Do not vendor LunaTranslator or AiNiee code.
- Do not start with archive unpack/repack formats such as `.xp3`, `.rpa`, `.rpyc`, encrypted `.dat`, Unity bundles, or RPG Maker VX/Ace binary data.
- Do not require users to translate only Ren'Py projects.

## Architecture Direction

Galgame support should be a new document type backed by pluggable adapters:

- `GalgameDocument`: stores original script/intermediate files as text sources and exports patched copies.
- `GalgameAdapter`: detects a script/intermediate format, extracts translation units, and applies translated text back to the original file.
- `TranslationUnit`: one translatable dialogue/menu/narration unit with stable identity, source path, original text, optional speaker/context, and adapter metadata.
- `GalgameDocumentHandler`: creates one translation chunk per unit and returns one translated entry per unit, avoiding line-splitting and duplicate-line deduplication bugs.

## Implementation Status

- Phase 1: Complete.
- Phase 2: Complete for MTool JSON, Translator++ `.trans`, VNText JSON, ParaTranz JSON, TPP / Translator++ `.xlsx`, and Wolf RPG extracted `.xlsx`.
- Phase 3: Complete for directly editable Ren'Py `.rpy` scripts and TyranoScript / KAG / KiriKiri extracted `.ks` scripts.
- Phase 4: Complete for RPG Maker MV/MZ extracted `data/*.json` event text, speaker names, choices, and scroll-text commands.
- Phase 5: Complete for adapter-level import summaries, manual adapter selection hooks, bilingual review export, and shared placeholder/control-code export validation.
- Phase 6: Complete for offline bridge-format discovery, explicit dry-run archive helper commands, and glossary seed inspection from speakers, character definitions, and project metadata.

## Phase 1: Foundation

- Add `galgame` as a document type with no OCR requirement.
- Store source files with original relative paths and original text content.
- Add adapter/unit abstractions and a registry for adapters.
- Serialize extracted units from `get_text()` for workflow bootstrap.
- Add a unit-preserving handler that creates one chunk per unit using identity-scoped hashes.
- Support preserve-structure export by reparsing originals and replacing only adapter-owned text slots.
- Add focused tests for import, extraction, chunking identity, and patched export.

## Phase 2: Broad Intermediate Formats

Prioritize formats produced by common extraction tools because they cover many engines without archive/repacker work:

- MTool JSON key/value dictionaries.
- Translator++ `.trans` project files.
- VNText JSON.
- TPP / Translator++ spreadsheet formats.
- ParaTranz JSON.
- Wolf RPG extracted spreadsheets if practical.

## Phase 3: Native Script Files

Add native text-script adapters where patching can remain safe and local:

- Ren'Py `.rpy` translation/source scripts.
- TyranoScript / KAG `.ks` files.
- KiriKiri extracted `.ks` files.

The parser must preserve commands, labels, interpolation placeholders, style tags, escapes, quotes, and speaker identifiers.

## Phase 4: RPG Maker MV/MZ

Support direct extracted project folders after the foundation is stable:

- Detect `www/data/*.json` and `data/*.json`.
- Extract safe event command text such as dialogue, continuation lines, choices, and names.
- Preserve JSON address paths and event command codes.
- Blacklist risky fields and unrelated JSON data.
- Export patched `data/` files while preserving original layout.

## Phase 5: UX And Safety

- Auto-detection confidence and manual adapter override.
- Import summary showing adapter, file count, and unit count.
- Export validation for missing translations, placeholder drift, quotes, and dangerous syntax.
- Bilingual/debug export for review.
- Placeholder/control-code protection shared across adapters.

## Phase 6: Advanced Integrations

- Optional bridge modes to external extraction tools, not live game hooks.
- Archive helper wrappers only when external tools are available and explicit.
- Later support for `.rpa`, `.rpyc`, `.xp3`, Unity assets, and RPG Maker VX/Ace if safe tooling exists.
- Glossary seeding from speaker names, character definitions, and project metadata.

## MVP Definition

The first user-valuable MVP should import common extracted/intermediate project files, translate each unit with stable unit identity, preserve placeholders/control codes, and export the same project/file structure through the existing UI.
