import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from EA_real_chromosome.EA_real_chromosome import EA_real_chromosome


@csrf_exempt
def EA_real_chromosome_api(request):
    """Api endpoint controller for classical evolution-algorithm"""
    if request.method == "POST":
        required_params = (
            "numberOfPopulation", "epochs", "crossProbability", "mutationProbability", "selectionPercent",
            "elitistStrategyPercent", "sizeOfTournament", "selectionName", "crossoverName", "mutationName")
        try:
            data = json.loads(request.body)
            if not all(param in data for param in required_params):
                return JsonResponse({"message": "Missing at least one of required params"})
            ea_real_chromosome = EA_real_chromosome(**data)
            return JsonResponse({"time": ea_real_chromosome.run()})
        except Exception as error:
            print(f"Classic_EA error: {error}")
            return JsonResponse({"message": "an error has occurred in the classical evolution algorithm"})
