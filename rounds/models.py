from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class Round(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    play_date = models.DateTimeField("date played")
    notes = models.CharField(max_length=500)

    def total_score(self):
        holes = Hole.objects.filter(round=self)
        score = 0
        for hole in holes:
            score += hole.score
        return score


class Hole(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    par = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    fir = models.BooleanField()
    putts = models.PositiveIntegerField()
    penalties = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.number) + " : " + str(self.score)
    
    def gir(self):
        return (self.score - self.putts) <= (self.par - 2)