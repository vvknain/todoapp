from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from todo.models import Todo, TodoList, User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()


class TodoListResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    # shared_with = fields.ManyToManyField(UserResource, 'shared_with')

    class Meta:
        queryset = TodoList.objects.all()
        resource_name = 'todolist'
        # authorization = Authorization()
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            # 'shared_with': ALL_WITH_RELATIONS,
        }


class TodoResource(ModelResource):
    todolist = fields.ForeignKey(TodoListResource, 'todolist')

    class Meta:
        queryset = Todo.objects.all()
        resource_name = 'todo'
        # authorization = Authorization()
        filtering = {
            'todolist': ALL_WITH_RELATIONS,
        }
