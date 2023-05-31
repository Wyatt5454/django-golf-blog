from django.utils import timezone
import random
from django.test import TestCase
from .models import Player, Round, Hole
from django.urls import reverse

# Create your tests here.

def create_random_hole(roundID, holeNumber, holeScore):
    """
    Creates a Hole with mostly random values.  holeScore is intended to be optional, provide
    a value if you want the hole to have a particular score.
    """
    if holeScore > 0:
        return Hole.objects.create(round=roundID, par=random.randint(3,5), score= holeScore, fir=random.randint(0,1),
                               putts=random.randint(1,3), penalties=random.randint(0,1), number=holeNumber)
    
    else:
        return Hole.objects.create(round=roundID, par=random.randint(3,5), score= random.randint(2,7), fir=random.randint(0,1),
                               putts=random.randint(1,3), penalties=random.randint(0,1), number=holeNumber)
    

def create_round(golfer, course):
    return Round.objects.create(player=golfer, play_date = timezone.now(), course = "Maplewood", notes = "I played great today")

def create_round_with_holes(golfer, course, holeScore):
    round = create_round(golfer=golfer, course=course)

    for x in range(18):
        create_random_hole(round, x+1, holeScore=holeScore)
    return round

class RoundModelTests(TestCase):
    def test_total_score_calculation(self):
        """
        total_score adds all the scores of holes where the pk of the Hole is the Round.
        Make sure its doing the math right.
        """
        player = Player.objects.create(name="Wyatt")
        course = "Maplewood"
        round = create_round_with_holes(golfer=player, course=course, holeScore=4)
        self.assertEqual(round.total_score(), 72)

        round = create_round_with_holes(golfer=player, course=course, holeScore=5)
        self.assertEqual(round.total_score(), 90)


class HoleModelTests(TestCase):
    def test_gir_calculation(self):
        """
        A GIR is found when a player hits the green on a hole in (par - 2) shots or fewer.
        """
        round = create_round(Player.objects.create(name="Wyatt"), "butts")
        hole = Hole.objects.create(round=round, number=1, fir=True, penalties=0, par=3, putts=2, score=3)
        self.assertTrue(hole.gir())

        hole = Hole.objects.create(round=round, number=1, fir=True, penalties=0, par=4, putts=3, score=5)
        self.assertTrue(hole.gir())

        hole = Hole.objects.create(round=round, number=1, fir=True, penalties=0, par=4, putts=2, score=5)
        self.assertFalse(hole.gir())

        hole = Hole.objects.create(round=round, number=1, fir=True, penalties=0, par=5, putts=4, score=6)
        self.assertTrue(hole.gir())

class RoundIndexViewTests(TestCase):
    def test_no_rounds(self):
        """
        If there's no rounds of golf, an appropriate message is displayed
        """
        response = self.client.get(reverse("rounds:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Rounds available")
        self.assertQuerySetEqual(response.context["round_list"], [])