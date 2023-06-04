from django.db import models
from django.urls import reverse

# Course class.  Used as a  primary key for Tees and Holes.
class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self) -> str:
        return self.name
    def get_absolute_url(self):
        return reverse("course", kwargs={"slug": self.slug})

class Hole(models.Model):
    number = models.PositiveIntegerField()
    par = models.PositiveIntegerField()

# Player class.  Used as a primary key to find Rounds
class Player(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class Tee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    yardage = models.PositiveIntegerField()
    slope = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.course.__str__() + " : " + self.name

class Round(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tee_played = models.ForeignKey(Tee, on_delete=models.CASCADE)
    play_date = models.DateTimeField("date played")
    notes = models.CharField(max_length=500)

    def total_score(self):
        holes = HoleScore.objects.filter(round=self)
        score = 0
        for hole in holes:
            score += hole.score
        return score

class HoleScore(Hole):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    fir = models.BooleanField()
    putts = models.PositiveIntegerField()
    penalties = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.number) + " : " + str(self.score)
    
    def gir(self):
        return (self.score - self.putts) <= (self.par - 2)
    
class HoleDisplay(Hole):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    yardage = models.PositiveIntegerField()