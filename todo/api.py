import json
from django.db import IntegrityError
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.contrib import auth
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from todo.models import Todo, TodoList, User
from tastypie.http import HttpUnauthorized


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('log_in')),
            url(r"^(?P<resource_name>%s)/logout%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('log_out')),
            url(r"^(?P<resource_name>%s)/signup%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('sign_up')),
        ]

    def log_in(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))
        user = auth.authenticate(username=data['username'], password=data['password'])
        if request.user.is_authenticated():
            return self.create_response(request, {'status':'You are already logged in', 'user': user.id})
        if user is not None and user.is_active and not (request.user.is_authenticated()):
            auth.login(request, user)
            return self.create_response(request, {'status':'logged in', 'user': user.id})
        else:
            return self.create_response(request, {'status':'Invalid user'})

    def log_out(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            auth.logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

    def sign_up(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        # username = request.POST.get('username')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        data = self.deserialize(
            request, request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))
        try:
            User.objects.create_user(data['username'], data['email'], data['password'])
        except IntegrityError:
            return self.create_response(request, {'status':'Username already exists'})
        # return JsonResponse({'success':'signed up successfully'})
        # return HttpResponse(content_type='application/json', content=json.dumps({'success':'signed up successfully'}))
        return self.create_response(request, {'success':'signed up successfully'})


class TodoListResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    shared_with = fields.ManyToManyField(UserResource, 'shared_with')
    open_todos = fields.IntegerField()

    class Meta:
        queryset = TodoList.objects.all()
        resource_name = 'todolist'
        always_return_data = True
        authorization = Authorization()
        filtering = {
            'created_by': ALL_WITH_RELATIONS,
            'shared_with': ALL_WITH_RELATIONS,
        }

    def dehydrate_open_todos(self, bundle):
        # print bundle.obj, type(bundle.obj), bundle.obj.id
        return Todo.objects.filter(todolist=bundle.obj.id, done=False).count()
        # return 6


class TodoResource(ModelResource):
    todolist = fields.ForeignKey(TodoListResource, 'todolist')

    class Meta:
        queryset = Todo.objects.all()
        resource_name = 'todo'
        always_return_data = True
        authorization = Authorization()
        filtering = {
            'todolist': ALL_WITH_RELATIONS,
        }
