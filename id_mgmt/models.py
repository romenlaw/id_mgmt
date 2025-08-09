from enum import Enum
from sqlalchemy import create_engine, Column, String, DateTime, Text, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

class IdType(Enum):
    FID = "Facility ID"
    OID = "Outlet ID"
    TID = "Terminal ID"

class IdStatus(Enum):
    ALLOCATED = "Allocated"
    CANCELLED = "Cancelled"

# Create custom TypeDecorator for Enum
class EnumAsString(TypeDecorator):
    """Custom type to store Enum as string in database"""
    
    impl = String  # Use String as the underlying type
    cache_ok = True
    
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)
    
    def process_bind_param(self, value, dialect):
        """Convert Python Enum to string for database storage"""
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        # If it's already a string, return as-is
        return value
    
    def process_result_value(self, value, dialect):
        """Convert string from database back to Python Enum"""
        if value is None:
            return None
        try:
            return self.enum_class(value)
        except ValueError:
            # Handle case where database has invalid enum value
            print(f"Warning: Invalid enum value '{value}' for {self.enum_class.__name__}")
            return None


Base = declarative_base()
# Database setup
engine = create_engine('duckdb:///db/memo_id.db', echo=False)
# engine = create_engine('duckdb:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

class ID(Base):
    __tablename__ = "memo_id"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(EnumAsString(IdType), nullable=False) 
    value = Column(Text, nullable=False, index=True)
    note = Column(Text)
    status = Column(EnumAsString(IdStatus), nullable=False) 
    last_updated_dt = Column(DateTime)

Base.metadata.create_all(engine)
