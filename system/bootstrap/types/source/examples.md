# Source Type — Examples

Worked examples for storing reusable PDFs, images, videos, and external links.

**Container:** `sources/instance.yaml` (`type: directory`, `content_type: source`). **Items:** catalog entries in `index.md` (`type: source`).

Protocol: read `sources/instance.yaml`, then `users/<principal>/types/source/README.md`

---

## Example 1: Project PDF (tax W-2)

**Situation:** User provides a Minerva W-2 PDF for the `us-taxes` project. Reusable across filing sessions.

**Steps:**

1. Read `sources/instance.yaml` and ask approval (L3–L4) to write to project sources.
2. Create folder if missing: `users/<principal>/projects/us-taxes/sources/files/2025/`
3. Save file: `users/<principal>/projects/us-taxes/sources/files/2025/w2-minerva.pdf`
4. Add entry to `users/<principal>/projects/us-taxes/sources/index.md`:

```markdown
### Minerva W-2 2025

- **id:** source.w2-minerva-2025
- **media_type:** pdf
- **source_type:** internal_file
- **path_or_url:** `files/2025/w2-minerva.pdf`
- **summary:** Minerva University W-2, Sep 25–Dec 31 2025
- **sensitivity:** high
- **tags:** tax, income, 2025
- **added:** 2026-06-09
```

5. Cite in session `output.md`: `users/<principal>/projects/us-taxes/sources/files/2025/w2-minerva.pdf`

---

## Example 2: Personal identity image

**Situation:** Passport scan used across multiple projects (taxes, visa, travel).

**Steps:**

1. Read `sources/instance.yaml` and ask approval to write to personal sources.
2. Save: `users/<principal>/personal/sources/files/identity/passport.jpg`
3. Catalog in `users/<principal>/personal/sources/index.md`:

```markdown
### Passport — bio page

- **id:** source.passport
- **media_type:** image
- **source_type:** internal_file
- **path_or_url:** `files/identity/passport.jpg`
- **summary:** Passport bio page, EB9443361, expires Dec 27 2027
- **sensitivity:** high
- **tags:** identity, passport
- **added:** 2026-06-09
```

---

## Example 3: Video recording

**Situation:** Screen recording of a Paycom download workaround for the `us-taxes` project.

**Steps:**

1. Save: `users/<principal>/projects/us-taxes/sources/files/guides/paycom-w4-download.mp4`
2. Catalog:

```markdown
### Paycom W-4 download workaround

- **id:** source.paycom-w4-workaround
- **media_type:** video
- **source_type:** internal_file
- **path_or_url:** `files/guides/paycom-w4-download.mp4`
- **summary:** Screen recording of print-to-PDF workaround for W-4 download
- **sensitivity:** medium
- **tags:** paycom, how-to
- **added:** 2026-06-09
```

---

## Example 4: External URL only (no local file)

**Situation:** IRS page referenced repeatedly; no need to save a local copy.

**Steps:**

1. Add to `users/<principal>/projects/us-taxes/sources/index.md` only — no `files/` entry:

```markdown
### IRS — Substantial Presence Test

- **id:** source.irs-spt
- **media_type:** other
- **source_type:** external_url
- **path_or_url:** `https://www.irs.gov/individuals/international-taxpayers/substantial-presence-test`
- **summary:** Official IRS SPT guidance
- **sensitivity:** low
- **tags:** irs, residency
- **added:** 2026-06-09
```

---

## Example 5: Promote from session to sources

**Situation:** User uploaded a PDF to the session folder during work; now wants it reusable.

**Before:** `users/<principal>/projects/us-taxes/sessions/2026-06-09-002/i94-printout.pdf` (session-only)

**After approval:**

1. Move (or copy) to `users/<principal>/projects/us-taxes/sources/files/identity/i94-2024.pdf`
2. Add catalog entry to `sources/index.md`
3. Note promotion in session `trace.md` and propose in `patch.md` if not applied directly

**Do not** leave reusable binaries only in the session folder.

---

## Quick reference

| media_type | Extensions | Example path |
|------------|------------|--------------|
| pdf | `.pdf` | `files/2025/w2-minerva.pdf` |
| image | `.jpg`, `.png`, `.webp`, `.heic` | `files/identity/passport.jpg` |
| video | `.mp4`, `.mov`, `.webm` | `files/guides/demo.mp4` |
| audio | `.mp3`, `.m4a`, `.wav` | `files/notes/call-recording.m4a` |
| markdown | `.md` | `files/refs/filing-checklist.md` |
| other | any | note format in summary |
