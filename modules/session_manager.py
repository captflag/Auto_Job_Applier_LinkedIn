'''
Session Manager Module
Handles session recovery and checkpoint management.

Author:     Enhanced by AI Assistant
License:    GNU Affero General Public License
'''

import json
import os
from datetime import datetime
from typing import Dict, Any
from modules.helpers import print_lg, make_directories

CHECKPOINT_FILE = "logs/session_checkpoint.json"


def save_checkpoint(data: Dict[str, Any]) -> bool:
    '''
    Save current session state to checkpoint file.
    * `data` - Dictionary containing session state
    * Returns True if successful, False otherwise
    '''
    try:
        make_directories([CHECKPOINT_FILE])
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
        print_lg(f"Checkpoint saved at {checkpoint['timestamp']}")
        return True
    except Exception as e:
        print_lg(f"Failed to save checkpoint: {e}")
        return False


def load_checkpoint() -> Dict[str, Any] | None:
    '''
    Load session state from checkpoint file.
    * Returns checkpoint data dictionary or None if not found
    '''
    try:
        if not os.path.exists(CHECKPOINT_FILE):
            print_lg("No checkpoint file found.")
            return None
        
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        print_lg(f"Checkpoint loaded from {checkpoint.get('timestamp', 'unknown time')}")
        return checkpoint.get('data')
    except Exception as e:
        print_lg(f"Failed to load checkpoint: {e}")
        return None


def clear_checkpoint() -> bool:
    '''
    Delete checkpoint file after successful completion.
    * Returns True if successful, False otherwise
    '''
    try:
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)
            print_lg("Checkpoint cleared.")
        return True
    except Exception as e:
        print_lg(f"Failed to clear checkpoint: {e}")
        return False


def should_resume() -> bool:
    '''
    Check if there's a valid checkpoint to resume from.
    * Returns True if checkpoint exists and is recent
    '''
    try:
        if not os.path.exists(CHECKPOINT_FILE):
            return False
        
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        # Check if checkpoint is less than 24 hours old
        timestamp_str = checkpoint.get('timestamp')
        if timestamp_str:
            checkpoint_time = datetime.fromisoformat(timestamp_str)
            age_hours = (datetime.now() - checkpoint_time).total_seconds() / 3600
            return age_hours < 24
        
        return False
    except:
        return False
