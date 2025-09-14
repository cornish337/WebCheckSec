# Web App Security Checklist — Project README

## Overview & Goals

This project delivers a **self-contained interactive checklist** you can open in any modern browser (no hosting required) to plan and track **web application security testing** across OWASP WSTG, ASVS, PTES, NIST SP 800-115, OSSTMM, and ISSAF.
Each card = a **Category** → contains **Sub-categories** → contains **Items** with **checkboxes**, optional **sub-tasks** (their own checkboxes), **ASVS mapping**, and rich **Details** fields (How to Test, Tools, References, Applicability, Sources). The UI persists to the browser’s localStorage, and supports **CSV/JSON import & export**.

The current main page is:

**`webapp_security_checklist_category_subtasks_v8_1_importable.html`**

* Shows progress counters and runs entirely locally (“Local-only • saves in your browser”).&#x20;
* Toolbar includes **Search**, **Open/Done filter**, **Save (local)**, **Export JSON**, **Export CSV**, and **Reset (from file)**, plus **Import Prefill (CSV/JSON)**.&#x20;
* Every item has a checkbox; sub-tasks (if present) also have checkboxes; an expandable **Details** section holds ASVS / Description / Tools / Links / Applicability / Sources.  &#x20;
* You can **Save**, **Export JSON/CSV**, or **Reset** to the embedded snapshot.&#x20;
* **Import Prefill (CSV/JSON)** reads your file and merges/creates content.&#x20;

> ✅ The end goal is to **cover every row from the original spreadsheet** by importing a structured CSV/JSON, then using the app to drill down category → subcategory → item, fill the details, **and tick off each test**.

---

## How the page is structured (technical)

* **Data model in the UI:** `Category → Sub Category → Items → Subtasks`. Each item stores:

  * `done`, `title`, `tags[]`, `subtasks[]`, plus `asvs`, `desc`, `tools`, `links`, `applic`, `sources` (editable in the **Details** pane).&#x20;
* **Persistence:** Data is kept under a storage key in localStorage; **Save (local)** writes; **Reset (from file)** reloads the embedded seed. &#x20;
* **Export:** One-click JSON and CSV exporters.&#x20;
* **Import:** CSV and JSON readers accept user files and merge/replace as appropriate. Errors are surfaced in-page.&#x20;
* **Progress & counts:** The header shows overall and per-category completion.&#x20;

---

## Using the app

1. Open `webapp_security_checklist_category_subtasks_v8_1_importable.html` in your browser.
2. Click **Reset (from file)** to load the embedded seed (if any), then **Save (local)** to persist.&#x20;
3. **Import Prefill (CSV/JSON)** to load your real dataset. &#x20;
4. Use **Search** and **Open/Done** filter to navigate.&#x20;
5. Expand **Details** on any item to edit **ASVS**, **Description**, **Tools**, **Links**, **Applicability / N/A**, **Sources**. Changes are saved automatically.&#x20;
6. Tick item/sub-task checkboxes to track progress. &#x20;
7. **Export JSON/CSV** anytime to share or archive.&#x20;

---

## Import formats (CSV & JSON)

### CSV (recommended for spreadsheet workflows)

**Required header row (order can vary):**

```
Category, Sub Category, Item, Done, Subtask, Subtask Done, ASVS, Description, Tools, Links, Applicability, Sources, Tags
```

* This is the exact header set the exporter writes and the importer understands.&#x20;
* **Rows without a Subtask** describe the main item; **rows with Subtask** add/merge sub-tasks under that item (each sub-task line carries its own `Subtask Done`). The exporter emits exactly this shape.&#x20;
* `Done` / `Subtask Done` accept TRUE/FALSE (case-insensitive).
* `ASVS`, `Description`, `Tools`, `Links`, `Applicability`, `Sources`, `Tags` populate the item’s **Details** fields (tags are space/comma split).

### JSON

Two accepted forms:

1. **Flat array of row objects** (same keys as CSV). Imported rows are merged/created under the right category/sub-category/item and sub-tasks added as needed. (Handled by the same import pipeline that parses CSV rows.)&#x20;

2. **Full dataset** (array of categories with nested `subcats/items`) — when present, this can replace the in-memory dataset (the import code expects an array and merges; the UI then saves and renders).&#x20;

> Tip: If an import appears to do nothing, ensure the file is valid CSV/JSON and includes a header row (for CSV). The importer reads the file’s extension to decide CSV vs JSON.&#x20;

---

## Content expectations (what to fill per item)

In **Details**, keep the content aligned to your methodology mix and expanded tooling:

* **ASVS**: Add `Vx.y.z` codes and links.
* **Description**: Plain-language summary of the risk/test.
* **Tools**: Include Burp **and** complementary tools (ZAP, ffuf, Arjun, sqlmap, httpx, nuclei, interactsh, etc.).
* **Links**: OWASP WSTG/ASVS, PTES, NIST SP 800-115, OSSTMM, ISSAF, and tool docs.
* **Applicability / N/A**: Quick rules of thumb for when to mark N/A.
* **Sources**: Papers, blog posts, cheat sheets.

(Example category-level and item-level prefill content you supplied—**Authentication** and **File Handling**—already follows this structure and can be imported as JSON/CSV; see your `auth_file_handling.json` sample for reference.) &#x20;

---

## Current status

* ✅ **Category/Sub-category/Item UI with checkboxes and sub-tasks** (including per-sub-task checkboxes).&#x20;
* ✅ **Editable details** (ASVS, Description, Tools, Links, Applicability, Sources) saved locally.&#x20;
* ✅ **Search & filter**, **local persistence**, **Export JSON/CSV**, **Import Prefill (CSV/JSON)**.  &#x20;
* ✅ **CSV schema** and exporter implemented.&#x20;
* ✅ **JSON sample (Auth/File Handling) works as a content template** for category prefill. &#x20;

---

## What remains / Next steps

1. **Populate all categories/items** from the original spreadsheet into a master CSV, using the header set above.

   * Start by exporting the current page to CSV, then extend it with more rows; re-import to iterate.&#x20;
2. **ASVS mapping at category level** (optional UI: surface an “ASVS (category)” textarea at the top of each card).
3. **Related items / links by tag** inside Details (show “Related” section by matching tags; tags already exist).&#x20;
4. **Lightweight validation** during import (e.g., warn on unknown headers, normalize TRUE/FALSE).
5. **Template packs** for common combo-tests (e.g., “Discovery → Param harvest → Injection → OAST”) that you can attach to items as prebuilt sub-tasks.
6. **Optional team workflows**: allow loading a shared JSON from disk each session (no server), or add an “Export to Markdown” per item for report writing.

---

## FAQ

* **Do I need a server?** No. It’s a single HTML file designed for local/offline use.&#x20;
* **Where does my data live?** In your browser’s localStorage under a scoped key; you can Export JSON/CSV at any time. &#x20;
* **How do I ensure coverage of the original spreadsheet?** Import a CSV using the schema above; each row becomes a trackable item (and sub-task if provided). You can then tick off items and maintain evidence/links directly in the card.

---

If you want, I can also generate a **starter CSV** scaffold with all your categories/sub-categories from the master sheet (empty fields for Description/Tools/etc.) so your team can fill it in, then import to the page for immediate use.
