from django.utils import timezone
import random
from django.test import TestCase
from .models import Player, Round, HoleScore, Course, Tee
from django.urls import reverse

# Create your tests here.

def create_random_holescore(roundID, holeNumber, holeScore, tee):
    """
    Creates a Hole with mostly random values.  holeScore is intended to be optional, provide
    a value if you want the hole to have a particular score.
    """
    if holeScore > 0:
        return HoleScore.objects.create(round=roundID, course=tee.course, par=random.randint(3,5), score= holeScore, fir=random.randint(0,1),
                               putts=random.randint(1,3), penalties=random.randint(0,1), number=holeNumber)
    
    else:
        return HoleScore.objects.create(round=roundID, par=random.randint(3,5), score= random.randint(2,7), fir=random.randint(0,1),
                               putts=random.randint(1,3), penalties=random.randint(0,1), number=holeNumber)
    

def create_round(golfer, tee):
    return Round.objects.create(player=golfer, play_date = timezone.now(), tee_played = tee, notes = "I played great today")

def create_course():
    return Course.objects.create(name="Maplewood")

def create_round_with_holes(golfer, holeScore):
    tee = create_tee(create_course())
    round = create_round(golfer=golfer, tee=tee)

    for x in range(18):
        create_random_holescore(round, x+1, holeScore=holeScore, tee=tee)
    return round

def create_tee(course):
    tee = Tee.objects.create(course=course, name = "Blue", yardage = 6000, slope = 120)
    return tee

class RoundModelTests(TestCase):
    def test_total_score_calculation(self):
        """
        total_score adds all the scores of holes where the pk of the Hole is the Round.
        Make sure its doing the math right.
        """
        player = Player.objects.create(name="Wyatt")
        
        round = create_round_with_holes(golfer=player, holeScore=4)
        self.assertEqual(round.total_score(), 72)

        round = create_round_with_holes(golfer=player, holeScore=5)
        self.assertEqual(round.total_score(), 90)


class HoleModelTests(TestCase):
    def test_gir_calculation(self):
        """
        A GIR is found when a player hits the green on a hole in (par - 2) shots or fewer.
        """
        course = create_course()
        round = create_round(Player.objects.create(name="Wyatt"), create_tee(course=create_course()))
        hole = HoleScore.objects.create(round=round, course=course, number=1, fir=True, penalties=0, par=3, putts=2, score=3)
        self.assertTrue(hole.gir())

        hole = HoleScore.objects.create(round=round, course=course, number=1, fir=True, penalties=0, par=4, putts=3, score=5)
        self.assertTrue(hole.gir())

        hole = HoleScore.objects.create(round=round, course=course, number=1, fir=True, penalties=0, par=4, putts=2, score=5)
        self.assertFalse(hole.gir())

        hole = HoleScore.objects.create(round=round, course=course, number=1, fir=True, penalties=0, par=5, putts=4, score=6)
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