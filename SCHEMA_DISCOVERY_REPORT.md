# Database Schema Discovery Report

**Date:** 2026-04-09  
**Database:** noog-tsql01\bdp_nbs_demo01  

---

## What Exists (Confirmed)

### Server Databases
- **ihi-hi** — Contains only 2 tables (FieldMetadata, ValueMetadata)
- **master** — System database
- **model** — Template database
- **msdb** — System database
- **tempdb** — Temporary database

### ihi-hi Schema
Only **dbo** schema with tables:
- `FieldMetadata` (5 columns): FieldName, FieldLabel, DataType, SourceTable, ValueSet
- `ValueMetadata` (3 columns): Code_Set, Code, Description
- No views
- No other tables

---

## What's Missing (Not Found)

The following **form structure metadata** is NOT in the ihi-hi read-only exposure:

❌ **Repeating Block** — Which repeat blocks fields belong to + nesting level  
❌ **Display Order** — Field sequence on form  
❌ **Question Package ID/Name** — Section grouping (CLINICAL, ADMIN, DEMOGRAPHIC)  
❌ **Required/Enabled/Displayed** — Boolean flags  
❌ **Tooltip / Help Text** — Field guidance  

---

## What This Means

The `ihi-hi` database is a **minimal metadata export** containing only:
- Field definitions (name, label, data type, source)
- Value set definitions (for dropdowns)

It appears to be a **read-only snapshot** meant for reference/mapping, not a complete application schema.

The form structure metadata likely exists **elsewhere**:
- In another database (not accessible to this user account)
- In the main Maven application database (different instance)
- In an admin/design-time database
- In configuration files outside SQL Server

---

## Next Step: Contact Page

**Message to send:**

> "Our schema discovery found that ihi-hi only contains FieldMetadata (5 columns) and ValueMetadata (3 columns) — no form structure metadata. The repeating block, display order, question package, and flag data isn't exposed in the read-only ihi-hi database.
>
> Can you help identify where these exist? Are they:
> 1. In a different Maven database we should connect to?
> 2. In application tables that need special read access?
> 3. In configuration outside SQL Server?
>
> We need to know where to look, or if extraction needs to come from a different system/export."

---

## Files Generated

- FieldMetadata.csv (7,692 fields) ✅
- ValueMetadata.csv (171,671 codes) ✅
- Form structure exports — **ON HOLD pending Page's guidance**

---

## Takeaway

The current FieldMetadata + ValueMetadata extraction is complete and accurate for what's available. But the migration pipeline's **form structure requirements won't be met from ihi-hi** — they need to come from a different source that Page can identify.
