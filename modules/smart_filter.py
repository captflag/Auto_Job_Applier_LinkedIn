'''
Smart Job Filter Module

Filters jobs based on various criteria to improve application success rate.
'''

import json
import os
from typing import Dict, List, Set
from datetime import datetime, timedelta


class SmartFilter:
    def __init__(self, 
                 viewed_jobs_file: str = "logs/viewed_jobs.json",
                 rejected_companies_file: str = "logs/rejected_companies.json"):
        """
        Initialize smart filter.
        
        Args:
            viewed_jobs_file: File to track viewed but not applied jobs
            rejected_companies_file: File to track companies that rejected applications
        """
        self.viewed_jobs_file = viewed_jobs_file
        self.rejected_companies_file = rejected_companies_file
        self.viewed_jobs = self._load_viewed_jobs()
        self.rejected_companies = self._load_rejected_companies()
    
    def _load_viewed_jobs(self) -> Set[str]:
        """Load viewed job IDs from file."""
        if os.path.exists(self.viewed_jobs_file):
            try:
                with open(self.viewed_jobs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get("viewed_job_ids", []))
            except:
                return set()
        return set()
    
    def _load_rejected_companies(self) -> Dict:
        """Load rejected companies data from file."""
        if os.path.exists(self.rejected_companies_file):
            try:
                with open(self.rejected_companies_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"companies": {}}
        return {"companies": {}}
    
    def _save_viewed_jobs(self) -> None:
        """Save viewed jobs to file."""
        os.makedirs(os.path.dirname(self.viewed_jobs_file), exist_ok=True)
        with open(self.viewed_jobs_file, 'w', encoding='utf-8') as f:
            json.dump({"viewed_job_ids": list(self.viewed_jobs)}, f, indent=2)
    
    def _save_rejected_companies(self) -> None:
        """Save rejected companies to file."""
        os.makedirs(os.path.dirname(self.rejected_companies_file), exist_ok=True)
        with open(self.rejected_companies_file, 'w', encoding='utf-8') as f:
            json.dump(self.rejected_companies, f, indent=2, ensure_ascii=False)
    
    def mark_as_viewed(self, job_id: str) -> None:
        """Mark a job as viewed."""
        self.viewed_jobs.add(job_id)
        self._save_viewed_jobs()
    
    def is_viewed(self, job_id: str) -> bool:
        """Check if job was already viewed."""
        return job_id in self.viewed_jobs
    
    def add_rejected_company(self, company: str, reason: str = "Rejected application") -> None:
        """
        Add a company to the rejected list.
        
        Args:
            company: Company name
            reason: Reason for rejection
        """
        if "companies" not in self.rejected_companies:
            self.rejected_companies["companies"] = {}
        
        if company not in self.rejected_companies["companies"]:
            self.rejected_companies["companies"][company] = {
                "first_rejection": datetime.now().isoformat(),
                "rejection_count": 0,
                "reasons": []
            }
        
        self.rejected_companies["companies"][company]["rejection_count"] += 1
        self.rejected_companies["companies"][company]["last_rejection"] = datetime.now().isoformat()
        if reason not in self.rejected_companies["companies"][company]["reasons"]:
            self.rejected_companies["companies"][company]["reasons"].append(reason)
        
        self._save_rejected_companies()
    
    def should_skip_company(self, company: str, rejection_threshold: int = 2) -> bool:
        """
        Check if company should be skipped based on rejection history.
        
        Args:
            company: Company name
            rejection_threshold: Number of rejections before skipping
        
        Returns:
            True if company should be skipped
        """
        if company in self.rejected_companies.get("companies", {}):
            rejection_count = self.rejected_companies["companies"][company].get("rejection_count", 0)
            return rejection_count >= rejection_threshold
        return False
    
    def calculate_job_priority(self, 
                              applicant_count: int = None,
                              days_posted: int = None,
                              is_easy_apply: bool = True,
                              company_rejection_count: int = 0) -> float:
        """
        Calculate job priority score (higher is better).
        
        Args:
            applicant_count: Number of applicants
            days_posted: Days since job was posted
            is_easy_apply: Whether job has easy apply
            company_rejection_count: Number of times company rejected applications
        
        Returns:
            Priority score (0-100)
        """
        score = 50.0  # Base score
        
        # Fewer applicants = higher priority
        if applicant_count is not None:
            if applicant_count < 10:
                score += 20
            elif applicant_count < 50:
                score += 10
            elif applicant_count > 200:
                score -= 20
        
        # Newer jobs = higher priority
        if days_posted is not None:
            if days_posted == 0:
                score += 15
            elif days_posted <= 2:
                score += 10
            elif days_posted <= 7:
                score += 5
            elif days_posted > 30:
                score -= 10
        
        # Easy apply = higher priority
        if is_easy_apply:
            score += 10
        
        # Companies that rejected before = lower priority
        score -= (company_rejection_count * 5)
        
        return max(0, min(100, score))
    
    def extract_applicant_count(self, applicant_text: str) -> int:
        """
        Extract applicant count from text like "50 applicants" or "Over 100 applicants".
        
        Args:
            applicant_text: Text containing applicant count
        
        Returns:
            Estimated applicant count
        """
        try:
            import re
            # Handle "Over X applicants"
            if "over" in applicant_text.lower():
                match = re.search(r'over\s+(\d+)', applicant_text.lower())
                if match:
                    return int(match.group(1)) + 50  # Add buffer for "over"
            
            # Handle "X applicants"
            match = re.search(r'(\d+)\s+applicant', applicant_text.lower())
            if match:
                return int(match.group(1))
            
            # Handle "Be in the first X applicants"
            if "first" in applicant_text.lower():
                match = re.search(r'first\s+(\d+)', applicant_text.lower())
                if match:
                    return int(match.group(1)) // 2  # Estimate half have applied
        except:
            pass
        
        return None
    
    def cleanup_old_data(self, days: int = 90) -> None:
        """Remove old viewed jobs and rejection data."""
        # For viewed jobs, we can clear all after certain days
        # since job postings expire
        if days > 0:
            self.viewed_jobs.clear()
            self._save_viewed_jobs()
