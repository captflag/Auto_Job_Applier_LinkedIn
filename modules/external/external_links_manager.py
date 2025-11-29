'''
External Links Manager
Manages collection of external application links for manual completion.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import csv
from datetime import datetime
from typing import Dict
from modules.helpers import print_lg, make_directories, truncate_for_csv


class ExternalLinksManager:
    '''
    Manages external application links that need manual completion.
    '''
    
    def __init__(self, links_file: str = "all excels/external_application_links.csv"):
        self.links_file = links_file
        make_directories([links_file])
    
    def save_external_link(
        self,
        job_id: str,
        job_title: str,
        company: str,
        external_url: str,
        ats_platform: str,
        reason: str = "Auto-fill failed"
    ) -> None:
        '''
        Save external application link for manual completion.
        '''
        try:
            file_exists = False
            try:
                with open(self.links_file, 'r'):
                    file_exists = True
            except FileNotFoundError:
                pass
            
            with open(self.links_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'Job ID', 'Job Title', 'Company', 'External URL',
                    'ATS Platform', 'Reason', 'Date Saved'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'Job ID': truncate_for_csv(job_id),
                    'Job Title': truncate_for_csv(job_title),
                    'Company': truncate_for_csv(company),
                    'External URL': truncate_for_csv(external_url),
                    'ATS Platform': truncate_for_csv(ats_platform),
                    'Reason': truncate_for_csv(reason),
                    'Date Saved': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            print_lg(f"Saved external link for manual application: {company} - {job_title}")
            print_lg(f"URL: {external_url}")
            
        except Exception as e:
            print_lg(f"Failed to save external link: {e}")
    
    def get_saved_links_count(self) -> int:
        '''
        Get count of saved external links.
        '''
        try:
            with open(self.links_file, 'r', encoding='utf-8') as f:
                return sum(1 for line in f) - 1  # Subtract header
        except FileNotFoundError:
            return 0
        except Exception as e:
            print_lg(f"Error counting saved links: {e}")
            return 0
