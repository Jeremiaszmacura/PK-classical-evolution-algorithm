import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from classic_EA.classicEA import ClassicEA


@csrf_exempt 
def classic_EA_api(request):
    """Api endpoint controller for classical evolution-algorithm"""
    if request.method == "POST":
        data = json.loads(request.body)
        classicEA_obj = ClassicEA(**data)
        classicEA_obj.run()
        return JsonResponse(data)
