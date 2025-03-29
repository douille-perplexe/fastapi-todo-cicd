import pytest
from app.models import TodoBase, TodoCreate, Todo


def test_todo_base_create():
   # Test creating a TodoBase with minimum required values
   todo = TodoBase(title="Test Title")
   assert todo.title == "Test Title"
   assert todo.description is None
   assert todo.completed is False

   # Test with all fields
   todo = TodoBase(
       title="Test Title",
       description="Test Description",
       completed=True
   )
   assert todo.title == "Test Title"
   assert todo.description == "Test Description"
   assert todo.completed is True


def test_todo_base_validation():
   # Validation test - title is required
   with pytest.raises(ValueError):
       TodoBase()

   # Type testing - completed must be a boolean
   with pytest.raises(ValueError):
       TodoBase(title="Test", completed="not a boolean")


def test_todo_create():
   # TodoCreate has the same properties as TodoBase
   todo = TodoCreate(title="Test Create")
   assert todo.title == "Test Create"
   assert todo.description is None
   assert todo.completed is False


def test_todo_model():
   # Test the complete model with ID
   todo = Todo(
       id=1,
       title="Test Todo",
       description="Test Description",
       completed=False
   )
   assert todo.id == 1
   assert todo.title == "Test Todo"
   assert todo.description == "Test Description"
   assert todo.completed is False

   # Test dictionary/JSON serialization
   todo_dict = todo.model_dump()
   assert todo_dict == {
       "id": 1,
       "title": "Test Todo",
       "description": "Test Description",
       "completed": False
   }


def test_todo_model_validation():
   # id is required for the Todo model
   with pytest.raises(ValueError):
       Todo(title="Test without ID")

   # id must be an int
   with pytest.raises(ValueError):
       Todo(id="not an int", title="Test")