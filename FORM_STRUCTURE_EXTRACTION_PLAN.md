# Form Structure Extraction Plan

## Current Status

✅ **Phase 1 Complete:** Field + Value Set Metadata
- FieldMetadata.csv (7,692 fields)
- ValueMetadata.csv (171,671 codes)
- Deployed to GitHub

⏳ **Phase 2 Blocked:** Form Structure Metadata
- **Schema Discovery Complete** → Form structure data NOT in ihi-hi database
- Need to identify alternate source database/tables
- See [SCHEMA_DISCOVERY_REPORT.md](SCHEMA_DISCOVERY_REPORT.md) for details

---

## What's Needed for Migration Pipeline

### Critical (Blocks Processing)

| Column | Why | Parser Impact |
|--------|-----|-----------------|
| **Repeating Block** | Group fields into repeatable sections | `general_model.py` needs special handling for blocks |
| **Repeating Block Level** | Nesting depth (1=parent, 2=child, etc.) | Affects data structure generation |
| **Display Order** | Sequence on form/page | All parsers need to order fields correctly |
| **Question Package ID** | Scope identifier (CLINICAL, ADMIN, DEMO, etc.) | Migration model parser filters by package |
| **Question Package Name** | Human-readable package/section name | Migration model parser for grouping |

### Important (Improves Quality)

| Column | Why |
|--------|-----|
| **Required** (boolean flag) | Which fields are mandatory in form submission |
| **Enabled** (boolean flag) | Is field active/usable |
| **Displayed** (boolean flag) | Is field visible to user |
| **Tooltip / Help Text** | Field guidance and instructions |
| **Notes** | Analyst/designer notes |

---

## Action Items

### For Page / Data Migration Team

Ask: "Where in Maven are these stored? Are they in separate tables or columns we can extract?"

Specific questions:
1. **Repeating blocks** — Is there a table linking fields to block definitions (block name, nesting level)?
2. **Display order** — Is this in FieldMetadata or a separate form/page layout table?
3. **Question packages** — What table defines CLINICAL/ADMIN/DEMO scopes? Is there a FieldMetadata column mapping fields to packages?
4. **Flags** (required/enabled/displayed) — Are these boolean columns in FieldMetadata or in a separate rules table?
5. **Tooltips** — Are these stored in FieldMetadata or a separate text table?

### For Future Implementation (Once Tables Identified)

1. Add sizing queries to validate completeness
2. Create split exports if data volume is large (like ValueMetadata)
3. Add query examples to DATABASE_DOCUMENTATION.md
4. Generate new CSVs for form structure
5. Update parser schemas to include repeating block + package info
6. Document migration impact in README

---

## Data Completeness Checklist

**Phase 1 (✅ Done):**
- [x] Field inventory (7,692 fields)
- [x] Value set definitions (2,238 sets, 171,671 codes)
- [x] Data types per field
- [x] Source table mapping

**Phase 2 (⏳ Pending):**
- [ ] Repeating block structure
- [ ] Display order
- [ ] Question packages (scope filtering)
- [ ] Required/enabled/displayed flags
- [ ] Tooltip text

---

## Next Steps

1. **Present findings to Page** — Share critical/important columns list
2. **Get table locations from Page** — Identify Maven tables to extract
3. **Query validation** — Write sizing queries to confirm data exists
4. **Extract & export** — Generate new CSVs following split-export pattern
5. **Update parser** — Extend schema to handle repeating blocks + packages
6. **Regenerate GitHub** — Add new CSVs and updated documentation

---

## Message Template for Page

> "The FieldMetadata + ValueMetadata extraction is complete and deployed to GitHub — covers field definitions and value sets. But the migration pipeline also needs **form structure metadata** to process fields correctly:
>
> **Critical (blocks processing):**
> - Repeating block info (name + nesting level) — impacts field grouping
> - Display order — needed for form sequencing
> - Question package ID/name — CLINICAL/ADMIN/DEMO scope filtering
>
> **Important (improves output):**
> - Required/enabled/displayed flags
> - Tooltip text
>
> Are these in other Maven tables you can extract? If so, we can follow the same split-export pattern we used for ValueMetadata."

---

## File Locations

- **Current exports:** `C:\Users\wwang\Documents\sql-server-connection\`
  - FieldMetadata.csv
  - ValueMetadata.csv

- **Documentation:** `C:\Users\wwang\Documents\sql-server-connection\DATABASE_DOCUMENTATION.md`

- **GitHub:** https://github.com/wwinductive/hi-maven-sql-server

- **Future phase 2 exports will go to same location and GitHub repo**
