'''
Analytics Module

Tracks application success rates and generates insights.
'''

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict


class Analytics:
    def __init__(self, metrics_file: str = "logs/success_metrics.json"):
        """
        Initialize analytics tracker.
        
        Args:
            metrics_file: Path to metrics JSON file
        """
        self.metrics_file = metrics_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load metrics data from file."""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._init_data_structure()
        return self._init_data_structure()
    
    def _init_data_structure(self) -> Dict:
        """Initialize empty data structure."""
        return {
            "applications": [],
            "daily_stats": {},
            "ats_stats": {},
            "company_stats": {},
            "time_filter_stats": {}
        }
    
    def _save_data(self) -> None:
        """Save metrics data to file."""
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def record_application(self, 
                          job_id: str,
                          job_title: str,
                          company: str,
                          application_type: str,  # "easy_apply" or "external"
                          ats_platform: str = None,
                          success: bool = True,
                          time_filter: str = None,
                          applicant_count: int = None,
                          days_posted: int = None) -> None:
        """
        Record an application attempt.
        
        Args:
            job_id: Job ID
            job_title: Job title
            company: Company name
            application_type: Type of application
            ats_platform: ATS platform (for external apps)
            success: Whether application was successful
            time_filter: Time filter used (r600, r3600, etc.)
            applicant_count: Number of applicants
            days_posted: Days since job was posted
        """
        application_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "job_id": job_id,
            "job_title": job_title,
            "company": company,
            "application_type": application_type,
            "ats_platform": ats_platform,
            "success": success,
            "time_filter": time_filter,
            "applicant_count": applicant_count,
            "days_posted": days_posted
        }
        
        self.data["applications"].append(application_data)
        self._update_stats(application_data)
        self._save_data()
    
    def _update_stats(self, app_data: Dict) -> None:
        """Update aggregated statistics."""
        date = app_data["date"]
        
        # Daily stats
        if date not in self.data["daily_stats"]:
            self.data["daily_stats"][date] = {"total": 0, "successful": 0, "failed": 0}
        
        self.data["daily_stats"][date]["total"] += 1
        if app_data["success"]:
            self.data["daily_stats"][date]["successful"] += 1
        else:
            self.data["daily_stats"][date]["failed"] += 1
        
        # ATS stats
        if app_data["ats_platform"]:
            ats = app_data["ats_platform"]
            if ats not in self.data["ats_stats"]:
                self.data["ats_stats"][ats] = {"total": 0, "successful": 0, "failed": 0}
            
            self.data["ats_stats"][ats]["total"] += 1
            if app_data["success"]:
                self.data["ats_stats"][ats]["successful"] += 1
            else:
                self.data["ats_stats"][ats]["failed"] += 1
        
        # Company stats
        company = app_data["company"]
        if company not in self.data["company_stats"]:
            self.data["company_stats"][company] = {"total": 0, "successful": 0, "failed": 0}
        
        self.data["company_stats"][company]["total"] += 1
        if app_data["success"]:
            self.data["company_stats"][company]["successful"] += 1
        else:
            self.data["company_stats"][company]["failed"] += 1
        
        # Time filter stats
        if app_data["time_filter"]:
            tf = app_data["time_filter"]
            if tf not in self.data["time_filter_stats"]:
                self.data["time_filter_stats"][tf] = {"total": 0, "successful": 0, "failed": 0}
            
            self.data["time_filter_stats"][tf]["total"] += 1
            if app_data["success"]:
                self.data["time_filter_stats"][tf]["successful"] += 1
            else:
                self.data["time_filter_stats"][tf]["failed"] += 1
    
    def get_success_rate(self, category: str = "overall", key: str = None) -> float:
        """
        Get success rate for a category.
        
        Args:
            category: "overall", "ats", "company", "time_filter", "daily"
            key: Specific key within category (e.g., ATS name)
        
        Returns:
            Success rate as percentage
        """
        if category == "overall":
            total = len(self.data["applications"])
            successful = sum(1 for app in self.data["applications"] if app["success"])
            return (successful / total * 100) if total > 0 else 0
        
        elif category == "ats" and key:
            stats = self.data["ats_stats"].get(key, {})
            total = stats.get("total", 0)
            successful = stats.get("successful", 0)
            return (successful / total * 100) if total > 0 else 0
        
        elif category == "company" and key:
            stats = self.data["company_stats"].get(key, {})
            total = stats.get("total", 0)
            successful = stats.get("successful", 0)
            return (successful / total * 100) if total > 0 else 0
        
        elif category == "time_filter" and key:
            stats = self.data["time_filter_stats"].get(key, {})
            total = stats.get("total", 0)
            successful = stats.get("successful", 0)
            return (successful / total * 100) if total > 0 else 0
        
        return 0
    
    def get_summary(self, days: int = 7) -> Dict:
        """
        Get summary statistics for the last N days.
        
        Args:
            days: Number of days to include
        
        Returns:
            Summary dictionary
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        recent_apps = [app for app in self.data["applications"] if app["date"] >= cutoff_date]
        
        total = len(recent_apps)
        successful = sum(1 for app in recent_apps if app["success"])
        failed = total - successful
        
        easy_apply = sum(1 for app in recent_apps if app["application_type"] == "easy_apply")
        external = sum(1 for app in recent_apps if app["application_type"] == "external")
        
        return {
            "period_days": days,
            "total_applications": total,
            "successful": successful,
            "failed": failed,
            "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
            "easy_apply_count": easy_apply,
            "external_count": external,
            "avg_per_day": f"{total/days:.1f}" if days > 0 else "0"
        }
    
    def get_best_time_filter(self) -> str:
        """Get the time filter with the best success rate."""
        best_filter = None
        best_rate = 0
        
        for tf, stats in self.data["time_filter_stats"].items():
            total = stats.get("total", 0)
            if total >= 5:  # Minimum sample size
                rate = self.get_success_rate("time_filter", tf)
                if rate > best_rate:
                    best_rate = rate
                    best_filter = tf
        
        return best_filter or "r600"
    
    def get_top_companies(self, limit: int = 10) -> List[Dict]:
        """Get top companies by application count."""
        companies = []
        for company, stats in self.data["company_stats"].items():
            companies.append({
                "company": company,
                "total": stats["total"],
                "successful": stats["successful"],
                "success_rate": f"{(stats['successful']/stats['total']*100):.1f}%" if stats['total'] > 0 else "0%"
            })
        
        return sorted(companies, key=lambda x: x["total"], reverse=True)[:limit]
