from tastypie.resources import ModelResource
from todo.models import Todo, TodoList


class TodoResource(ModelResource):
    class Meta:
        queryset = Todo.objects.all()
        resource_name = 'todo'


class TodoListResource(ModelResource):
    class Meta:
        queryset = TodoList.objects.all()
        resource_name = 'todolist'
