# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from todo.models import Todo, TodoList, User
from django.core.urlresolvers import resolve
import json
import ipdb

# Create your tests here.
API_BASE_URL = '/api/v1'


def get_pk_from_resource_uri(resource_uri):
    resource, args, kwargs = resolve(resource_uri)
    return kwargs.get('pk')


class Helper(ResourceTestCaseMixin):
    def signup_helper(self):
        url = ''.join([API_BASE_URL, '/user/signup/'])
        data = {
            "username": "gauravorgzit",
            "email": "gaurav@p3infotech.in",
            "password": "viveknain"
        }
        return self.client.post(url, data=json.dumps(data), content_type='application/json')

    def signup_helper2(self):
        url = ''.join([API_BASE_URL, '/user/signup/'])
        data = {
            "username": "gauravorgzit1",
            "email": "gaurav1@p3infotech.in",
            "password": "viveknain"
        }
        return self.client.post(url, data=json.dumps(data), content_type='application/json')

    def logout_helper(self):
        url = ''.join([API_BASE_URL, '/user/logout/'])
        self.client.get(url)

    def save_todolist_helper(self):
        user = self.signup_helper().json()['user']
        url = ''.join([API_BASE_URL, '/todolist/'])
        data = {
            "title": "this is for testing",
            "created_by": user['resource_uri'],
            "shared_with": []
        }
        return self.client.post(url, data=json.dumps(data), content_type='application/json')

    def share_todolist_helper(self):
        user1 = self.signup_helper2().json()['user']
        self.logout_helper()
        todol = self.save_todolist_helper().json()
        todol['shared_with'].append(user1['resource_uri'])
        url = ''.join([API_BASE_URL, '/todolist/', str(todol['id']), '/'])
        return self.client.put(url, data=json.dumps(todol), content_type='application/json')


class UserTestCase(Helper, ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(UserTestCase, self).setUp()

    def test_user_signup(self):
        resp = self.signup_helper()
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    def test_user_login(self):
        user = self.signup_helper().json()['user']
        self.logout_helper()
        url = ''.join([API_BASE_URL, '/user/login/'])
        data = {
            "username": "gauravorgzit",
            "password": "viveknain"
        }
        resp = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_user_incorrect_password(self):
        user = self.signup_helper().json()['user']
        self.logout_helper()
        url = ''.join([API_BASE_URL, '/user/login/'])
        data = {
            "username": "gauravorgzit",
            "password": "viveknin"
        }
        resp = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertHttpUnauthorized(resp)
        self.assertValidJSON(resp.content)

    def test_user_incorrect_username(self):
        user = self.signup_helper().json()['user']
        self.logout_helper()
        url = ''.join([API_BASE_URL, '/user/login/'])
        data = {
            "username": "gauravogzit",
            "password": "viveknain"
        }
        resp = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertHttpUnauthorized(resp)
        self.assertValidJSON(resp.content)


class TodoListTestCase(Helper, ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(TodoListTestCase, self).setUp()

    def test_save_todolist(self):
        resp = self.save_todolist_helper()
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    def test_see_own_todolist(self):
        todol = self.save_todolist_helper()
        url = ''.join([API_BASE_URL, '/todolist/mytodolists/'])
        resp = self.client.get(url)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_share_todolist(self):
        resp = self.share_todolist_helper()
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

    def test_shared_with_me_todolist(self):
        todol = self.share_todolist_helper().json()
        url = ''.join([API_BASE_URL, '/todolist/?shared_with=', get_pk_from_resource_uri(todol['created_by'])])
        resp = self.client.get(url)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)


class TodoTestCase(Helper, ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(TodoTestCase, self).setUp()

    def test_save_todo(self):
        todol = self.save_todolist_helper().json()
        url = ''.join([API_BASE_URL, '/todo/'])
        data = {
            "content": "Its just about testing nothing else.",
            "todolist": todol['resource_uri']
        }
        resp = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

    def test_see_todo(self):
        todol = self.save_todolist_helper().json()
        url = ''.join([API_BASE_URL, '/todo/?todolist=', str(todol['id'])])
        resp = self.client.get(url)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
