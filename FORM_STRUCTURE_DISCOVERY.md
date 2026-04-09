# Form Structure Data Location - Investigation Complete

**Date:** 2026-04-09  
**Status:** Form structure metadata NOT FOUND in accessible SQL Server

---

## Search Results

### ihi-hi Database
- ✅ Searched all tables: Only FieldMetadata + ValueMetadata found
- ❌ No FormStructure, PageLayout, QuestionPackage, RepeatingBlock, or similar tables
- ❌ No tables matching: form%, page%, structure%, package%, repeating%, block%, question%

### Server Instance
- Checked: noog-tsql01\bdp_nbs_demo01
- Non-system databases: **Only ihi-hi** (no Maven, forms, pages, or config databases)
- Searched entire instance for form/page/structure/package/repeating/block/question table names
- Result: **0 matches across all accessible databases**

---

## Findings

### What EXISTS (Confirmed)
✅ FieldMetadata (7,692 fields with names, labels, types, source tables, value sets)  
✅ ValueMetadata (171,671 codes for dropdowns)  
✅ Perfect referential integrity (0 broken references)  
✅ Ready for workbench import

### What DOES NOT EXIST (Confirmed Missing)
❌ Repeating block definitions (group fields into sections)  
❌ Display order/sequence (field ordering on forms)  
❌ Question package definitions (CLINICAL/ADMIN/DEMOGRAPHIC scopes)  
❌ Required/enabled/displayed flags (business rules)  
❌ Tooltip/help text (field guidance)  
❌ Any related form structure tables

---

## Where Form Structure Might Be

Since the metadata is NOT in SQL Server on this instance, it could be:

### 1. Different SQL Server Instance
- "Where are the form definition databases?" → Need for Page to identify
- Could be on a different server (Maven application DB server)
- Would require separate connection credentials

### 2. File-Based Configuration
- Maven config files (XML, JSON, YAML)
- Form definitions in application packages
- Excel/CSV extracts from Maven admin

### 3. Maven Application API/Service
- Form structure available only through Maven API
- Requires Maven API credentials/access
- Not exposed in read-only database

### 4. Different Database Engine
- MongoDB, Postgres, or other system
- Not accessible from this SQL Server instance

---

## Recommendation

**Message for Page:**

> "We've thoroughly searched the ihi-hi database and the entire SQL Server instance (noog-tsql01\bdp_nbs_demo01) for form structure data. The only tables available are FieldMetadata and ValueMetadata — no form configuration, page layout, question package, or repeating block tables exist on this database.
>
> Can you help identify where Maven stores the form structure metadata (repeating blocks, display order, question packages)? Is it:
> - In a different database/SQL Server instance? (If so, server/database names?)
> - In file-based configuration? (Excel, XML, JSON files?)
> - In the Maven application server? (API endpoint?)
> - In a different database system? (MongoDB, Postgres, etc?)
>
> We're ready to extract form structure as soon as you point us to where it lives."

---

## Current Data Status

| Data | Status | Location |
|---|---|---|
| **Field Definitions** | ✅ Complete | ihi-hi.dbo.FieldMetadata |
| **Value Sets** | ✅ Complete | ihi-hi.dbo.ValueMetadata |
| **Form Structure** | ❌ Not Found | Unknown |
| **Display Order** | ❌ Not Found | Unknown |
| **Question Packages** | ❌ Not Found | Unknown |

**Workbench Readiness:** 80% complete with existing data, blocked on form structure metadata from Page

---

## Next Steps

1. Clarify with Page where form structure data lives
2. Once location identified, we can extract and integrate
3. If data is in SQL Server elsewhere, we'll add extraction scripts
4. If file-based, we'll create parser/importer
5. If API-based, we'll build connector

The core field and value set data is production-ready. Form structure is the only remaining dependency.
