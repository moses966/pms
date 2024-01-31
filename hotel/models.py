from django.db import models

class Room(models.Model):
    name = models.CharField(
        max_length=30,
    )
    description = models.TextField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
