"""
HI Maven Metadata CSV Parser

Converts FieldMetadata.csv + ValueMetadata.csv into standardized question objects.

Usage:
    parser = HiMavenParser()
    questions = parser.parse(fields_csv_path, values_csv_path)
"""

import csv
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict


@dataclass
class ValueOption:
    """Represents a single code/value in a dropdown or selection field"""
    code: str
    description: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Question:
    """Standard question/field schema"""
    question_id: str  # Auto-generated from field_name if not found
    field_name: str  # From FieldMetadata.FieldName
    field_label: str  # From FieldMetadata.FieldLabel
    data_type: str  # From FieldMetadata.DataType (Selection, String, Date, etc.)
    source_table: str  # From FieldMetadata.SourceTable (disease/module grouping)
    value_set_name: Optional[str]  # From FieldMetadata.ValueSet
    value_options: List[ValueOption] = field(default_factory=list)  # From ValueMetadata
    
    def to_dict(self):
        return {
            'question_id': self.question_id,
            'field_name': self.field_name,
            'field_label': self.field_label,
            'data_type': self.data_type,
            'source_table': self.source_table,
            'value_set_name': self.value_set_name,
            'value_options': [opt.to_dict() for opt in self.value_options],
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


class HiMavenParser:
    """Parse HI Maven FieldMetadata + ValueMetadata CSVs"""
    
    # Map SourceTable to disease/module groupings for page association
    SOURCE_TABLE_MAPPING = {
        'GeneralModel': 'general',
        'HepModel': 'hepatitis',
        'STDModel': 'std',
        'LeadModel': 'lead',
        'ids_case': 'case_management',
        'ids_contactpoint': 'case_management',
        'ids_investigation': 'case_management',
        'ids_investigationresult': 'case_management',
        'ids_investigationresultattr': 'case_management',
        'ids_party': 'case_management',
    }
    
    def __init__(self):
        self.questions: List[Question] = []
        self.values_by_set: Dict[str, List[ValueOption]] = defaultdict(list)
    
    def parse(self, fields_csv_path: str, values_csv_path: str) -> List[Question]:
        """
        Parse FieldMetadata and ValueMetadata CSVs into Question objects
        
        Args:
            fields_csv_path: Path to FieldMetadata.csv
            values_csv_path: Path to ValueMetadata.csv
        
        Returns:
            List of Question objects with value options populated
        """
        # Step 1: Load all value sets
        self._load_value_sets(values_csv_path)
        
        # Step 2: Load fields and attach value options
        self._load_fields(fields_csv_path)
        
        return self.questions
    
    def _load_value_sets(self, csv_path: str):
        """Load ValueMetadata.csv into memory, grouped by Code_Set"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    code_set = row.get('Code_Set', '').strip()
                    code = row.get('Code', '').strip()
                    description = row.get('Description', '').strip()
                    
                    if code_set and code:
                        self.values_by_set[code_set].append(
                            ValueOption(code=code, description=description)
                        )
            print(f"✓ Loaded {len(self.values_by_set)} value sets from {csv_path}")
        except Exception as e:
            print(f"✗ Error loading value sets: {e}")
            raise
    
    def _load_fields(self, csv_path: str):
        """Load FieldMetadata.csv and create Question objects"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    field_name = row.get('FieldName', '').strip()
                    field_label = row.get('FieldLabel', '').strip()
                    data_type = row.get('DataType', '').strip()
                    source_table = row.get('SourceTable', '').strip()
                    value_set = row.get('ValueSet', '').strip() or None
                    
                    if not field_name:
                        continue
                    
                    # Auto-generate question_id from field_name
                    question_id = self._generate_question_id(field_name)
                    
                    # Get value options if this is a selection field
                    value_options = []
                    if value_set and value_set in self.values_by_set:
                        value_options = self.values_by_set[value_set]
                    
                    question = Question(
                        question_id=question_id,
                        field_name=field_name,
                        field_label=field_label,
                        data_type=data_type,
                        source_table=source_table,
                        value_set_name=value_set,
                        value_options=value_options,
                    )
                    
                    self.questions.append(question)
            
            print(f"✓ Loaded {len(self.questions)} fields from {csv_path}")
        except Exception as e:
            print(f"✗ Error loading fields: {e}")
            raise
    
    @staticmethod
    def _generate_question_id(field_name: str) -> str:
        """Generate question ID from field name (e.g., DISEASE -> HI_DISEASE)"""
        return f"HI_{field_name.upper()}"
    
    def get_by_source_table(self, source_table: str) -> List[Question]:
        """Get all questions from a specific source table (disease/module)"""
        return [q for q in self.questions if q.source_table == source_table]
    
    def get_by_data_type(self, data_type: str) -> List[Question]:
        """Get all questions of a specific data type (Selection, String, etc.)"""
        return [q for q in self.questions if q.data_type == data_type]
    
    def get_dropdown_fields(self) -> List[Question]:
        """Get all Selection/dropdown fields only"""
        return [q for q in self.questions if q.data_type == 'Selection' and q.value_options]
    
    def export_json(self, output_path: str):
        """Export all questions as JSON"""
        data = {
            'metadata': {
                'source': 'HI_Maven',
                'total_fields': len(self.questions),
                'total_value_sets': len(self.values_by_set),
                'source_tables': list(set(q.source_table for q in self.questions)),
            },
            'questions': [q.to_dict() for q in self.questions],
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Exported {len(self.questions)} questions to {output_path}")
    
    def export_csv(self, output_path: str):
        """Export questions as CSV (flattened)"""
        if not self.questions:
            print("✗ No questions to export")
            return
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'question_id', 'field_name', 'field_label', 'data_type',
                'source_table', 'value_set_name', 'value_count'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for q in self.questions:
                writer.writerow({
                    'question_id': q.question_id,
                    'field_name': q.field_name,
                    'field_label': q.field_label,
                    'data_type': q.data_type,
                    'source_table': q.source_table,
                    'value_set_name': q.value_set_name,
                    'value_count': len(q.value_options),
                })
        
        print(f"✓ Exported {len(self.questions)} questions to {output_path}")
    
    def print_summary(self):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("HI MAVEN PARSER SUMMARY")
        print("="*60)
        print(f"Total Fields: {len(self.questions)}")
        print(f"Total Value Sets: {len(self.values_by_set)}")
        print(f"Dropdown Fields: {len(self.get_dropdown_fields())}")
        print(f"String/Text Fields: {len(self.get_by_data_type('String'))}")
        
        print("\nBy Source Table:")
        for source_table in sorted(set(q.source_table for q in self.questions)):
            count = len(self.get_by_source_table(source_table))
            print(f"  {source_table}: {count}")
        
        print("\nBy Data Type:")
        for data_type in sorted(set(q.data_type for q in self.questions)):
            count = len(self.get_by_data_type(data_type))
            print(f"  {data_type}: {count}")
        
        print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    # Example usage
    parser = HiMavenParser()
    
    fields_csv = 'FieldMetadata.csv'
    values_csv = 'ValueMetadata.csv'
    
    print("Parsing HI Maven metadata...")
    questions = parser.parse(fields_csv, values_csv)
    
    # Export to multiple formats
    parser.export_csv('hi_maven_questions.csv')
    parser.export_json('hi_maven_questions.json')
    
    parser.print_summary()
    
    # Example: Get all hepatitis fields
    print("\nExample: First 5 Hepatitis fields:")
    hep_fields = parser.get_by_source_table('HepModel')
    for q in hep_fields[:5]:
        print(f"  {q.field_name}: {q.field_label}")
        if q.value_options:
            print(f"    Values: {len(q.value_options)} options")
