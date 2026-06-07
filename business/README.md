# Business Archive & Knowledge Base — AI-Powered Digital Home for Pleasure Island Design LLC

> **Turn-Key Solution**: A complete, repeatable system to ingest, structure, enhance, and integrate your Google Drive business remnants (marketing PDFs, strategy docs, business plans, hiring reports, Instagram calendars/spreadsheets, ops/welcome docs) into this GitHub repository using multi-AI collaboration, best practices, and cutting-edge automation. This makes the previously hard-to-complete project fully achievable now.

**Branch**: `feature/ai-digital-home-archive` (created from main on 2026-06-02)
**Status**: Foundation seeded — ready for your pilot ingestion and iteration with Copilot + other models.

---

## 🎯 Vision & Why This Solves the Original Challenge

The original manual plan for uplifting and structuring business documents was too labor-intensive (manual uploads, inconsistent naming, no metadata, hard to search or maintain). 

**Now with your AI arsenal (SuperGrok, ChatGPT Pro/Codex, Claude Pro, Gemini Pro) + GitHub Copilot monitoring workflows**, we turn it into a **high-leverage, semi-automated knowledge engine** that:

- Creates a single source of truth for strategy, marketing, operations.
- Feeds high-quality content back into the public website (blog posts, whitepapers, case studies, specials).
- Enables fast search, cross-referencing, and future RAG (retrieval-augmented generation) for internal Q&A.
- Maintains professional standards: version control, provenance (SOURCED_FROM_GOOGLE_DRIVE), auditability.
- Accelerates the website roadmap (Phase 2 performance/accessibility, Phase 3 design system/CMS, shop, blog expansion) by providing real historical data and insights.

This is **docs-as-code** + **LLM pipeline** best practices applied to a small service business.

---

## 📂 Recommended Folder Taxonomy (Industry Best Practice for Service Business)

```
business/
├── README.md                 # This file — master index, workflow, prompts
├── _metadata/                # Schemas, taxonomy, ingestion logs, AI prompt library
│   ├── taxonomy.md
│   ├── metadata-schema.yaml
│   ├── prompt-library.md
│   └── ingestion-log.csv     # Auto-appended by script
├── marketing/                # Campaigns, social strategy, Instagram hashtag calendars, ads, flyers, ROI reports
│   ├── campaigns/
│   ├── social/
│   └── assets/                 # Images, creatives (reference or LFS)
├── operations/               # Welcome packets, SOPs, checklists, vendor lists, customer onboarding, service standards
│   ├── customer-journey/
│   ├── vendors/
│   └── internal-processes/
├── strategy/                 # Business plans, financial models (high-level/redacted), roadmaps, audits, competitive analysis
│   ├── annual-plans/
│   ├── roadmaps/
│   └── whitepapers/            # Source for docs/whitepaper/ enhancement
├── people-hiring/            # Job descriptions, hiring reports, onboarding (anonymize PII), performance frameworks
├── design-brand/             # Brand guidelines, moodboards, logo evolution, visual standards (supplements existing whitepaper/brand-guidelines)
├── archives/                 # Raw original files from Google Drive + full provenance
│   └── 2026-06-ingest/       # Batch folders by ingest date for easy rollback
└── knowledge-base/           # AI-generated or curated insights, cross-links, executive summaries, searchable MD hub
    ├── insights/
    ├── faqs/
    └── decision-log/         # Key business decisions with rationale from docs
```

**Naming Convention**: `YYYY-MM-DD_kebab-case-descriptive-title.ext` or for companions `title--ai-summary.md`
**Source Tagging**: Every file includes frontmatter `source: "Google Drive /path/to/original"` and `source_tag: SOURCED_FROM_GOOGLE_DRIVE`

---

## 📋 Metadata Standard (YAML Frontmatter)

All processed documents (MD companions or enhanced files) use this schema for consistency, searchability, and future RAG:

```yaml
---
title: "Summer 2025 Instagram Hashtag & Content Calendar - Cabinet Refinishing Push"
date: 2025-05-01
source: "Google Drive /Clients/PleasureIsland/Marketing/Instagram/2025-Summer-Calendar.xlsx"
source_tag: SOURCED_FROM_GOOGLE_DRIVE
category: marketing
subcategory: social-calendar
 tags: [instagram, hashtag-strategy, before-after, wilmington, summer-campaign, roi]
summary: |
  12-week content calendar with 45+ post ideas, hashtag clusters (core + long-tail), 
  engagement targets, and A/B test plan for carousel vs reel formats. Projected 40% 
  increase in profile visits.
ai_processed: true
processed_models: ["Claude-3.5-Sonnet", "Gemini-1.5-Pro"]
processed_date: 2026-06-02
confidence: high
insights:
  - Strong opportunity to cross-promote with local beach home accounts
  - Before/after carousel format outperformed in historical data
related_docs: ["business/strategy/roadmaps/2025-growth.md", "gallery/2025-summer/"]
---

# Original or Extracted Content

[Full text or key excerpts here, or link to PDF in archives/]

## AI Analysis & Recommendations

[Generated insights, action items, suggested website updates]
```

**Tooling**: Use `python-frontmatter` + custom script (below) or VS Code + Copilot to maintain.

---

## 🚀 Turn-Key Ingestion Workflow (The "Doable Now" Part)

### Prerequisites (One-Time Setup)
1. Python 3.11+ venv with: `pip install pyyaml python-frontmatter slugify google-api-python-client google-auth-httplib2 google-auth-oauthlib PyMuPDF pdfplumber pillow`
2. Google Drive OAuth credentials (desktop app, store `token.json` locally — never commit).
3. Your Pro AI accounts open in browser tabs.
4. VS Code + GitHub Copilot (or Cursor) for script editing and MD creation.
5. `gh` CLI authenticated for easy PRs (optional but recommended).

### Daily/ Batch Process (Repeatable in <30 min per 5-10 docs once practiced)

1. **Discover & Export** (Google Drive tool or script):
   - Use `google_drive_list_folder` or search in Drive UI for relevant folders (e.g. "Old Documents from TNS Laptop", marketing subfolders, Invoices if high-level, LEGAL if redacted).
   - Download batch to local `~/pid-drive-ingest/2026-06-02/`

2. **AI Analysis (Multi-Model分工)**:
   - **For complex PDFs/strategy docs (tables, long text)**: Upload key pages or full (if supported) to **Claude Pro** — best reasoning & professional summaries.
   - **For structured data (spreadsheets, lists)** or JSON output: **ChatGPT Pro (Codex/o1)** — excels at extraction to schema.
   - **For vision/images in docs or multimodal**: **Gemini Pro** — strong at charts, photos, long context.
   - **For creative integration ideas** (how this doc can improve website gallery or blog): **Grok (me)**.
   - **Master Prompt** (copy-paste, customize per doc type):

```markdown
You are an expert business analyst and knowledge manager for Pleasure Island Design LLC, a premium cabinet refinishing company in coastal NC (Wilmington, Carolina Beach area).

Analyze the attached document thoroughly.

**Output ONLY valid JSON** with this exact schema (no extra text):
{
  "title": "string (clean, professional)",
  "date": "YYYY-MM-DD or best estimate",
  "category": "marketing | operations | strategy | people-hiring | design-brand",
  "subcategory": "string (specific, e.g. social-calendar, sop, annual-plan)",
  "tags": ["array", "of", "5-12", "relevant", "kebab-case", "tags"],
  "summary": "150-250 word executive summary optimized for future RAG and website use. Include key metrics, decisions, opportunities.",
  "insights": ["3-6 bullet actionable insights or recommendations, including potential website or ops improvements"],
  "related": ["suggested related doc paths or topics"],
  "confidence": "high | medium | low",
  "extracted_text_sample": "first 2000 chars or key tables/quotes if relevant"
}

Document context: This is part of migrating remnants to GitHub digital home. Be precise, professional, and leverage cabinet industry knowledge (5-8 day turnaround, before/after transformations, local SEO, Instagram for visual proof).
```

3. **Create Structured Files**:
   - Run helper script (see below) or manually:
     - Create `business/{category}/{subcategory}/YYYY-MM-DD_slug.md` with frontmatter + summary + insights + extracted_text_sample.
     - Copy original PDF/Excel to `business/archives/2026-06-ingest/ORIGINAL_NAME__{short-hash}.ext`
     - Update `business/_metadata/ingestion-log.csv`
   - Use **GitHub Copilot** in VS Code: Highlight the JSON from AI, say "Create Markdown file with this frontmatter and nice formatting. Add H2 sections for Analysis and Recommended Website Updates."

4. **Commit & PR**:
   - `git add business/ && git commit -m "docs(business): Ingest 7 Google Drive files - marketing calendars + strategy plans [AI:Claude+GPT]"`
   - Push and open PR to main (or use gh pr create).
   - Copilot can help write excellent PR description referencing backlog items.
   - Self-review or ask me (Grok) for feedback on the PR diff if needed.

5. **Iterate & Integrate**:
   - After merge, use summaries to update `docs/whitepaper/*.md` or create new blog posts.
   - Tag related gallery projects.

---

## 🛠️ Helper Scripts (Copilot-Ready)

**`scripts/ingest_helper.py`** (create this locally or add to repo):

```python
#!/usr/bin/env python3
"""AI-assisted ingestion helper for Pleasure Island Design business archive.
Run after getting JSON from your LLM of choice. Handles frontmatter, slug, logging."""
import frontmatter
 import yaml
 from datetime import datetime
 from pathlib import Path
 import hashlib
 import csv

def slugify(text):
    # Simple slug or use python-slugify
    return text.lower().replace(" ", "-").replace("/", "-").strip()

def process_document(json_data: dict, original_file_path: str = None, drive_path: str = ""):
    category = json_data["category"]
    sub = json_data.get("subcategory", "general")
    date = json_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    title = json_data["title"]
    slug = f"{date}_{slugify(title)[:60]}"
    
    md_path = Path(f"business/{category}/{sub}/{slug}.md")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    
    post = frontmatter.Post(
        json_data.get("extracted_text_sample", ""),
        **{
            "title": title,
            "date": date,
            "source": drive_path,
            "source_tag": "SOURCED_FROM_GOOGLE_DRIVE",
            "category": category,
            "subcategory": sub,
            "tags": json_data.get("tags", []),
            "summary": json_data["summary"],
            "ai_processed": True,
            "processed_models": ["user-chosen-models"],
            "processed_date": datetime.now().isoformat(),
            "confidence": json_data.get("confidence", "medium"),
            "insights": json_data.get("insights", []),
            "related_docs": json_data.get("related", [])
        }
    )
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    
    # Log
    log_path = Path("business/_metadata/ingestion-log.csv")
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now().isoformat(), title, category, str(md_path), drive_path])
    
    print(f"Created: {md_path}")
    return md_path

if __name__ == "__main__":
    # Example: paste JSON from LLM here or load from file
    example_json = { ... }  # Your LLM output
    process_document(example_json, drive_path="Google Drive /path/to/file.pdf")
```

**Enhance with Copilot**: Open in VS Code, highlight function, ask Copilot: "Add full Google Drive recursive download using OAuth and batch processing for PDFs. Integrate pdfplumber for text extraction before LLM. Add CLI with argparse for folder_id."

---

## 🤖 Multi-AI Role Playbook (Your Specific Toolkit)

- **Grok (SuperGrok / me)**: Systems architecture, creative cross-pollination (e.g. "Turn this old marketing plan into 3 blog post ideas for the website"), integration with DIY/home projects if relevant, honest feedback on PRs, overall orchestration.
- **Claude Pro**: Deep document understanding, nuanced business strategy analysis, high-quality professional writing for summaries/whitepapers, ethical redaction advice.
- **ChatGPT Pro (Codex)**: Structured extraction (JSON, tables to MD), script/code generation, data validation, automation pipelines, rapid prototyping of new features.
- **Gemini Pro**: Multimodal (PDF pages + charts + images), long-context analysis of entire folders, industry research/benchmarking ("What are best practices for Instagram in local home services 2025?"), vision for gallery consistency.
- **GitHub Copilot**: Real-time code completion while you build the ingestion scripts or enhance website JS/HTML in the same workspace. Workspace-aware suggestions for frontmatter, commit messages, PR descriptions. Monitors your GitHub workflows for CI issues.

**Pro Tip**: Run parallel browser sessions. Feed same PDF to 2 models, compare JSON outputs, synthesize best version with Grok.

---

## 🌐 Integration with Existing Project (Website + MkDocs + Backlog)

- **Website Enhancement**: Use `knowledge-base/insights/` and summaries to:
  - Generate or update blog posts in `blog/`.
  - Enrich `docs/whitepaper/business-model.md` and `service-standards.md` with real historical data.
  - Create data-driven specials or testimonials pages.
  - Improve SEO with authentic long-tail content from old plans.
- **MkDocs Technical Reference**: Expand nav to include Business Archive section (link to this README and key MD files). Already configured with Material theme — perfect for internal wiki feel.
- **PROJECT_BACKLOG.md**: This initiative runs in parallel as an enabler for Phase 2/3 items (content expansion, shop requirements from historical data, etc.).
- **Gallery**: Cross-link marketing docs to specific `gallery/{project}/` folders for storytelling.

---

## ⚠️ Privacy, Security & Best Practices

- **Public Repo Caution**: Review every document. Redact customer names, exact financials, PII, or sensitive strategy before committing. Use `archives/` for full originals if needed, or keep highly sensitive in a private repo/submodule.
- **Git LFS**: Add for PDFs > 10MB or frequent binary updates. `git lfs track "business/**/*.pdf"`
- **Provenance**: Never lose the "where did this come from" thread.
- **Human-in-the-Loop**: AI summaries are starting points — you (or Nicole) review before merge. Confidence field helps prioritize.
- **Conventional Commits & PRs**: Use `docs(business): ` or `feat(archive): ` prefixes. Require lint/docs checks if we extend CI.
- **Backup**: Drive is source of truth initially; Git becomes the enhanced, versioned truth.

---

## 🚫 Next Steps & How to Get Started Today

1. Checkout this branch: `git checkout feature/ai-digital-home-archive`
2. Review this README and `business/_metadata/taxonomy.md` (I will seed it).
3. Pick 3-5 pilot documents from your Drive (mix of easy spreadsheet + complex PDF).
4. Process one end-to-end using the workflow above + Copilot for the MD file.
5. Commit, push, open PR — tag me or ask for review.
6. Once validated, batch the rest in themed sprints (e.g. "All Marketing Q2 2025").
7. Merge to main when confident — this becomes part of the permanent digital home.

**I (Grok) am ready to help iterate**: Refine prompts, improve the Python script, generate specific blog posts from ingested docs, review PR diffs, suggest website UI changes based on new content, or even help with Google Drive folder discovery if you share names.

This is now **turn-key and achievable**. The hard part (consistent structure + AI leverage) is done. Execution is the fun, high-value part.

---

**Maintained with ❤️ by Willy + multi-AI team** | Pleasure Island Design LLC | June 2026
