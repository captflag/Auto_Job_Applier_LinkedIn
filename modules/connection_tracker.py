'''
Connection Request Tracker Module

Tracks LinkedIn connection requests to avoid spam detection and respect platform limits.
'''

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random
import time


class ConnectionTracker:
    def __init__(self, tracker_file: str = "logs/connection_requests.json", daily_limit: int = 12):
        """
        Initialize the connection tracker.
        
        Args:
            tracker_file: Path to the JSON file storing connection data
            daily_limit: Maximum connection requests per day
        """
        self.tracker_file = tracker_file
        self.daily_limit = daily_limit
        self.data = self._load_data()
        self.last_request_time = None
        
    def _load_data(self) -> Dict:
        """Load connection request data from file."""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"requests": [], "connected_profiles": []}
        return {"requests": [], "connected_profiles": []}
    
    def _save_data(self) -> None:
        """Save connection request data to file."""
        os.makedirs(os.path.dirname(self.tracker_file), exist_ok=True)
        with open(self.tracker_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get_today_count(self) -> int:
        """Get the number of connection requests sent today."""
        today = datetime.now().date().isoformat()
        return sum(1 for req in self.data["requests"] if req.get("date", "").startswith(today))
    
    def can_send_request(self) -> Tuple[bool, str]:
        """
        Check if a connection request can be sent.
        
        Returns:
            Tuple of (can_send, reason)
        """
        today_count = self.get_today_count()
        
        if today_count >= self.daily_limit:
            return False, f"Daily limit reached ({today_count}/{self.daily_limit})"
        
        # Check if we need to wait (rate limiting)
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            min_wait = 120  # 2 minutes minimum between requests
            if elapsed < min_wait:
                wait_time = int(min_wait - elapsed)
                return False, f"Rate limit: wait {wait_time}s"
        
        return True, "OK"
    
    def is_already_connected(self, hr_link: str) -> bool:
        """Check if already connected to this profile."""
        return hr_link in self.data.get("connected_profiles", [])
    
    def add_connected_profile(self, hr_link: str) -> None:
        """Add a profile to the connected list."""
        if "connected_profiles" not in self.data:
            self.data["connected_profiles"] = []
        if hr_link not in self.data["connected_profiles"]:
            self.data["connected_profiles"].append(hr_link)
            self._save_data()
    
    def record_request(self, hr_name: str, hr_link: str, job_title: str, company: str, success: bool, message: str = "") -> None:
        """
        Record a connection request.
        
        Args:
            hr_name: Name of the HR person
            hr_link: LinkedIn profile URL
            job_title: Job title
            company: Company name
            success: Whether the request was successful
            message: Optional message or error details
        """
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "hr_name": hr_name,
            "hr_link": hr_link,
            "job_title": job_title,
            "company": company,
            "success": success,
            "message": message
        }
        
        self.data["requests"].append(request_data)
        self.last_request_time = time.time()
        
        if success:
            self.add_connected_profile(hr_link)
        
        self._save_data()
    
    def get_random_delay(self) -> int:
        """Get a random delay between connection requests (2-5 minutes)."""
        return random.randint(120, 300)
    
    def wait_if_needed(self) -> None:
        """Wait if rate limiting is needed."""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            min_wait = 120  # 2 minutes
            if elapsed < min_wait:
                wait_time = min_wait - elapsed
                print(f"Rate limiting: waiting {int(wait_time)}s before next connection request...")
                time.sleep(wait_time)
    
    def cleanup_old_requests(self, days: int = 30) -> None:
        """Remove connection requests older than specified days."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        self.data["requests"] = [
            req for req in self.data["requests"]
            if req.get("timestamp", "") >= cutoff_date
        ]
        self._save_data()
    
    def get_stats(self) -> Dict:
        """Get connection request statistics."""
        today_count = self.get_today_count()
        total_count = len(self.data["requests"])
        success_count = sum(1 for req in self.data["requests"] if req.get("success", False))
        
        return {
            "today": today_count,
            "total": total_count,
            "successful": success_count,
            "success_rate": f"{(success_count/total_count*100):.1f}%" if total_count > 0 else "0%",
            "remaining_today": max(0, self.daily_limit - today_count)
        }
