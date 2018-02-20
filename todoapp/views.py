from django.shortcuts import render_to_response
# from django.contrib import auth
# from todoapp.models import User
# from django import oldforms as forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
# import datetime


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = auth.authenticate(username=username, password=password)
#     if user is not none and user.is_active:
#         auth.login(request, user)
#         return HttpResponse('logged in')
#     else:
#         return HttpResponse('Invalid user')

# def logout(request):
#     auth.logout(request)
#     return HttpResponse('logged out')


# def signin_user(request):
#     now = datetime.datetime.now()
#     return render_to_response('current_datetime.html', {'current_date': now})
#     t = get_template('current_datetime.html')
#     html = t.render(Context({'current_date': now}))
#     return HttpResponse(html)


# def signout_user(request, offset):
#     offset = int(offset)
#     dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
#     return render_to_response('hours_ahead.html', {'current_date': dt, 'offset': offset})
#     html = "<html><body>In %s hour(s), it will be %s</body></html>" % (offset,dt)
#     return HttpResponse(html)


# def signup_user(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         data = request.POST.copy()
#         errors = form.get_validation_errors(data)
#         if not errors:
#             new_user = form.save(data)
#             return HttpResponseRedirect('/')
#     else:
#         data, errors = {}, {}
#     return render_to_response()
