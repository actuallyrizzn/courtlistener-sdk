"""
Comprehensive tests for BaseModel class.
"""

import pytest
import json
from datetime import datetime, date
from unittest.mock import Mock, patch
from courtlistener.models.base import BaseModel


class TestBaseModelComprehensive:
    """Test cases for BaseModel class."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        
        assert model._data == data
        assert model.id == 1
        assert model.name == "Test"

    def test_init_with_common_fields(self):
        """Test initialization with common fields."""
        data = {
            "id": 123,
            "name": "Test Model",
            "title": "Test Title",
            "description": "Test Description",
            "url": "https://example.com",
            "absolute_url": "https://example.com/absolute"
        }
        model = BaseModel(data)
        
        assert model.id == 123
        assert model.name == "Test Model"
        assert model.title == "Test Title"
        assert model.description == "Test Description"
        assert model.url == "https://example.com"
        assert model.absolute_url == "https://example.com/absolute"

    def test_init_with_private_fields(self):
        """Test initialization with private fields (should not be set as attributes)."""
        data = {
            "id": 1,
            "_private_field": "private_value",
            "__double_private": "double_private"
        }
        model = BaseModel(data)
        
        assert model.id == 1
        assert not hasattr(model, "_private_field")
        assert not hasattr(model, "__double_private")

    def test_init_with_property_conflict(self):
        """Test initialization when data key conflicts with property."""
        class ModelWithProperty(BaseModel):
            @property
            def name(self):
                return "Property Name"
        
        data = {"id": 1, "name": "Data Name"}
        model = ModelWithProperty(data)
        
        # Should not set name as attribute due to property conflict
        assert model.name == "Property Name"  # Property value
        # Note: The current implementation still sets it as attribute, 
        # but the property takes precedence when accessed

    def test_parse_data_override(self):
        """Test that _parse_data can be overridden."""
        class CustomModel(BaseModel):
            def _parse_data(self):
                super()._parse_data()
                self.custom_field = "custom_value"
        
        data = {"id": 1}
        model = CustomModel(data)
        
        assert model.id == 1
        assert model.custom_field == "custom_value"

    def test_to_dict_basic(self):
        """Test to_dict with basic data."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_dict()
        
        assert result == {"id": 1, "name": "Test"}

    def test_to_dict_with_datetime(self):
        """Test to_dict with datetime objects."""
        now = datetime(2023, 1, 1, 12, 0, 0)
        today = date(2023, 1, 1)
        
        data = {"id": 1}
        model = BaseModel(data)
        model.created_at = now
        model.date_field = today
        
        result = model.to_dict()
        
        assert result["created_at"] == "2023-01-01T12:00:00"
        assert result["date_field"] == "2023-01-01"

    def test_to_dict_with_basemodel(self):
        """Test to_dict with nested BaseModel objects."""
        data = {"id": 1}
        model = BaseModel(data)
        
        nested_data = {"id": 2, "name": "Nested"}
        nested_model = BaseModel(nested_data)
        model.nested = nested_model
        
        result = model.to_dict()
        
        assert result["nested"] == {"id": 2, "name": "Nested"}

    def test_to_dict_with_list_of_models(self):
        """Test to_dict with list of BaseModel objects."""
        data = {"id": 1}
        model = BaseModel(data)
        
        nested_models = [
            BaseModel({"id": 2, "name": "Item 1"}),
            BaseModel({"id": 3, "name": "Item 2"})
        ]
        model.items = nested_models
        
        result = model.to_dict()
        
        expected = [
            {"id": 2, "name": "Item 1"},
            {"id": 3, "name": "Item 2"}
        ]
        assert result["items"] == expected

    def test_to_dict_with_mixed_list(self):
        """Test to_dict with mixed list (models and primitives)."""
        data = {"id": 1}
        model = BaseModel(data)
        
        mixed_list = [
            BaseModel({"id": 2, "name": "Model"}),
            "string",
            123,
            {"dict": "value"}
        ]
        model.mixed = mixed_list
        
        result = model.to_dict()
        
        expected = [
            {"id": 2, "name": "Model"},
            "string",
            123,
            {"dict": "value"}
        ]
        assert result["mixed"] == expected

    def test_to_dict_with_properties(self):
        """Test to_dict includes properties."""
        class ModelWithProperty(BaseModel):
            @property
            def computed_field(self):
                return f"computed_{self.id}"
        
        data = {"id": 1, "name": "Test"}
        model = ModelWithProperty(data)
        
        result = model.to_dict()
        
        assert result["computed_field"] == "computed_1"
        assert result["id"] == 1
        assert result["name"] == "Test"

    def test_to_dict_property_exception_handling(self):
        """Test to_dict handles property exceptions gracefully."""
        class ModelWithFailingProperty(BaseModel):
            @property
            def failing_property(self):
                raise Exception("Property error")
        
        data = {"id": 1}
        model = ModelWithFailingProperty(data)
        
        result = model.to_dict()
        
        # Should not include the failing property
        assert "failing_property" not in result
        assert result["id"] == 1

    def test_to_json_basic(self):
        """Test to_json with basic data."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_json()
        
        expected = '{"id": 1, "name": "Test"}'
        assert result == expected

    def test_to_json_with_indent(self):
        """Test to_json with indentation."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_json(indent=2)
        
        expected = '{\n  "id": 1,\n  "name": "Test"\n}'
        assert result == expected

    def test_to_json_with_default_str(self):
        """Test to_json with default=str for non-serializable objects."""
        data = {"id": 1}
        model = BaseModel(data)
        model.custom_obj = Mock()  # Non-serializable object
        
        result = model.to_json()
        
        # Should not raise exception due to default=str
        assert '"custom_obj"' in result

    def test_get_method(self):
        """Test get method with default fallback."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        
        assert model.get("id") == 1
        assert model.get("name") == "Test"
        assert model.get("nonexistent") is None
        assert model.get("nonexistent", "default") == "default"

    def test_getitem_method(self):
        """Test dictionary-style access."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        
        assert model["id"] == 1
        assert model["name"] == "Test"

    def test_getitem_method_missing_key(self):
        """Test dictionary-style access with missing key."""
        data = {"id": 1}
        model = BaseModel(data)
        
        with pytest.raises(AttributeError):
            _ = model["nonexistent"]

    def test_contains_method(self):
        """Test contains method."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        
        assert "id" in model
        assert "name" in model
        assert "nonexistent" not in model

    def test_repr_with_id(self):
        """Test string representation with id."""
        data = {"id": 123, "name": "Test"}
        model = BaseModel(data)
        
        assert repr(model) == "BaseModel(id=123)"

    def test_repr_with_name(self):
        """Test string representation with name (no id)."""
        data = {"name": "Test Model"}
        model = BaseModel(data)
        
        assert repr(model) == "BaseModel(name='Test Model')"

    def test_repr_without_id_or_name(self):
        """Test string representation without id or name."""
        data = {"description": "Test Description"}
        model = BaseModel(data)
        
        assert repr(model) == "BaseModel()"

    def test_str_method(self):
        """Test str method delegates to repr."""
        data = {"id": 123}
        model = BaseModel(data)
        
        assert str(model) == repr(model)

    def test_from_dict_classmethod(self):
        """Test from_dict class method."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel.from_dict(data)
        
        assert isinstance(model, BaseModel)
        assert model.id == 1
        assert model.name == "Test"

    def test_from_json_classmethod(self):
        """Test from_json class method."""
        json_str = '{"id": 1, "name": "Test"}'
        model = BaseModel.from_json(json_str)
        
        assert isinstance(model, BaseModel)
        assert model.id == 1
        assert model.name == "Test"

    def test_from_json_invalid_json(self):
        """Test from_json with invalid JSON."""
        json_str = '{"id": 1, "name": "Test"'  # Missing closing brace
        
        with pytest.raises(json.JSONDecodeError):
            BaseModel.from_json(json_str)

    def test_parse_date_valid_formats(self):
        """Test _parse_date with valid date formats."""
        data = {"id": 1}
        model = BaseModel(data)
        
        # Test YYYY-MM-DD format
        result1 = model._parse_date("2023-01-15")
        assert result1 == date(2023, 1, 15)
        
        # Test YYYY-MM-DDTHH:MM:SS format
        result2 = model._parse_date("2023-01-15T12:30:45")
        assert result2 == date(2023, 1, 15)

    def test_parse_date_invalid_formats(self):
        """Test _parse_date with invalid date formats."""
        data = {"id": 1}
        model = BaseModel(data)
        
        # Test invalid format
        result = model._parse_date("invalid-date")
        assert result is None
        
        # Test None input
        result = model._parse_date(None)
        assert result is None
        
        # Test empty string
        result = model._parse_date("")
        assert result is None

    def test_parse_datetime_valid_formats(self):
        """Test _parse_datetime with valid datetime formats."""
        data = {"id": 1}
        model = BaseModel(data)
        
        # Test YYYY-MM-DDTHH:MM:SS format
        result1 = model._parse_datetime("2023-01-15T12:30:45")
        assert result1 == datetime(2023, 1, 15, 12, 30, 45)
        
        # Test YYYY-MM-DD format (should return datetime at midnight)
        result2 = model._parse_datetime("2023-01-15")
        assert result2 == datetime(2023, 1, 15, 0, 0, 0)

    def test_parse_datetime_invalid_formats(self):
        """Test _parse_datetime with invalid datetime formats."""
        data = {"id": 1}
        model = BaseModel(data)
        
        # Test invalid format
        result = model._parse_datetime("invalid-datetime")
        assert result is None
        
        # Test None input
        result = model._parse_datetime(None)
        assert result is None
        
        # Test empty string
        result = model._parse_datetime("")
        assert result is None

    def test_parse_list_empty(self):
        """Test _parse_list with empty list."""
        data = {"id": 1}
        model = BaseModel(data)
        
        result = model._parse_list([])
        assert result == []

    def test_parse_list_without_model_class(self):
        """Test _parse_list without model class."""
        data = {"id": 1}
        model = BaseModel(data)
        
        items = [{"id": 1}, {"id": 2}, "string", 123]
        result = model._parse_list(items)
        
        assert result == items

    def test_parse_list_with_model_class(self):
        """Test _parse_list with model class."""
        data = {"id": 1}
        model = BaseModel(data)
        
        items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
        result = model._parse_list(items, BaseModel)
        
        assert len(result) == 2
        assert all(isinstance(item, BaseModel) for item in result)
        assert result[0].id == 1
        assert result[0].name == "Item 1"
        assert result[1].id == 2
        assert result[1].name == "Item 2"

    def test_parse_list_with_mixed_types(self):
        """Test _parse_list with mixed types."""
        data = {"id": 1}
        model = BaseModel(data)
        
        items = [{"id": 1}, "string", 123]
        result = model._parse_list(items, BaseModel)
        
        assert len(result) == 3
        assert isinstance(result[0], BaseModel)
        assert result[1] == "string"
        assert result[2] == 123

    def test_parse_related_model_none(self):
        """Test _parse_related_model with None input."""
        data = {"id": 1}
        model = BaseModel(data)
        
        result = model._parse_related_model(None)
        assert result is None

    def test_parse_related_model_with_model_class(self):
        """Test _parse_related_model with model class."""
        data = {"id": 1}
        model = BaseModel(data)
        
        related_data = {"id": 2, "name": "Related"}
        result = model._parse_related_model(related_data, BaseModel)
        
        assert isinstance(result, BaseModel)
        assert result.id == 2
        assert result.name == "Related"

    def test_parse_related_model_without_model_class(self):
        """Test _parse_related_model without model class."""
        data = {"id": 1}
        model = BaseModel(data)
        
        related_data = {"id": 2, "name": "Related"}
        result = model._parse_related_model(related_data)
        
        assert result == related_data

    def test_parse_related_model_non_dict(self):
        """Test _parse_related_model with non-dict data."""
        data = {"id": 1}
        model = BaseModel(data)
        
        result = model._parse_related_model("string", BaseModel)
        assert result == "string"

    def test_parse_related_model_invalid_model_class(self):
        """Test _parse_related_model with invalid model class."""
        data = {"id": 1}
        model = BaseModel(data)
        
        related_data = {"id": 2, "name": "Related"}
        result = model._parse_related_model(related_data, str)  # str is not a BaseModel
        
        assert result == related_data

    def test_edge_case_empty_data(self):
        """Test initialization with empty data."""
        model = BaseModel({})
        
        assert model._data == {}
        assert not hasattr(model, "id")
        assert not hasattr(model, "name")

    def test_edge_case_none_values(self):
        """Test initialization with None values."""
        data = {"id": None, "name": None, "description": "Valid"}
        model = BaseModel(data)
        
        assert model.id is None
        assert model.name is None
        assert model.description == "Valid"

    def test_edge_case_boolean_values(self):
        """Test initialization with boolean values."""
        data = {"id": 1, "active": True, "deleted": False}
        model = BaseModel(data)
        
        assert model.id == 1
        # Boolean values are not in the common fields list, so they won't be set as attributes
        # They are still accessible via _data
        assert model._data["active"] is True
        assert model._data["deleted"] is False

    def test_edge_case_numeric_values(self):
        """Test initialization with various numeric values."""
        data = {
            "id": 1,
            "count": 0,
            "rate": 0.5,
            "negative": -1
        }
        model = BaseModel(data)
        
        assert model.id == 1
        # Numeric values are not in the common fields list, so they won't be set as attributes
        # They are still accessible via _data
        assert model._data["count"] == 0
        assert model._data["rate"] == 0.5
        assert model._data["negative"] == -1
