'''
Metrics Tracking Module
Tracks and analyzes bot performance metrics.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import csv
from datetime import datetime
from typing import Dict, Any
from modules.helpers import print_lg, make_directories

class MetricsTracker:
    '''
    Tracks bot performance metrics and statistics.
    '''
    
    def __init__(self, metrics_file: str = "all excels/bot_metrics.csv"):
        self.metrics_file = metrics_file
        self.current_session = {
            'session_start': datetime.now(),
            'applications_submitted': 0,
            'applications_failed': 0,
            'applications_skipped': 0,
            'external_applications': 0,
            'questions_answered_by_ai': 0,
            'questions_answered_randomly': 0,
            'questions_answered_manually': 0,
            'total_time_seconds': 0,
            'errors_encountered': {},
            'jobs_by_company': {},
        }
        make_directories([metrics_file])
    
    def increment(self, metric: str, amount: int = 1) -> None:
        '''Increment a metric counter.'''
        if metric in self.current_session:
            self.current_session[metric] += amount
    
    def record_error(self, error_type: str) -> None:
        '''Record an error occurrence.'''
        errors = self.current_session['errors_encountered']
        errors[error_type] = errors.get(error_type, 0) + 1
    
    def record_company_application(self, company: str) -> None:
        '''Record application to a company.'''
        companies = self.current_session['jobs_by_company']
        companies[company] = companies.get(company, 0) + 1
    
    def get_success_rate(self) -> float:
        '''Calculate application success rate.'''
        total = self.current_session['applications_submitted'] + self.current_session['applications_failed']
        if total == 0:
            return 0.0
        return (self.current_session['applications_submitted'] / total) * 100
    
    def get_average_time_per_application(self) -> float:
        '''Calculate average time per application in seconds.'''
        total_apps = self.current_session['applications_submitted'] + self.current_session['external_applications']
        if total_apps == 0:
            return 0.0
        return self.current_session['total_time_seconds'] / total_apps
    
    def save_session_metrics(self) -> None:
        '''Save current session metrics to CSV file.'''
        try:
            session_end = datetime.now()
            self.current_session['total_time_seconds'] = (session_end - self.current_session['session_start']).total_seconds()
            
            file_exists = False
            try:
                with open(self.metrics_file, 'r'):
                    file_exists = True
            except FileNotFoundError:
                pass
            
            with open(self.metrics_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'session_date', 'session_duration_minutes', 'applications_submitted',
                    'applications_failed', 'applications_skipped', 'external_applications',
                    'success_rate_percent', 'avg_time_per_app_seconds',
                    'ai_answered', 'random_answered', 'manual_answered',
                    'top_error', 'most_applied_company'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                # Find most common error and company
                errors = self.current_session['errors_encountered']
                top_error = max(errors.items(), key=lambda x: x[1])[0] if errors else "None"
                
                companies = self.current_session['jobs_by_company']
                top_company = max(companies.items(), key=lambda x: x[1])[0] if companies else "None"
                
                writer.writerow({
                    'session_date': self.current_session['session_start'].strftime('%Y-%m-%d %H:%M:%S'),
                    'session_duration_minutes': round(self.current_session['total_time_seconds'] / 60, 2),
                    'applications_submitted': self.current_session['applications_submitted'],
                    'applications_failed': self.current_session['applications_failed'],
                    'applications_skipped': self.current_session['applications_skipped'],
                    'external_applications': self.current_session['external_applications'],
                    'success_rate_percent': round(self.get_success_rate(), 2),
                    'avg_time_per_app_seconds': round(self.get_average_time_per_application(), 2),
                    'ai_answered': self.current_session['questions_answered_by_ai'],
                    'random_answered': self.current_session['questions_answered_randomly'],
                    'manual_answered': self.current_session['questions_answered_manually'],
                    'top_error': top_error,
                    'most_applied_company': top_company
                })
            
            print_lg(f"Session metrics saved to {self.metrics_file}")
        except Exception as e:
            print_lg(f"Failed to save metrics: {e}")
    
    def print_summary(self) -> None:
        '''Print session summary to console.'''
        print_lg("\n" + "="*60)
        print_lg("SESSION METRICS SUMMARY")
        print_lg("="*60)
        print_lg(f"Applications Submitted:     {self.current_session['applications_submitted']}")
        print_lg(f"Applications Failed:        {self.current_session['applications_failed']}")
        print_lg(f"Applications Skipped:       {self.current_session['applications_skipped']}")
        print_lg(f"External Applications:      {self.current_session['external_applications']}")
        print_lg(f"Success Rate:               {self.get_success_rate():.2f}%")
        print_lg(f"AI Answered Questions:      {self.current_session['questions_answered_by_ai']}")
        print_lg(f"Randomly Answered:          {self.current_session['questions_answered_randomly']}")
        print_lg(f"Session Duration:           {self.current_session['total_time_seconds']/60:.2f} minutes")
        print_lg("="*60 + "\n")
