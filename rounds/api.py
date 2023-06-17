from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views import generic
from .models import HoleScore, Round

def round_to_json(round):
    return {'id': round.id, 'player': round.player.name, 'tee_played': round.tee_played.name,
            'course': round.tee_played.course.name, 'score': round.total_score(),
            'play_date': round.play_date, 'notes': round.notes}

def hole_to_json(holeScore):
     return {'number': holeScore.number, 'par': holeScore.par, 'yardage': holeScore.yardage, 'score': holeScore.score, 'fir':holeScore.fir,
             'putts': holeScore.putts, 'penalties': holeScore.penalties}

class APIView(generic.ListView):    
    
    def all_rounds(request):
        rounds = Round.objects.all()  # Fetch the rounds from the database

        # Convert rounds to JSON format
        rounds_data = [ round_to_json(round) for round in rounds]

        return JsonResponse(rounds_data, safe=False)
    
    def round_by_pk(request, round_id):
        # Get the round then use it to get all the HoleScores
        round = get_object_or_404(Round, id=round_id)
        holes = get_list_or_404(HoleScore, round=round)

        # Convert all the holes to json format
        score_data = [ hole_to_json(hole) for hole in holes ]

        return JsonResponse(score_data, safe=False)