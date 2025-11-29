# External Application Modules
# This package contains modules for handling external job applications

from .ats_detector import detect_ats_platform, is_supported_ats
from .stealth_setup import apply_stealth
from .captcha_detector import detect_captcha, should_skip_captcha_site
from .external_links_manager import ExternalLinksManager
from .field_knowledge_base import FieldKnowledgeBase
from .greenhouse_handler import is_greenhouse_site, fill_greenhouse_application

__all__ = [
    'detect_ats_platform',
    'is_supported_ats',
    'apply_stealth',
    'detect_captcha',
    'should_skip_captcha_site',
    'ExternalLinksManager',
    'FieldKnowledgeBase',
    'is_greenhouse_site',
    'fill_greenhouse_application'
]
