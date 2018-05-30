from django.shortcuts import render, HttpResponse
import json
# Create your views here.
def index(request):
    
    return render(request, 'index.html')


def sendMsg(request):
    message = {'status': True, 'summary': 'sss'}
    print(request.POST.get("email"))
    return HttpResponse(json.dumps(message))
