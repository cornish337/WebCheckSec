# WebCheckSec – Web Application Security Checklist

A **single-file, client-side checklist tool** for web application security testing.  
No build, no server, no install – just open the HTML file in Chrome desktop and work locally.  
All changes are saved to your browser’s localStorage, with CSV/JSON import/export for sharing.

---

## ✨ Features

- **Category → Subcategory → Item** hierarchy
- **Collapsible UI** for categories and subcategories
- **Check/Uncheck items and subtasks** with live completion counts
- **Priority levels (0–3)**  
  - High (3) = red highlight  
  - Medium (2) = amber  
  - Low (1) = green, slightly faded  
  - Very Low (0) = gray, most faded
- **Hide by Default**  
  - Items or subtasks can be marked hidden  
  - Hidden entries are suppressed unless “Show hidden” is enabled
- **Subcategory Notes** – add free-text notes at the subcategory level
- **Filtering**  
  - Search across Category, Subcategory, Item, Description, Tools, Links, Tags  
  - Filter by Done/Open/All  
  - Multi-select Priority filter  
  - Clickable tag pills to filter by tag
- **Import / Export**  
  - CSV or JSON  
  - Round-trip safe with extended schema  
  - Export always includes priority, hidden, and notes
- **Local persistence** – automatically saves in your browser

---

## 🚀 Getting Started

1. Clone or download this repo.
2. Open `webapp_security_checklist.html` in **desktop Chrome**.
3. Start checking items, editing details, setting priorities, or hiding items.
4. Use **Export JSON/CSV** to save your progress externally.
5. Use **Import Prefill** to load checklist data from CSV or JSON.

> ⚠️ Data is stored in `localStorage`. Clearing site data in your browser will erase it.  
> Always export before resetting or switching machines.

---

## 📑 Data Model

The checklist supports two equivalent formats:

### Nested JSON (preferred)

```json
[
  {
    "category": "Authentication",
    "subcats": [
      {
        "name": "Password Policy",
        "notes": "Review against corporate baseline.",
        "items": [
          {
            "title": "Passwords must be at least 12 chars",
            "done": false,
            "hidden": false,
            "priority": 3,
            "tags": ["auth","policy"],
            "asvs": "2.1.1",
            "desc": "Verify minimum length in registration form.",
            "tools": "Manual; Burp Repeater",
            "links": "https://owasp.org/ASVS",
            "applic": "",
            "sources": "",
            "subtasks": [
              { "text": "Test registration page", "done": false, "hidden": false }
            ]
          }
        ]
      }
    ]
  }
]
````

### Flat CSV / JSON Rows

Header:

```
Category, Sub Category, Item, Done, Subtask, Subtask Done, Subtask Hidden,
ASVS, Description, Tools, Links, Applicability, Sources, Tags,
Priority, Hidden, Subcategory Notes
```

Example row:

```
Authentication,Password Policy,Passwords must be at least 12 chars,FALSE,,,,
2.1.1,Verify minimum length in registration form.,Manual; Burp Repeater,https://owasp.org/ASVS,,,,auth policy,
3,FALSE,Review against corporate baseline.
```

### Field Definitions

* **Category / Sub Category / Item** – required hierarchy
* **Done / Subtask Done / Hidden / Subtask Hidden** – booleans (`TRUE/FALSE`, `yes/no`, `1/0`)
* **Priority** – integer 0–3

  * `0` = Very Low (faded gray)
  * `1` = Low (faded green)
  * `2` = Medium (amber)
  * `3` = High (red highlight)
* **Notes** – free-text, stored at Subcategory level
* **Tags** – space or comma separated; stored as array
* **ASVS / Description / Tools / Links / Applicability / Sources** – free-text fields

---

## 🔒 Security

* All imported data is treated as **plain text** (no HTML execution).
* Links are stored as text only (no clickable anchors by default).
* LocalStorage is used for persistence; export data before clearing browser data.
* No external network requests, no server component.

---

## 📦 Roadmap

* [x] Priority levels and filters
* [x] Hide by Default toggle
* [x] Subcategory Notes
* [x] Fully working CSV/JSON import/export
* [ ] Preserve expanded/collapsed state between renders
* [ ] Related items by tag in Details panel
* [ ] Optional Markdown/Report export
* [ ] Performance optimization for very large checklists (virtual scrolling)

---