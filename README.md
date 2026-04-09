# HI Maven SQL Server Connection & Parser

Tools and documentation for extracting metadata from HI Maven SQL Server database and parsing it for workbench integration.

## 📊 Data Overview

**What you have:**
- **7,692 fields** across 10 source tables (GeneralModel, HepModel, STDModel, LeadModel, ids_*)
- **171,671 code values** across 2,238 value sets
- **Complete field definitions** with labels, data types, and value set mappings

**Key improvements over ND data:**
- ✅ Complete value sets (ND Pages.xlsx had empty code_set_name)
- ✅ Multiple disease modules (not just GeneralModel)
- ✅ Full data type support (Selection, String, Date, Number, ReferenceCode, Boolean, etc.)

## 📁 Project Files

### Documentation
- `DATABASE_DOCUMENTATION.md` - Complete schema, queries, and workbench integration guide
- `PARSER_USAGE.md` - Python parser usage examples and schema reference
- `README.md` - This file

### PowerShell Scripts
- `query.ps1` - Reusable SQL query function (with built-in `Query-SqlServer`)
- `connect.ps1` - Test database connection
- `metadata-info.ps1` - Inspect table structures
- `export-scope.ps1` - Run all sizing queries
- `export-separate.ps1` / `export-values.ps1` - Export data to CSV

### CSV Exports
- `FieldMetadata.csv` (0.69 MB) - All 7,692 field definitions
- `ValueMetadata.csv` (8.77 MB) - All 171,671 code values

### Python Parser
- `hi_maven_parser.py` - Convert CSVs to standardized Question objects
- Can parse, filter, and export to JSON/CSV

## 🚀 Quick Start

### PowerShell: Query Database

```powershell
cd C:\Users\wwang\Documents\sql-server-connection
. .\query.ps1

# Query fields
$fields = Query-SqlServer -Query "SELECT TOP 10 * FROM [ihi-hi].dbo.FieldMetadata" -Database "ihi-hi"
$fields | Format-Table

# Query values for a specific value set
$values = Query-SqlServer -Query "SELECT * FROM [ihi-hi].dbo.ValueMetadata WHERE Code_Set = 'DISEASE'" -Database "ihi-hi"
$values | Format-Table
```

### Python: Parse for Workbench

```python
from hi_maven_parser import HiMavenParser

parser = HiMavenParser()
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

# Export to JSON
parser.export_json('hi_maven_questions.json')

# Get hepatitis fields only
hep_fields = parser.get_by_source_table('HepModel')
```

## 🗄️ Database Connection

- **Server:** `noog-tsql01\bdp_nbs_demo01`
- **Database:** ihi-hi (contains FieldMetadata and ValueMetadata)
- **Authentication:** Windows (Integrated Security)
- **No installation required** - PowerShell uses built-in .NET Framework

## 📋 Schema Reference

### FieldMetadata (7,692 rows)
| Column | Type | Example |
|--------|------|---------|
| FieldName | text | `DISEASE` |
| FieldLabel | text | `Disease` |
| DataType | text | `Selection` \| `String` \| `Date` \| `Number` |
| SourceTable | text | `GeneralModel` \| `HepModel` \| `STDModel` |
| ValueSet | text | `DISEASE` (references ValueMetadata.Code_Set) |

### ValueMetadata (171,671 rows)
| Column | Type | Example |
|--------|------|---------|
| Code_Set | text | `DISEASE` |
| Code | text | `NCOV` |
| Description | text | `2019 Novel Coronavirus (2019-nCoV)` |

## 🗺️ Module Mapping

| SourceTable | Module | Purpose |
|-------------|--------|---------|
| GeneralModel | General | Core/common fields |
| HepModel | Hepatitis | Hepatitis investigation |
| STDModel | STD | Sexually transmitted disease investigation |
| LeadModel | Lead | Lead exposure investigation |
| ids_case | Case Mgmt | Case data |
| ids_contactpoint | Contact Mgmt | Contact tracing |
| ids_investigation | Investigation | Investigation workflow |
| ids_investigationresult | Results | Lab/investigation results |
| ids_investigationresultattr | Result Attrs | Result attributes |
| ids_party | Parties | People/organizations |

## 📚 Complete Documentation

See **DATABASE_DOCUMENTATION.md** for:
- All SQL queries (sizing, export, join patterns)
- Complete schema documentation
- Common use cases
- Workbench integration patterns

See **PARSER_USAGE.md** for:
- Python parser API
- Usage examples
- Export formats (JSON, CSV)
- Filtering methods

## 💾 CSV Files Ready to Use

Both CSV files are already generated and ready:
- `FieldMetadata.csv` - Import into your field definitions table
- `ValueMetadata.csv` - Import into your value sets table

**To regenerate:**
```powershell
. .\query.ps1

$fields = Query-SqlServer -Query "SELECT FieldName, FieldLabel, DataType, SourceTable, ValueSet FROM [ihi-hi].dbo.FieldMetadata" -Database "ihi-hi"
$fields | Export-Csv FieldMetadata.csv -NoTypeInformation -Encoding UTF8

$values = Query-SqlServer -Query "SELECT Code_Set, Code, Description FROM [ihi-hi].dbo.ValueMetadata" -Database "ihi-hi"
$values | Export-Csv ValueMetadata.csv -NoTypeInformation -Encoding UTF8
```

## 🎯 Next Steps

1. **Review Documentation**: Start with DATABASE_DOCUMENTATION.md
2. **Use CSV Exports**: Import FieldMetadata.csv and ValueMetadata.csv into your workbench
3. **Run Parser**: Use hi_maven_parser.py to generate standardized question objects
4. **Map to Pages**: Use SourceTable for page/disease grouping

## 📝 License

HI Maven metadata extracted from noog-tsql01\bdp_nbs_demo01 SQL Server.
