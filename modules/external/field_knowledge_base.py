'''
Field Knowledge Base
Learning system that improves field detection over time.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import json
import os
from typing import Dict, Any
from modules.helpers import print_lg, make_directories


class FieldKnowledgeBase:
    '''
    Stores and retrieves successful field mappings to improve accuracy over time.
    '''
    
    def __init__(self, kb_file: str = "logs/field_knowledge_base.json"):
        self.kb_file = kb_file
        make_directories([kb_file])
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self) -> Dict[str, Any]:
        '''Load knowledge base from file.'''
        try:
            if os.path.exists(self.kb_file):
                with open(self.kb_file, 'r', encoding='utf-8') as f:
                    kb = json.load(f)
                print_lg(f"Loaded knowledge base with {len(kb.get('field_mappings', {}))} field mappings")
                return kb
        except Exception as e:
            print_lg(f"Failed to load knowledge base: {e}")
        
        return {
            'field_mappings': {},
            'successful_patterns': {},
            'ats_specific_mappings': {}
        }
    
    def _save_knowledge(self) -> None:
        '''Save knowledge base to file.'''
        try:
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, indent=2)
        except Exception as e:
            print_lg(f"Failed to save knowledge base: {e}")
    
    def learn_field_mapping(
        self,
        field_identifier: str,
        field_type: str,
        ats_platform: str = "unknown"
    ) -> None:
        '''
        Store a successful field mapping.
        * field_identifier - name, id, or label of the field
        * field_type - what the field represents (e.g., 'first_name', 'email')
        * ats_platform - which ATS platform this is from
        '''
        try:
            # Store general mapping
            if field_identifier not in self.knowledge['field_mappings']:
                self.knowledge['field_mappings'][field_identifier] = {}
            
            # Increment count for this mapping
            if field_type not in self.knowledge['field_mappings'][field_identifier]:
                self.knowledge['field_mappings'][field_identifier][field_type] = 0
            
            self.knowledge['field_mappings'][field_identifier][field_type] += 1
            
            # Store ATS-specific mapping
            if ats_platform != "unknown":
                if ats_platform not in self.knowledge['ats_specific_mappings']:
                    self.knowledge['ats_specific_mappings'][ats_platform] = {}
                
                if field_identifier not in self.knowledge['ats_specific_mappings'][ats_platform]:
                    self.knowledge['ats_specific_mappings'][ats_platform][field_identifier] = field_type
            
            self._save_knowledge()
            print_lg(f"Learned: {field_identifier} → {field_type} ({ats_platform})")
            
        except Exception as e:
            print_lg(f"Failed to learn field mapping: {e}")
    
    def get_field_type(self, field_identifier: str, ats_platform: str = "unknown") -> str | None:
        '''
        Get the most likely field type for a given identifier.
        * Returns: field type or None if unknown
        '''
        try:
            # Check ATS-specific mapping first
            if ats_platform != "unknown" and ats_platform in self.knowledge['ats_specific_mappings']:
                if field_identifier in self.knowledge['ats_specific_mappings'][ats_platform]:
                    return self.knowledge['ats_specific_mappings'][ats_platform][field_identifier]
            
            # Check general mappings
            if field_identifier in self.knowledge['field_mappings']:
                mappings = self.knowledge['field_mappings'][field_identifier]
                # Return the most common mapping
                if mappings:
                    return max(mappings, key=mappings.get)
            
            return None
            
        except Exception as e:
            print_lg(f"Error retrieving field type: {e}")
            return None
    
    def get_stats(self) -> Dict[str, int]:
        '''Get statistics about the knowledge base.'''
        return {
            'total_field_mappings': len(self.knowledge['field_mappings']),
            'ats_platforms_learned': len(self.knowledge['ats_specific_mappings']),
            'total_patterns': len(self.knowledge['successful_patterns'])
        }
