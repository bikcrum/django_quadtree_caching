from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "user"

class Location(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "location"
