# SQL Server Database Documentation

## Overview

Connected to SQL Server instance: **noog-tsql01\bdp_nbs_demo01**

This documentation covers the metadata tables used to define and manage field configurations and their allowed values in the system.

---

## Databases

- **master** - Default system database
- **model** - Template for new databases
- **msdb** - SQL Server system database
- **tempdb** - Temporary database
- **ihi-hi** - Main application database containing FieldMetadata and ValueMetadata

---

## Table: dbo.FieldMetadata

**Database:** ihi-hi  
**Purpose:** Defines all available fields/columns in the system, their data types, and associated value sets

### Structure

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| FieldName | text | NO | Unique identifier for the field (e.g., DISEASE, ALL_ARBO) |
| FieldLabel | text | YES | Human-readable display label (e.g., "Disease", "All Arboviruses") |
| DataType | text | NO | The type of data: `Selection` (dropdown), `String`, etc. |
| SourceTable | text | NO | Source table this field originates from (e.g., GeneralModel) |
| ValueSet | text | YES | Reference to a value set in dbo.ValueMetadata for Selection fields |

### Sample Data

```
FieldName   FieldLabel              DataType    SourceTable   ValueSet
----------  ----------------------  ----------  -----------   --------
DISEASE     Disease                 Selection   GeneralModel  DISEASE
ALL_ARBO    All Arboviruses         String      GeneralModel  NULL
ALL_BT      Show for all BT         String      GeneralModel  NULL
```

### Query Examples

**Get all Selection-type fields (dropdowns):**
```sql
SELECT * FROM dbo.FieldMetadata 
WHERE DataType = 'Selection'
```

**Get all fields for a specific source table:**
```sql
SELECT * FROM dbo.FieldMetadata 
WHERE SourceTable = 'GeneralModel'
```

**Get fields with associated value sets:**
```sql
SELECT FieldName, FieldLabel, ValueSet 
FROM dbo.FieldMetadata 
WHERE ValueSet IS NOT NULL
```

---

## Table: dbo.ValueMetadata

**Database:** ihi-hi  
**Purpose:** Stores the allowed codes/values for Selection-type fields defined in dbo.FieldMetadata

### Structure

| Column | Data Type | Nullable | Description |
|--------|-----------|----------|-------------|
| Code_Set | text | NO | The value set identifier (e.g., DISEASE, matches FieldMetadata.ValueSet) |
| Code | text | YES | The actual code/value (e.g., NCOV, AMB, ANG) |
| Description | text | YES | Human-readable description of the code |

### Sample Data

```
Code_Set   Code    Description
---------  ------  ----------------------------------------
DISEASE    NCOV    2019 Novel Coronavirus (2019-nCoV)
DISEASE    AMB     Amebiasis
DISEASE    ANG     Angiostrongyliasis
```

### Query Examples

**Get all codes for a value set:**
```sql
SELECT Code, Description 
FROM dbo.ValueMetadata 
WHERE Code_Set = 'DISEASE'
ORDER BY Code
```

**Get all configured value sets:**
```sql
SELECT DISTINCT Code_Set 
FROM dbo.ValueMetadata 
ORDER BY Code_Set
```

**Get count of codes per value set:**
```sql
SELECT Code_Set, COUNT(*) as CodeCount 
FROM dbo.ValueMetadata 
GROUP BY Code_Set 
ORDER BY CodeCount DESC
```

---

## Relationships

```
dbo.FieldMetadata
    |
    | ValueSet (text)
    |
    ⬇
dbo.ValueMetadata.Code_Set (text)
```

**How it works:**

1. **FieldMetadata** defines a field with `DataType = 'Selection'` and `ValueSet = 'DISEASE'`
2. When rendering a dropdown UI, look up all rows in **ValueMetadata** where `Code_Set = 'DISEASE'`
3. Display the `Code` as the value and `Description` as the label to users

**Example:**
- **Field:** DISEASE (Disease) - Selection type
- **ValueSet points to:** DISEASE
- **Available options:** 
  - NCOV → 2019 Novel Coronavirus (2019-nCoV)
  - AMB → Amebiasis
  - ANG → Angiostrongyliasis

---

## Data Export Queries

Use these queries to extract the metadata needed for workbench integration.

### Three Core Queries (In Order of Importance)

#### 1. **Full Field Inventory** (Equivalent to GeneralModel spreadsheet)

```sql
SELECT FieldName, FieldLabel, DataType, SourceTable, ValueSet
FROM [ihi-hi].dbo.FieldMetadata
```

This gives you all 7,692 HI Maven field definitions directly from the source.

#### 2. **All Value Sets** (What ND Pages.xlsx was missing)

```sql
SELECT Code_Set, Code, Description
FROM [ihi-hi].dbo.ValueMetadata
ORDER BY Code_Set, Code
```

This is the piece your workbench was missing — `ND Pages.xlsx` had `code_set_name` empty for all parsed questions. HI's `ValueMetadata` has all 171,671 codes.

#### 3. **Main Export: Fields with Dropdown Values** (Complete flattened export)

```sql
SELECT 
    fm.FieldName,
    fm.FieldLabel,
    fm.DataType,
    fm.SourceTable,
    fm.ValueSet,
    vm.Code,
    vm.Description
FROM [ihi-hi].dbo.FieldMetadata fm
LEFT JOIN [ihi-hi].dbo.ValueMetadata vm 
    ON fm.ValueSet = vm.Code_Set
ORDER BY fm.FieldName, vm.Code
```

**This is the main export** — every field with its allowed values flattened out. Directly comparable to what your GeneralModel parser already ingests.

**Note:** Due to SQL Server's `text` data type limitations with sorting, use this modified version:
```sql
SELECT 
    fm.FieldName,
    fm.FieldLabel,
    fm.DataType,
    fm.SourceTable,
    fm.ValueSet,
    vm.Code,
    vm.Description
FROM [ihi-hi].dbo.FieldMetadata fm
LEFT JOIN [ihi-hi].dbo.ValueMetadata vm 
    ON CAST(fm.ValueSet AS varchar(max)) = CAST(vm.Code_Set AS varchar(max))
```

---

### Sizing Queries (Run First to Validate Completeness)

```sql
-- How many fields total?
SELECT COUNT(*) as field_count
FROM [ihi-hi].dbo.FieldMetadata

-- Distribution: dropdowns vs strings?
SELECT CAST(DataType AS varchar(max)) as DataType, COUNT(*) as cnt 
FROM [ihi-hi].dbo.FieldMetadata 
GROUP BY CAST(DataType AS varchar(max))

-- Value sets summary
SELECT COUNT(DISTINCT CAST(Code_Set AS varchar(max))) as value_sets, 
       COUNT(*) as total_codes 
FROM [ihi-hi].dbo.ValueMetadata

-- What source tables exist?
SELECT DISTINCT CAST(SourceTable AS varchar(max)) as SourceTable
FROM [ihi-hi].dbo.FieldMetadata
ORDER BY CAST(SourceTable AS varchar(max))
```

**Expected Results:**
- Field count: 7,692 (compare to Laura's GeneralModel baseline)
- Value sets: 2,238
- Total codes: 171,671
- Source tables: 10 (GeneralModel, HepModel, STDModel, LeadModel, ids_case, ids_contactpoint, ids_investigation, ids_investigationresult, ids_investigationresultattr, ids_party)

---

### Data Scope Summary

- **Total Fields:** 7,692
- **Total Value Sets:** 2,238
- **Total Codes:** 171,671
- **Selection/Dropdown Fields:** 2,854
- **String/Text Fields:** 3,160
- **Other Types:** ReferenceCode, Date, Number, TextArea, Integer, DateTime, Boolean, Case, User, DistinctID, DynamicList, Time
- **Source Tables:** 10

**Largest Value Sets:**
- ICD-9: 108,720 codes
- CS_COUNTIES: 26,304 codes
- CITIES: 12,482 codes
- CS_OCCUPATIONS: 4,170 codes
- CS_CANCER_TYPE: 3,299 codes

---

## Common Use Cases

### 1. Build a Dropdown UI for a Field
```sql
-- Get all options for a specific field
SELECT vm.Code, vm.Description
FROM dbo.FieldMetadata fm
JOIN dbo.ValueMetadata vm ON fm.ValueSet = vm.Code_Set
WHERE fm.FieldName = 'DISEASE'
ORDER BY vm.Code
```

### 2. Validate User Input
```sql
-- Check if a submitted value is valid for a field
SELECT COUNT(*) as IsValid
FROM dbo.ValueMetadata
WHERE Code_Set = 'DISEASE' AND Code = 'NCOV'
```

### 3. Add a New Field
```sql
-- Add a new field definition
INSERT INTO dbo.FieldMetadata (FieldName, FieldLabel, DataType, SourceTable, ValueSet)
VALUES ('NEW_FIELD', 'New Field Label', 'String', 'GeneralModel', NULL)
```

### 4. Add New Values to a Value Set
```sql
-- Add a new disease code
INSERT INTO dbo.ValueMetadata (Code_Set, Code, Description)
VALUES ('DISEASE', 'NEW', 'New Disease')
```

---

## Connection Details

**Server:** noog-tsql01\bdp_nbs_demo01  
**Authentication:** Windows (Integrated Security)  
**Default Database:** master  
**Application Database:** ihi-hi

### PowerShell Query Example

```powershell
. .\query.ps1

# Query FieldMetadata
$fields = Query-SqlServer -Query "SELECT * FROM dbo.FieldMetadata" -Database "ihi-hi"
$fields | Format-Table

# Query ValueMetadata
$values = Query-SqlServer -Query "SELECT * FROM dbo.ValueMetadata WHERE Code_Set = 'DISEASE'" -Database "ihi-hi"
$values | Format-Table
```

---

## Workbench Integration Notes

### Data Exports Already Generated

**Generated on 2026-04-09** using Query #1 and Query #2 (Split Export):
- `FieldMetadata.csv` - 0.69 MB (7,692 fields) — *From Query #1*
- `ValueMetadata.csv` - 8.77 MB (171,671 codes) — *From Query #2*

**Status:** ✅ Ready for workbench ingestion. Both files available at `C:\Users\wwang\Documents\sql-server-connection\`

**Why split export instead of Query #3?**
- Query #3 (LEFT JOIN) produces ~179,363 rows (all 7,692 fields + each field's codes)
- This large join times out on first execution
- Solution: Use split CSVs and join in your application (same final result, better performance)
- Both CSVs already match Query #1 and Query #2 patterns exactly

### Using the Exports

**In your workbench/application:**

1. **Load FieldMetadata.csv:**
   - Import all 7,692 field definitions
   - Each row specifies FieldName, FieldLabel, DataType, SourceTable, ValueSet

2. **Load ValueMetadata.csv:**
   - Import all 171,671 code values
   - Each row specifies Code_Set, Code, Description

3. **Build dropdowns in your UI:**
   ```sql
   SELECT vm.Code, vm.Description
   FROM fields fm
   JOIN values vm ON fm.value_set = vm.code_set
   WHERE fm.field_name = [user-selected-field]
   ORDER BY vm.code
   ```

### Data Comparison

- **HI Maven's FieldMetadata** = equivalent to Laura's `GeneralModel` spreadsheet (field definitions)
- **HI Maven's ValueMetadata** = what was **missing from ND Pages.xlsx** (the code_set_name field was empty for all parsed questions)
- **The two CSVs together** produce exactly what your existing GeneralModel ingestion pipeline expects

### Validation Checklist

If you need to regenerate/verify the exports:

```powershell
# Run in C:\Users\wwang\Documents\sql-server-connection

# Export FieldMetadata
. .\query.ps1
$fields = Query-SqlServer -Query "SELECT FieldName, FieldLabel, DataType, SourceTable, ValueSet FROM [ihi-hi].dbo.FieldMetadata" -Database "ihi-hi"
$fields | Export-Csv FieldMetadata.csv -NoTypeInformation -Encoding UTF8

# Export ValueMetadata  
$values = Query-SqlServer -Query "SELECT Code_Set, Code, Description FROM [ihi-hi].dbo.ValueMetadata" -Database "ihi-hi"
$values | Export-Csv ValueMetadata.csv -NoTypeInformation -Encoding UTF8
```

### Processing Notes

- Both tables use `text` data type for all columns, requiring `CAST(column AS varchar(max))` for sorting operations
- The `NULL` value in ValueMetadata.Code column suggests some codes may be optional
- ValueSet field in FieldMetadata provides the join key to ValueMetadata.Code_Set
- This is a typical metadata pattern used in configurable applications for managing dropdown options
- The LEFT JOIN ensures you capture String fields even though they have no associated value sets
- **Top 3 value sets by code count:**
  - ICD-9: 108,720 codes
  - CS_COUNTIES: 26,304 codes
  - CITIES: 12,482 codes
