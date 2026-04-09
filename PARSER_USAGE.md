# HI Maven Parser Usage Guide
# Since Python isn't readily available, here's a reference implementation
# for how to use the hi_maven_parser.py when Python is installed

## Installation

Once Python is properly installed, install the parser in your project:

```bash
cd C:\Users\wwang\Documents\sql-server-connection
python -m pip install dataclasses
```

## Usage Examples

### Example 1: Basic Parsing

```python
from hi_maven_parser import HiMavenParser

# Create parser instance
parser = HiMavenParser()

# Parse the CSV files
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

print(f"Loaded {len(questions)} questions")
```

### Example 2: Export to JSON and CSV

```python
parser = HiMavenParser()
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

# Export to JSON (one question per object with value options)
parser.export_json('hi_maven_questions.json')

# Export to CSV (summary format)
parser.export_csv('hi_maven_questions.csv')

# Print summary
parser.print_summary()
```

### Example 3: Filter by Disease/Module

```python
parser = HiMavenParser()
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

# Get all Hepatitis fields
hep_fields = parser.get_by_source_table('HepModel')
for q in hep_fields:
    print(f"{q.field_name}: {q.field_label}")

# Get all STD fields
std_fields = parser.get_by_source_table('STDModel')

# Get all Lead exposure fields
lead_fields = parser.get_by_source_table('LeadModel')

# Get all dropdown/selection fields
dropdowns = parser.get_dropdown_fields()
print(f"Found {len(dropdowns)} selection fields with values")
```

### Example 4: Access Individual Question Data

```python
parser = HiMavenParser()
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

# Each question is a Question object with:
q = questions[0]
print(f"ID: {q.question_id}")
print(f"Field Name: {q.field_name}")
print(f"Label: {q.field_label}")
print(f"Data Type: {q.data_type}")
print(f"Module: {q.source_table}")
print(f"Value Set: {q.value_set_name}")

# If it's a dropdown field
if q.value_options:
    print(f"  Options ({len(q.value_options)}):")
    for option in q.value_options[:10]:  # Show first 10
        print(f"    {option.code}: {option.description}")
```

### Example 5: Convert to Dictionary or JSON String

```python
parser = HiMavenParser()
questions = parser.parse('FieldMetadata.csv', 'ValueMetadata.csv')

# Get single question as dict
q = questions[0]
d = q.to_dict()

# Get single question as JSON string
json_str = q.to_json()
print(json_str)
```

---

## Output Formats

### JSON Export Structure

```json
{
  "metadata": {
    "source": "HI_Maven",
    "total_fields": 7692,
    "total_value_sets": 2238,
    "source_tables": ["GeneralModel", "HepModel", "STDModel", ...]
  },
  "questions": [
    {
      "question_id": "HI_DISEASE",
      "field_name": "DISEASE",
      "field_label": "Disease",
      "data_type": "Selection",
      "source_table": "GeneralModel",
      "value_set_name": "DISEASE",
      "value_options": [
        {
          "code": "NCOV",
          "description": "2019 Novel Coronavirus (2019-nCoV)"
        },
        {
          "code": "AMB",
          "description": "Amebiasis"
        }
      ]
    },
    ...
  ]
}
```

### CSV Export Structure

```
question_id,field_name,field_label,data_type,source_table,value_set_name,value_count
HI_DISEASE,DISEASE,Disease,Selection,GeneralModel,DISEASE,3
HI_ALL_ARBO,ALL_ARBO,All Arboviruses,String,GeneralModel,,0
```

---

## Schema Reference

### Question Object

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| question_id | string | Auto-generated | Format: `HI_<FieldName>` (e.g., `HI_DISEASE`) |
| field_name | string | FieldMetadata.FieldName | Unique field identifier |
| field_label | string | FieldMetadata.FieldLabel | Human-readable label |
| data_type | string | FieldMetadata.DataType | Selection, String, Date, Number, etc. |
| source_table | string | FieldMetadata.SourceTable | GeneralModel, HepModel, STDModel, LeadModel, ids_* tables |
| value_set_name | string/null | FieldMetadata.ValueSet | Reference to value set (null for non-selection fields) |
| value_options | ValueOption[] | ValueMetadata | List of allowed codes/descriptions |

### ValueOption Object

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| code | string | ValueMetadata.Code | The code/value |
| description | string | ValueMetadata.Description | Human-readable description |

---

## Module/Disease Mapping

SourceTable → Module/Disease:
- `GeneralModel` → General/Core fields
- `HepModel` → Hepatitis
- `STDModel` → Sexually Transmitted Diseases
- `LeadModel` → Lead exposure
- `ids_case` → Case management
- `ids_contactpoint` → Contact management
- `ids_investigation` → Investigation
- `ids_investigationresult` → Investigation results
- `ids_investigationresultattr` → Investigation result attributes
- `ids_party` → Parties/People

---

## Next Steps for Workbench Integration

1. **Install Python** (if not already done)
2. **Run the parser** on your FieldMetadata.csv and ValueMetadata.csv
3. **Import the JSON output** into your workbench application
4. **Map question_id** to your internal question identifiers (or use the HI_* IDs directly)
5. **Populate dropdown options** from the value_options array
6. **Associate questions with pages** using the source_table mapping as a guide
