from django.db import models

class Remove(models.Model):
    number = models.PositiveIntegerField()


class PileUp(models.Model):
    number = models.PositiveIntegerField()