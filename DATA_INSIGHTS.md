# HI Maven Data Insights & Analysis

**Generated:** 2026-04-09  
**Database:** ihi-hi on noog-tsql01\bdp_nbs_demo01

---

## Data Type Distribution

| DataType | Count | % | Purpose |
|----------|-------|---|---------|
| **String** | 3,160 | 41.1% | Open text fields, names, descriptions |
| **Selection** | 1,950 | 25.4% | Single-select dropdowns, standard options |
| **ReferenceCode** | 850 | 11.1% | References to hierarchical code sets |
| **Date** | 747 | 9.7% | Date fields |
| **Number** | 315 | 4.1% | Numeric values |
| **Selection [Multiple]** | 190 | 2.5% | Multi-select dropdowns (checkboxes/lists) |
| **TextArea** | 125 | 1.6% | Long text fields, notes |
| **Party** | 98 | 1.3% | People/contact references |
| **Text** | 72 | 0.9% | Short text |
| **Integer** | 30 | 0.4% | Whole numbers |
| **Case** | 28 | 0.4% | Case references |
| **User** | 20 | 0.3% | User/staff references |
| **Other** | 38 | 0.5% | DateTime, Time, Boolean, DynamicList, etc. |

**Migration Insight:** Most fields (41%) are open text — limited validation enforcement. Multi-select fields (190) will need special UI handling in workbench.

---

## Source Table Breakdown

| Table | Fields | With ValueSet | % |
|-------|--------|---|---|
| **GeneralModel** | 3,834 | 1,625 | 50% |
| **STDModel** | 2,268 | 862 | 30% |
| **HepModel** | 882 | 296 | 11% |
| **LeadModel** | 566 | 266 | 7% |
| **ids_contactpoint** | 40 | 0 | — |
| **ids_case** | 32 | 0 | — |
| **ids_party** | 32 | 0 | — |
| **ids_investigation** | 16 | 0 | — |
| **ids_investigationresult** | 14 | 0 | — |
| **ids_investigationresultattr** | 8 | 0 | — |

**Key Insight:** GeneralModel is 50% of fields. STDModel adds 30%. These two tables dominate migration scope. The `ids_*` infrastructure tables have NO value sets — they're structural/relational only.

---

## Largest Value Sets (Top 15)

| ValueSet | Codes | Purpose |
|----------|-------|---------|
| **ICD-9** | 108,720 | Disease/diagnosis codes (MANDATORY for all disease investigations) |
| **CS_COUNTIES** | 26,304 | Hawaii county codes (geography) |
| **CITIES** | 12,482 | Hawaii city codes (geography) |
| **CS_RACE_AMERICAN_INDIAN_DETAIL** | 980 | Race/ethnicity detail codes |
| **Pangolin lineage** | 712 | COVID-19 lineage classification |
| **CS_LAB_TEST_UNIT** | 545 | Lab measurement units |
| **CS_LAB_SPECIMEN_SOURCE** | 398 | Lab specimen types |
| **CS_VACCINE** | 396 | Vaccine names/types |
| **CS_LAB_TEST_METHOD** | 291 | Lab test methodologies |
| **CS_VACCINE_MANUFACTURER** | 264 | Vaccine manufacturers |
| **CS_IMMUNO_CONDITION** | 249 | Immunocompromised conditions |
| **CS_TRANSPLANT_ORGAN** | 247 | Organ transplant types |
| **CS_OCCUPATION** | 4,170 | Occupations (U.S. standard) |
| **DISEASE** | 2,238+ | Disease list (reference) |
| **Various CS_*** codes** | ~500 each | Disease-investigation-specific |

**Migration Insight:** ICD-9 is massive (108k codes) — this will be your largest join. Geographic/race/vaccine codes are Hawaii-specific standards. Most value sets < 500 codes.

---

## ReferenceCode Field Types

Many fields use **ReferenceCode** data type with bracketed value set names:
- `ReferenceCode [MN_LPH_AGENCIES]` — Agencies (6 fields)
- `ReferenceCode [HEP_NUMBER_SEX_PARTNERS]` — Hepatitis partners (5 fields)
- `ReferenceCode [HAWAII_ISLANDS]` — Islands (3 fields)
- `ReferenceCode [CS_COUNTIES]` — Counties (3 fields)
- `ReferenceCode [CONTACT_TYPE]` — Contact types (2 fields)
- Plus 30+ other ReferenceCode subtypes

**Strategy:** These are essentially value sets with special handling. In your parser, can treat `ReferenceCode [VALUESET]` like `Selection [VALUESET]`.

---

## Special Field Types (Non-Text/Selection)

### Party (98 fields)
Fields like: ContactInfo, PersonID, StaffAssignee, etc.
- **Migration Impact:** These reference Party table (probably needs JOIN on ids_party)
- **Example:** Investigation agent would link Party → investigator
- **Action:** May need special handling in migration (foreign key references)

### Case (28 fields)
Case-related references (probably CaseID links)
- **Similar to Party:** These are relational/structural fields
- **Action:** Map to case ID patterns in your workbench

### User (20 fields)
User/staff references (UserID, CreatedBy, etc.)
- **Action:** Link to staff/user directories

### DynamicList (5 fields)
Database-driven lists that change (probably based on context)
- **Action:** Mark as dynamic in parser (value sets may vary by investigation type)

---

## Quick Wins for Parser Development

### 1. Filter by Data Type
```python
# Get fields that need special handling
string_fields = df[df['DataType'] == 'String']  # 41% of fields
selection_fields = df[df['DataType'].isin(['Selection', 'Selection [Multiple]'])]  # 28%
reference_fields = df[df['DataType'].str.contains('ReferenceCode')]  # 11%
party_fields = df[df['DataType'] == 'Party']  # for relationship mapping
date_fields = df[df['DataType'].isin(['Date', 'DateTime'])]  # 10%
```

### 2. Multi-Select Fields (190 total)
Extract these separately for UI/validation logic:
```python
multi_select = df[df['DataType'] == 'Selection [Multiple]']
```

### 3. Value Set Coverage By Module
```python
general_with_values = 1625 / 3834  # 42% of GeneralModel has value sets
std_with_values = 862 / 2268       # 38% of STDModel has value sets
hep_with_values = 296 / 882        # 34% of HepModel has value sets
lead_with_values = 266 / 566       # 47% of LeadModel has value sets
```

### 4. ReferenceCode Pattern Extraction
```python
# Extract reference code subtypes from DataType column
ref_codes = df[df['DataType'].str.contains('ReferenceCode')]['DataType'].unique()
# Returns: ReferenceCode [NAME], ReferenceCode [NAME], ...
```

---

## What's Missing (For Phase 2)

These insights **confirm** the schema discovery findings. Form structure metadata NOT in ihi-hi:

- ❌ Repeating blocks (group fields in sections)
- ❌ Display order (field sequence)
- ❌ Question packages (CLINICAL/ADMIN/DEMO scopes)
- ❌ Required/enabled/displayed flags
- ❌ Tooltip/help text

But the **field & value set foundation is complete** (7,692 fields, 171,671 codes, 23 data types).

---

## Recommendations

### For Immediate Migration
1. ✅ Use FieldMetadata.csv + ValueMetadata.csv as-is
2. ✅ Filter by SourceTable in parser (GeneralModel → STDModel → HepModel → LeadModel progression)
3. ✅ Handle Selection [Multiple] separately in UI layer
4. ✅ Map Party/Case/User types to your staff/case ID systems
5. ✅ Note: 41% of fields are open String (minimal validation from Maven)

### For Future Phase 2
- Ask Page about **repeating block structure** (how groups nest)
- Get **display order** (sequence within pages)
- Find **question packages** (CLINICAL/ADMIN split)
- Extract **mandatory/enabled/visible flags**

### Performance Notes
- ICD-9 (108k codes) will be your largest JOIN
- Geographic data (26k counties + 12k cities) useful for Hawaii testing
- Most value sets < 500 codes (fast to load)
- Split CSV export approach works well (no timeout on 171k codes)

