from django.db import IntegrityError
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.contrib import auth
from django.http import HttpResponse, HttpResponseBadRequest
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponse('logged in')
        else:
            return HttpResponse('Invalid user')

    def log_out(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            auth.logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

    def sign_up(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            User.objects.create_user(username, email, password)
        except IntegrityError:
            return HttpResponseBadRequest('Username already exists')
        return HttpResponse({'success':'signed up successfully'})


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
