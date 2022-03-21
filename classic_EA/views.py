import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class ClassicEA:
    """Class representation of classical evolution-algorithm"""
    def __init__(self, **kwargs):
        self.dokladnosc = kwargs.get('dokladnosc')
        self.wielkosc_populacji = kwargs.get('wielkosc_populacji')
        self.liczba_epok = kwargs.get('liczba_epok')
        self.metoda_selekcji = kwargs.get('metoda_selekcji')
        self.krzyzowanie = kwargs.get('krzyzowanie')
        self.prawdop_krzyzowania = kwargs.get('prawdop_krzyzowania')
        self.metoda_mutacji = kwargs.get('metoda_mutacji')
        self.prawdop_mutacji = kwargs.get('prawdop_mutacji')
        self.prawdop_inwersji = kwargs.get('prawdop_inwersji')
        self.prawdop_w_strategi_elitarnej = kwargs.get('prawdop_w_strategi_elitarnej')
    
    def proces_classic_EA(self):
        """Logic of classical evolution-algorithm"""
        print("Put there logic of classical evolution-algorithm")


@csrf_exempt 
def classic_EA_api(request):
    """Api endpoint controller for classical evolution-algorithm"""
    if request.method == "POST":
        data = json.loads(request.body)
        classicEA_obj = ClassicEA(**data)
        classicEA_obj.proces_classic_EA()
        return JsonResponse(data)

    return JsonResponse({"message": "GET request to classic-EA"})
