# Anki-Connect (yukikase0422 fork)

This repository has permanently moved to https://git.sr.ht/~foosoft/anki-connect.

---

## About this fork

This is a fork of [FooSoft/anki-connect](https://github.com/FooSoft/anki-connect)
maintained by [yukikase0422](https://github.com/yukikase0422) for personal use.
It adds a small set of actions that the upstream project does not (yet) expose,
while keeping full backwards compatibility with the upstream API.

The license is unchanged — the original GPLv3 (see `LICENSE`) — and modified
sources are made available through this public repository as required by GPLv3.

## Added actions

### `getDeckDescription`

Return the description (`desc` field) of the given deck.

- Parameters
  - `deck` *(str, required)*: name of the deck.
- Returns: the deck's description as a string (may be empty).
- Errors: raises if the deck does not exist.

Request example:

```json
{
  "action": "getDeckDescription",
  "version": 6,
  "params": { "deck": "Japanese::N3" }
}
```

Response example:

```json
{ "result": "Vocabulary for JLPT N3 (auto-managed)", "error": null }
```

### `setDeckDescription`

Overwrite the description (`desc` field) of the given deck.

- Parameters
  - `deck` *(str, required)*: name of the deck.
  - `description` *(str, required)*: new description string. May be empty.
- Returns: `true` once the description has been persisted.
- Errors: raises if the deck does not exist, or if `description` is not a string.

Request example:

```json
{
  "action": "setDeckDescription",
  "version": 6,
  "params": {
    "deck": "Japanese::N3",
    "description": "Vocabulary for JLPT N3 (auto-managed)\nSource: https://example.com/..."
  }
}
```

Response example:

```json
{ "result": true, "error": null }
```

Notes:

- `description` is written verbatim. Newlines (`\n`) are preserved, and Anki
  renders the description on the deck overview page (so basic HTML works on
  newer Anki versions, just as in the GUI deck-options screen).
- The action goes through `startEditing()` / `stopEditing()` so Anki's
  reviewer/browser state is kept consistent.

## Installing this fork into a locally-installed AnkiConnect add-on

The official AnkiConnect add-on lives in Anki's add-on folder. On Windows, for
add-on id `2055492159` (the canonical AnkiConnect id), that is:

```
%APPDATA%\Anki2\addons21\2055492159\
```

To replace the installed add-on with this fork **manually**:

1. **Close Anki completely.** Anki holds the collection file open; copying
   `plugin/*.py` while Anki is running can corrupt the add-on cache.
2. (Recommended) Make a backup of the existing add-on folder, e.g. copy
   `2055492159\` to `2055492159.bak\`.
3. Copy every file inside `plugin/` of this repository **into**
   `%APPDATA%\Anki2\addons21\2055492159\`, overwriting:
   - `__init__.py`
   - `config.json`
   - `config.md`
   - `edit.py`
   - `util.py`
   - `web.py`
4. **Do not** delete `meta.json` in the destination folder — Anki regenerates
   it but your existing user-level config (e.g. `webBindPort`) lives there.
5. Start Anki. Open *Tools → Add-ons*; AnkiConnect should still be listed and
   load without errors. The new actions are now available over HTTP at
   `http://127.0.0.1:8765`.

To revert, either restore the backup from step 2, or reinstall the official
AnkiConnect from Anki's add-on dialog using add-on code `2055492159`.

### Quick smoke test

With Anki running, from a shell:

```bash
curl -X POST http://127.0.0.1:8765 \
  -H "Content-Type: application/json" \
  -d '{"action":"setDeckDescription","version":6,
        "params":{"deck":"Default","description":"hello from fork"}}'

curl -X POST http://127.0.0.1:8765 \
  -H "Content-Type: application/json" \
  -d '{"action":"getDeckDescription","version":6,
        "params":{"deck":"Default"}}'
```

The first call should return `{"result": true, "error": null}` and the second
should return `{"result": "hello from fork", "error": null}`.

## Running the test suite

The upstream tests in `tests/` require a Linux environment with `xvfb`, PyQt
and a matching `anki`/`aqt` pair. See `tox.ini` for details. On Windows the
recommended fast feedback loop is the smoke test above (or to run individual
methods through the live add-on).
