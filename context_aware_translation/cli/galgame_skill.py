GALGAME_CODEX_SKILL_TEXT = """---
name: contextweave-galgame-translation
description: Use ContextWeave CLI to translate extracted galgame scripts and intermediate files while preserving patchable structure.
---

# ContextWeave Galgame Translation

Use this skill when the user wants to translate a visual novel / galgame with ContextWeave from extracted scripts or tool exports.

## Ground Rules

- Work on a copy of the game or extracted files, never the original install folder.
- Do not import `.exe`, `.dll`, save data, images, audio, video, or opaque archives directly.
- Prefer stable intermediate formats over raw text dumps.
- Preserve placeholders/control codes exactly, including Ren'Py `{...}`, RPG Maker `\\N[1]`, and KAG/Tyrano `[l]` tags.
- If a game is packed, use external extractors only when the user explicitly asks and the tool is installed.
- ContextWeave translates supported extracted files; external tools are still responsible for unpacking/repacking proprietary archives.

## Supported Direct Inputs

- Ren'Py `.rpy`
- TyranoScript / KAG / extracted KiriKiri `.ks`
- RPG Maker MV/MZ `data/*.json` or `www/data/*.json`
- MTool JSON dictionaries
- Translator++ `.trans`
- VNText JSON
- ParaTranz JSON
- TPP / Translator++ `.xlsx`
- Wolf RPG extracted `.xlsx`

## Preferred Unsupported-Engine Bridge

When a game engine or extractor output is not directly supported by ContextWeave, ask the extractor/converter agent to normalize the extracted script text into ParaTranz-style JSON:

```json
[
  {
    "key": "script001:000001",
    "original": "こんにちは",
    "translation": "",
    "speaker": "Alice",
    "context": "script001 line 1"
  }
]
```

Rules for the converter:

- Output UTF-8 JSON.
- Use one object per translatable game entry.
- Keep `translation` empty before ContextWeave translation.
- Make `key` stable and unique from source file plus entry index.
- Preserve control codes/placeholders exactly in `original`.
- Do not merge entries.
- Generate a separate injector that writes translated JSON back to the original extracted script format by `key` or original order.

## CLI Workflow

1. Validate config:

```bash
contextweave-cli --config ./contextweave.yaml config validate
```

2. Inspect source support:

```bash
contextweave-cli --json galgame inspect ./extracted_or_exported_source
```

3. If the source is unsupported, inspect possible external helper hints:

```bash
contextweave-cli --json galgame helpers ./game_copy
```

4. Translate and preserve structure:

```bash
contextweave-cli \
  --config ./contextweave.yaml \
  --library-root ./contextweave-library \
  --json \
  run ./extracted_or_exported_source \
  --type galgame \
  --output ./translated_patch \
  --preserve-structure
```

5. Use the corresponding injector/repacker to apply `./translated_patch` back to the copied game or extracted script tree.

## Useful Inspection Commands

```bash
contextweave-cli galgame inspect ./source
contextweave-cli galgame glossary-seeds ./source
contextweave-cli galgame helpers ./source
```

## Failure Handling

- If import is ambiguous, rerun `run` with `--type galgame`.
- If placeholder validation fails, repair the translated entry so all source control codes are present exactly once.
- If an extracted dump is raw plain text, convert it to ParaTranz JSON before using ContextWeave.
- If only opaque binary chunks remain after extraction, stop and ask for a game-specific adapter/extractor instead of guessing.
"""
