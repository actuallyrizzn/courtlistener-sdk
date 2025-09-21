"""
Base model class for CourtListener SDK data models.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, date
import json


class BaseModel:
    """Base class for all CourtListener data models."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize model with API response data.
        
        Args:
            data: Dictionary containing model data from API response
        """
        self._data = data
        self._parse_data()
    
    def _parse_data(self):
        """Parse raw data into model attributes. Override in subclasses."""
        # Store all data in _data for access via getattr
        for key, value in self._data.items():
            if not key.startswith('_'):
                # Only set attributes that are not already defined as properties
                if not (hasattr(self.__class__, key) and isinstance(getattr(self.__class__, key), property)):
                    setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        result = {}
        # Include normal attributes
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, (datetime, date)):
                    result[key] = value.isoformat()
                elif isinstance(value, BaseModel):
                    result[key] = value.to_dict()
                elif isinstance(value, list):
                    result[key] = [
                        item.to_dict() if isinstance(item, BaseModel) else item
                        for item in value
                    ]
                else:
                    result[key] = value
        # Include properties that are not private and not already in result
        for key in dir(self.__class__):
            if not key.startswith('_') and isinstance(getattr(self.__class__, key), property) and key not in result:
                try:
                    result[key] = getattr(self, key)
                except Exception:
                    pass
        return result
    
    def to_json(self, indent: Optional[int] = None) -> str:
        """Convert model to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get attribute value with default fallback."""
        return getattr(self, key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to attributes."""
        return getattr(self, key)
    
    def __contains__(self, key: str) -> bool:
        """Check if attribute exists."""
        return hasattr(self, key)
    
    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            return f"{class_name}(id={self.id})"
        elif hasattr(self, 'name'):
            return f"{class_name}(name='{self.name}')"
        else:
            return f"{class_name}()"
    
    def __str__(self) -> str:
        """String representation of the model."""
        return self.__repr__()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model instance from dictionary."""
        return cls(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """Create model instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str:
            return None
        
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').date()
            except ValueError:
                return None
    
    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not datetime_str:
            return None
        
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(datetime_str, '%Y-%m-%d')
            except ValueError:
                return None
    
    def _parse_list(self, data: List[Any], model_class: Optional[type] = None) -> List[Any]:
        """Parse list of items, optionally converting to model instances."""
        if not data:
            return []
        
        if model_class and issubclass(model_class, BaseModel):
            return [model_class(item) if isinstance(item, dict) else item for item in data]
        else:
            return data
    
    def _parse_related_model(self, data: Any, model_class: Optional[type] = None) -> Any:
        """Parse related model data."""
        if not data:
            return None
        
        if isinstance(data, dict) and model_class and issubclass(model_class, BaseModel):
            return model_class(data)
        else:
            return data 