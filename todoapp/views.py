from django.shortcuts import render_to_response  
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})
    #t = get_template('current_datetime.html')
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hours_ahead.html', {'current_date': dt, 'offset': offset})
    #html = "<html><body>In %s hour(s), it will be %s</body></html>" % (offset,dt)
    #return HttpResponse(html)