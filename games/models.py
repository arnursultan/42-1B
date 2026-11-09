from django.db import models

class Game(models.Model):
    title       = models.CharField(max_length=120)
    genre       = models.CharField(max_length=50, default='unknown')
    rating      = models.FloatField(default=0)
    released    = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title