# ScentGather — repo context

> **⚠ Repo not public-ready as of 2026-05-16.** This subproject
> contains real-run test data with personal file paths:
> `scentgather.db` (145 MB SQLite from a 2022 run), `logfile.log.*`
> (over 2 GB total of timestamped logs), `whatisthis` (kept
> untracked — keep that way), `فثسفيهق/` (Arabic-named dir of
> unclear contents). Scrub or gitignore these before any push.

## What this is

ScentGather is the v1 **metadata crawler** for DataMasterer. It walks
a user-specified directory tree, computes file hashes (MD5), and
extracts metadata using the heavy `file_metadata` Python 2 library
(which itself pulls in pillow / numpy / dlib / scikit-image / wand /
zbar / pycolorname / ffprobe — image, video, audio, archive, face,
QR-code, colour-extraction). Stores everything in SQLite (or
optionally MySQL / MariaDB / Oracle / SQL Server / JSON / XML — never
actually exercised beyond SQLite).

Bee theme: bees forage for **scent** to find flowers. ScentGather is
the foraging step — finding and tagging the raw material.

## Status

- **Last functional update: 2022-06** (commit `aaa8dadb`: "Add
  logging and attempt speeding up using the checksum").
- **2026-05-16 housekeeping** (`cd8a2ba`): moved modules into a proper
  src-layout (`src/ScentGather/`), added a missing `setup.py` +
  `requirements.txt` scaffold. No functional changes.
- **Python 2** throughout (`#!/usr/bin/python` shebangs, `print`
  statements, `u''` literal markers in dict keys). Will need full
  port to Python 3 for v2.
- **Heavy native deps**: `dlib` (face detection), `wand` (ImageMagick
  binding), `zbar` (QR / barcodes) — all C extensions that may not
  build on modern systems without effort.
- **One published-to-PyPI ancestor**: the README references the
  external `file_metadata` package; that lib was abandoned and is
  the main blocker for re-running ScentGather as-is on a modern box.

## Layout

```
src/ScentGather/
  __main__.py                  CLI entry-point (argparse, db connect, walk loop)
  scentgather_connecttodb.py   SQLite/MySQL/etc. connection + schema DDL
  scentgather_getfilemeta.py   md5 hashing + file_metadata wrapper + dir walker
  scentgather_logging.py       Log rotation + ScentTimer (ETA / progress)
setup.py                       distutils, packages=['ScentGather']
requirements.txt               wheel, distro, python-magic, six, appdirs,
                               pillow, numpy, dlib, scikit-image, wand, zbar,
                               pycolorname, ffprobe, file_metadata
README.md                      original motivation + usage example
scentgather.db                 145 MB, real prior-run data (test fixture — DO NOT PUSH)
logfile.log + logfile.log.*    ~2 GB of timestamped run logs (DO NOT PUSH)
whatisthis                     7 MB EXIF debug dump (currently untracked — KEEP UNTRACKED)
build/, *.egg-info/, *.pyc, __pycache__/  build artifacts (should be gitignored)
```

## CLI surface (v1)

```
python -m ScentGather [-h] [-d DEPTH] [-l MEMORY_LIMIT]
                     [-H HOST] [-s SCHEMA] [-u USER] [-p PASS]
                     [-t {mysql,sqlite,json,xml,oracle,sqlserver,mariadb}]
                     [--verbose] [--quick]
                     pathname
```

- `-d 0` infinite depth, otherwise stop at N.
- `-l 100` in-memory batch limit (writes to db every N files).
- `-t sqlite` default; schema name → `<schema>.db` filename.
- `--quick` skips files by pathname only (faster, less accurate —
  misses moved files).

## SQLite schema (relevant tables)

| Table | What |
|---|---|
| `platforms` | one row per host that ever scanned (architecture, machine, node, platform, processor, system) |
| `files` | one row per (path × system). Tracks filename, pathname, inode, size, timestamps (lastmod, lastaccess, apparentcreation, discovereddeletion), insertion-date default-CURRENT. |
| `exif` | EXIF key dictionary (id, name) — referenced from a join table tying file → exif key → value |

The schema is normalised more than v2 needs to be — the v1 design
treated EXIF keys as a controlled vocabulary, which became a
maintenance pain. v2 should store EXIF as a JSON blob with the
critical fields (date, GPS, camera, dimensions) promoted to columns.

## How this maps to v2

This subproject is the **v1 ancestor of `scentgather` in
DataMasterer v2** (per the bee-themed package layout). The v2 port:

- Python 3 + asyncio (v1 is Python 2 + synchronous).
- Replace heavy `file_metadata` dep with focused libs from doc 13:
  pikepdf, pypdf, ebooklib, mutagen, Pillow, python-magic,
  ffmpeg-python.
- Use SHA-256 + the "head + tail + size" cheap-fingerprint (proved
  92.5 % match rate in the disk-toolkit field study; see
  `docs/design/inspiration/disk-toolkit-cleanup-2026-05/LESSONS.md`).
- Incremental scan (only re-index changed files) — v1 is full-rescan
  every run.
- The cascading-classifier pattern from the disk-toolkit's
  `bookclassify` (path → filename → content-sniff → first/last-page
  text) belongs in v2 `scentgather.classify.*`.

## How v2's migration tool (doc 14) uses this

The 145 MB `scentgather.db` is the canonical migration test fixture.
v2's `dm migrate scentgather --from-db <path>` reads the v1 schema
and emits inserts into the new v2 schema. Doc 14 (MIGRATION-V1.md)
documents the field-by-field mapping.

## Hygiene applied 2026-05-16

- `core.fileMode = false` (exFAT mode-flip mitigation; local config).
- `requirements.txt` + `setup.py` added (had been missing despite
  the README referencing them).
- src-layout enforced (`src/ScentGather/`).

## Hygiene still needed (before any push)

- Add `.gitignore` entries for `*.pyc`, `__pycache__/`, `build/`,
  `*.egg-info/`, `*.db`, `logfile.log*`, `whatisthis`, `فثسفيهق/`.
- `git rm --cached` the currently-tracked `.pyc` files.
- Decide whether to keep `scentgather.db` and the logs as
  out-of-tree test fixtures, or delete them entirely.
