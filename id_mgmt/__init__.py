"""
ID Management Package

This package provides ID generation and management functionality for different types of IDs:
- FID (Facility ID)
- OID (Outlet ID) 
- TID (Terminal ID)

Main Components:
- ID managers for generating different types of IDs
- Models for storing ID information in database
- Enums for ID types and statuses
"""

# Import models and enums
from .models import (
    IdType,
    IdStatus,
    ID,
    Base,
    session,
)

# Import ID managers
from .id_manager import (
    IdManager,
    FidManager,
    OidManager,
    TidManager
)

# Define what gets imported with "from id_mgmt import *"
__all__ = [
    # Enums
    'IdType',
    'IdStatus',
    
    # Models
    'ID',
    'Base',
    'session',
    
    # Managers
    'IdManager',
    'FidManager',
    'OidManager',
    'TidManager',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Romen Law'
__description__ = 'A package for generating and managing different types of MeMo IDs'
