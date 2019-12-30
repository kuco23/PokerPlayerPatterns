"""
╔═══════════════════════════════════════════╗
║                                           ║
║   Standard tools for simplifying the      ║
║   parsing process of poker stream-like    ║
║   output provided by the poker dataset    ║
║   .txt file                               ║
║                                           ║
╚═══════════════════════════════════════════╝ 
"""

from ._enums import OutId, ActionId, TurnId
from . import _stream_patterns as patterns
from . import _stream_parser as parser
