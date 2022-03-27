import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from classic_EA.classicEA import ClassicEA

{
  "number_of_population": 20,
  "length_of_chromosome": 25,
  "epochs": 500,
  "cross_probability": 0.8,
  "mutation_probability": 0.3,
  "inversion_probability": 0.3,
  "selection_best_percent": 0.1,
  "elitist_strategy_percent": 0.1,
  "size_of_tournament": 5,
  "selection_name": "tournament",
  "crossover_name": "two_points",
  "mutation_name": "two_points"
}
@csrf_exempt 
def classic_EA_api(request):
    """Api endpoint controller for classical evolution-algorithm"""
    if request.method == "POST":
        required_params = ("number_of_population", "length_of_chromosome", "epochs", "cross_probability", "mutation_probability", "inversion_probability",
                           "selection_best_percent", "elitist_strategy_percent", "size_of_tournament", "selection_name", "crossover_name", "mutation_name")
        try:
            data = json.loads(request.body)
            print(data)
            if not all(param in data for param in required_params):
                return JsonResponse({"message": "Missing at least one of required params"})
            classicEA_obj = ClassicEA(**data)
            classicEA_obj.run()
            return JsonResponse({"message": "Processed successfully"})
        except Exception as error:
            print(f"Classic_EA error: {error}")
            return JsonResponse({"message": "an error has occurred in the classical evolution algorithm"})