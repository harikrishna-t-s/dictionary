# TESLA DOC — Instruction Manual

A fast, Notion-inspired study reference and clinical protocol lookup tool. Built as a single, self-contained web app with zero dependencies.

---

## 📌 Where the Data Lives

All protocol data is stored directly inside [`index.html`](index.html) within the dedicated `<script type="text/markdown" id="study-data">` section.

- **Zero network requests needed** — loads instantly and reliably everywhere.
- **Works offline and on local files** — you can double-click `index.html` to run it offline in any browser.
- **100% compatible with Vercel**, Netlify, GitHub Pages, or any static host.

---

## ✍️ How to Edit or Add Studies

Open [`index.html`](index.html) in any text editor and scroll to the section labeled:

```html
<!-- ═══════════════════════════════════════════════════════════
     DATA SOURCE (Markdown)
     To add, edit, or remove studies, edit the markdown below.
══════════════════════════════════════════════════════════════ -->
<script type="text/markdown" id="study-data">
...
</script>
```

### Markdown Formatting Pattern

```markdown
## Category Name

### Study Name
- **Summary:** One line shown on the card preview (before expanding)
- **Also known as:** Short names, abbreviations, keywords (boosts search ranking)
- **Prep:** Fasting or prep instructions
- **Duration:** Estimated time
- **Any Custom Label:** Any value you need
  - Indented bullet continuation for the label above
A plain line or bullet without a label becomes a general note.
```

### Formatting Rules

| Syntax | Meaning |
|---|---|
| `# Title` | Sets the page title and breadcrumb header (e.g. `# TESLA DOC`). |
| `## Category` | Defines a category. Each category automatically generates a filter chip at the top. |
| `### Study Name` | Defines a new study card. Keep names concise and recognizable. |
| `- **Summary:** text` | Displayed directly on the collapsed card preview. If omitted, the first field is used. |
| `- **Also known as:** text` | Add abbreviations (e.g. `CECT`, `HRCT`, `FBS`), alternate spellings, or search keywords. |
| `- **Label:** Value` | Key-value pairs displayed inside the expanded card details. |
| `  - Indented item` | Belongs as a sub-bullet under the field above it. |
| `**bold text**` | Highlights critical safety notes or timings. |
| `<!-- comments -->` | Ignored by the parser. |

---

## 🚀 How to Run Locally

Because the data is embedded directly in `index.html`:

- **Option A (Instant):** Double-click `index.html` to open it directly in any browser (`file:///...`).
- **Option B (Local Web Server):**
  ```bash
  # Using Python (standard on macOS & Linux)
  python3 -m http.server 3000
  ```
  Then navigate to `http://localhost:3000`.

---

## ☁️ Deployment

### Vercel
This project is pre-configured for Vercel:
1. Push your repository to GitHub, GitLab, or Bitbucket.
2. In Vercel, click **Add New...** → **Project** and select this repository.
3. Vercel automatically deploys `index.html` as a fast static site.

---

## 🎨 Design System

- **Theme:** Notion-inspired light theme.
- **Palette:** Minimalist black & white canvas with violet accent family (`#6d28d9` / `#7c3aed`).
- **Animations:** Fluid CSS Grid accordion expansion (`0fr` → `1fr`), spring-eased chevrons, staggered search result entry, and floating empty states.
- **Search Engine:** Built-in multi-token search with alias weighting and fuzzy spelling tolerance.
