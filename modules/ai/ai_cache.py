'''
AI Response Cache Module
Caches AI responses to save API calls and improve performance.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Any, Dict
from modules.helpers import print_lg, make_directories

CACHE_DIR = "logs/ai_cache/"
CACHE_FILE = os.path.join(CACHE_DIR, "ai_responses.json")


def _get_cache_key(question: str, context: str = "") -> str:
    '''Generate a unique cache key for a question and context.'''
    combined = f"{question.lower().strip()}|{context.lower().strip()}"
    return hashlib.md5(combined.encode()).hexdigest()


def get_cached_response(question: str, context: str = "", max_age_days: int = 7) -> Any | None:
    '''
    Retrieve a cached AI response if available and not expired.
    * `question` - The question asked
    * `context` - Additional context (job description, etc.)
    * `max_age_days` - Maximum age of cache entry in days
    * Returns cached response or None
    '''
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        cache_key = _get_cache_key(question, context)
        
        if cache_key in cache:
            entry = cache[cache_key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            age = datetime.now() - cached_time
            
            if age.days <= max_age_days:
                print_lg(f"Using cached AI response (age: {age.days} days)")
                return entry['response']
            else:
                print_lg(f"Cached response expired (age: {age.days} days)")
        
        return None
    except Exception as e:
        print_lg(f"Failed to retrieve cached response: {e}")
        return None


def cache_response(question: str, response: Any, context: str = "") -> bool:
    '''
    Cache an AI response for future use.
    * `question` - The question asked
    * `response` - The AI response
    * `context` - Additional context
    * Returns True if successful
    '''
    try:
        make_directories([CACHE_FILE])
        
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        
        cache_key = _get_cache_key(question, context)
        cache[cache_key] = {
            'question': question,
            'response': response,
            'context_hash': hashlib.md5(context.encode()).hexdigest()[:16],
            'timestamp': datetime.now().isoformat()
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
        
        return True
    except Exception as e:
        print_lg(f"Failed to cache response: {e}")
        return False


def clear_old_cache(max_age_days: int = 30) -> int:
    '''
    Clear cache entries older than specified days.
    * `max_age_days` - Maximum age to keep
    * Returns number of entries removed
    '''
    try:
        if not os.path.exists(CACHE_FILE):
            return 0
        
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        original_count = len(cache)
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        cache = {
            k: v for k, v in cache.items()
            if datetime.fromisoformat(v['timestamp']) > cutoff_date
        }
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
        
        removed = original_count - len(cache)
        if removed > 0:
            print_lg(f"Cleared {removed} old cache entries")
        
        return removed
    except Exception as e:
        print_lg(f"Failed to clear old cache: {e}")
        return 0


def get_cache_stats() -> Dict[str, Any]:
    '''Get statistics about the cache.'''
    try:
        if not os.path.exists(CACHE_FILE):
            return {'total_entries': 0, 'oldest_entry': None, 'newest_entry': None}
        
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        
        if not cache:
            return {'total_entries': 0, 'oldest_entry': None, 'newest_entry': None}
        
        timestamps = [datetime.fromisoformat(v['timestamp']) for v in cache.values()]
        
        return {
            'total_entries': len(cache),
            'oldest_entry': min(timestamps).isoformat(),
            'newest_entry': max(timestamps).isoformat()
        }
    except Exception as e:
        print_lg(f"Failed to get cache stats: {e}")
        return {'total_entries': 0, 'error': str(e)}
