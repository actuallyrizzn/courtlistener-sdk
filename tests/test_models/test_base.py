"""
Comprehensive tests for the BaseModel class.
"""

import pytest
import json
from datetime import datetime, date
from courtlistener.models.base import BaseModel


class TestBaseModel:
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
            "id": 1,
            "name": "Test",
            "title": "Test Title",
            "description": "Test Description",
            "url": "https://example.com",
            "absolute_url": "https://example.com/absolute"
        }
        model = BaseModel(data)
        assert model.id == 1
        assert model.name == "Test"
        assert model.title == "Test Title"
        assert model.description == "Test Description"
        assert model.url == "https://example.com"
        assert model.absolute_url == "https://example.com/absolute"

    def test_init_with_private_fields(self):
        """Test initialization with private fields (should not be set as attributes)."""
        data = {"id": 1, "_private": "secret", "__very_private": "very_secret"}
        model = BaseModel(data)
        assert model.id == 1
        assert not hasattr(model, "_private")
        assert not hasattr(model, "__very_private")

    def test_init_with_unknown_fields(self):
        """Test initialization with unknown fields (should not be set as attributes)."""
        data = {"id": 1, "unknown_field": "value", "another_unknown": 123}
        model = BaseModel(data)
        assert model.id == 1
        assert not hasattr(model, "unknown_field")
        assert not hasattr(model, "another_unknown")

    def test_to_dict_basic(self):
        """Test basic to_dict conversion."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_dict()
        assert result == {"id": 1, "name": "Test"}

    def test_to_dict_with_datetime(self):
        """Test to_dict with datetime objects."""
        now = datetime.now()
        data = {"id": 1, "created_at": now}
        model = BaseModel(data)
        result = model.to_dict()
        assert result["id"] == 1
        assert result["created_at"] == now.isoformat()

    def test_to_dict_with_date(self):
        """Test to_dict with date objects."""
        today = date.today()
        data = {"id": 1, "date_filed": today}
        model = BaseModel(data)
        result = model.to_dict()
        assert result["id"] == 1
        assert result["date_filed"] == today.isoformat()

    def test_to_dict_with_nested_model(self):
        """Test to_dict with nested BaseModel."""
        class TestModel(BaseModel):
            pass
        
        nested_data = {"id": 2, "name": "Nested"}
        nested_model = TestModel(nested_data)
        data = {"id": 1, "nested": nested_model}
        model = BaseModel(data)
        result = model.to_dict()
        assert result["id"] == 1
        assert result["nested"] == {"id": 2, "name": "Nested"}

    def test_to_dict_with_list_of_models(self):
        """Test to_dict with list of BaseModel instances."""
        class TestModel(BaseModel):
            pass
        
        nested_models = [
            TestModel({"id": 2, "name": "Item1"}),
            TestModel({"id": 3, "name": "Item2"})
        ]
        data = {"id": 1, "items": nested_models}
        model = BaseModel(data)
        result = model.to_dict()
        assert result["id"] == 1
        assert result["items"] == [
            {"id": 2, "name": "Item1"},
            {"id": 3, "name": "Item2"}
        ]

    def test_to_dict_with_mixed_list(self):
        """Test to_dict with mixed list of models and primitives."""
        class TestModel(BaseModel):
            pass
        
        mixed_list = [
            TestModel({"id": 2, "name": "Item1"}),
            "string_item",
            123,
            {"dict": "item"}
        ]
        data = {"id": 1, "items": mixed_list}
        model = BaseModel(data)
        result = model.to_dict()
        assert result["id"] == 1
        assert result["items"] == [
            {"id": 2, "name": "Item1"},
            "string_item",
            123,
            {"dict": "item"}
        ]

    def test_to_json_basic(self):
        """Test basic to_json conversion."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_json()
        expected = json.dumps({"id": 1, "name": "Test"})
        assert result == expected

    def test_to_json_with_indent(self):
        """Test to_json with indentation."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        result = model.to_json(indent=2)
        expected = json.dumps({"id": 1, "name": "Test"}, indent=2)
        assert result == expected

    def test_get_existing_attribute(self):
        """Test get method with existing attribute."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        assert model.get("id") == 1
        assert model.get("name") == "Test"

    def test_get_missing_attribute(self):
        """Test get method with missing attribute."""
        data = {"id": 1}
        model = BaseModel(data)
        assert model.get("missing") is None
        assert model.get("missing", "default") == "default"

    def test_getitem_existing_attribute(self):
        """Test __getitem__ with existing attribute."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        assert model["id"] == 1
        assert model["name"] == "Test"

    def test_getitem_missing_attribute(self):
        """Test __getitem__ with missing attribute."""
        data = {"id": 1}
        model = BaseModel(data)
        with pytest.raises(AttributeError):
            model["missing"]

    def test_contains_existing_attribute(self):
        """Test __contains__ with existing attribute."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel(data)
        assert "id" in model
        assert "name" in model

    def test_contains_missing_attribute(self):
        """Test __contains__ with missing attribute."""
        data = {"id": 1}
        model = BaseModel(data)
        assert "missing" not in model

    def test_repr_with_id(self):
        """Test __repr__ with id attribute."""
        data = {"id": 1}
        model = BaseModel(data)
        assert repr(model) == "BaseModel(id=1)"

    def test_repr_with_name(self):
        """Test __repr__ with name attribute."""
        data = {"name": "Test"}
        model = BaseModel(data)
        assert repr(model) == "BaseModel(name='Test')"

    def test_repr_without_id_or_name(self):
        """Test __repr__ without id or name."""
        data = {"other": "value"}
        model = BaseModel(data)
        assert repr(model) == "BaseModel()"

    def test_str(self):
        """Test __str__ method."""
        data = {"id": 1}
        model = BaseModel(data)
        assert str(model) == "BaseModel(id=1)"

    def test_from_dict(self):
        """Test from_dict class method."""
        data = {"id": 1, "name": "Test"}
        model = BaseModel.from_dict(data)
        assert isinstance(model, BaseModel)
        assert model.id == 1
        assert model.name == "Test"

    def test_from_json(self):
        """Test from_json class method."""
        json_str = '{"id": 1, "name": "Test"}'
        model = BaseModel.from_json(json_str)
        assert isinstance(model, BaseModel)
        assert model.id == 1
        assert model.name == "Test"

    def test_parse_date_valid_format(self):
        """Test _parse_date with valid date format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_date("2023-01-01")
        assert result == date(2023, 1, 1)

    def test_parse_date_datetime_format(self):
        """Test _parse_date with datetime format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_date("2023-01-01T12:30:45")
        assert result == date(2023, 1, 1)

    def test_parse_date_invalid_format(self):
        """Test _parse_date with invalid format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_date("invalid-date")
        assert result is None

    def test_parse_date_none(self):
        """Test _parse_date with None."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_date(None)
        assert result is None

    def test_parse_date_empty_string(self):
        """Test _parse_date with empty string."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_date("")
        assert result is None

    def test_parse_datetime_valid_format(self):
        """Test _parse_datetime with valid datetime format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_datetime("2023-01-01T12:30:45")
        assert result == datetime(2023, 1, 1, 12, 30, 45)

    def test_parse_datetime_date_format(self):
        """Test _parse_datetime with date format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_datetime("2023-01-01")
        assert result == datetime(2023, 1, 1)

    def test_parse_datetime_invalid_format(self):
        """Test _parse_datetime with invalid format."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_datetime("invalid-datetime")
        assert result is None

    def test_parse_datetime_none(self):
        """Test _parse_datetime with None."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_datetime(None)
        assert result is None

    def test_parse_datetime_empty_string(self):
        """Test _parse_datetime with empty string."""
        data = {"id": 1}
        model = BaseModel(data)
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
        items = [{"id": 2}, {"id": 3}]
        result = model._parse_list(items)
        assert result == items

    def test_parse_list_with_model_class(self):
        """Test _parse_list with model class."""
        class TestModel(BaseModel):
            pass
        
        data = {"id": 1}
        model = BaseModel(data)
        items = [{"id": 2, "name": "Item1"}, {"id": 3, "name": "Item2"}]
        result = model._parse_list(items, TestModel)
        assert len(result) == 2
        assert all(isinstance(item, TestModel) for item in result)
        assert result[0].id == 2
        assert result[1].id == 3

    def test_parse_list_mixed_items(self):
        """Test _parse_list with mixed items."""
        class TestModel(BaseModel):
            pass
        
        data = {"id": 1}
        model = BaseModel(data)
        items = [{"id": 2}, "string", 123]
        result = model._parse_list(items, TestModel)
        assert len(result) == 3
        assert isinstance(result[0], TestModel)
        assert result[1] == "string"
        assert result[2] == 123

    def test_parse_related_model_none(self):
        """Test _parse_related_model with None."""
        data = {"id": 1}
        model = BaseModel(data)
        result = model._parse_related_model(None)
        assert result is None

    def test_parse_related_model_with_model_class(self):
        """Test _parse_related_model with model class."""
        class TestModel(BaseModel):
            pass
        
        data = {"id": 1}
        model = BaseModel(data)
        related_data = {"id": 2, "name": "Related"}
        result = model._parse_related_model(related_data, TestModel)
        assert isinstance(result, TestModel)
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
        result = model._parse_related_model("string")
        assert result == "string"
