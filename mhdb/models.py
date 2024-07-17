from django.db import models

# Create your models here.


class Genre(models.Model):

    name=models.CharField(max_length=200,unique=True)


    def __str__(self):

        return self.name
    
class Director(models.Model):

    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name
    
class Actor(models.Model):

    name=models.CharField(max_length=200)

    def __str__(self):

        return self.name

class Movie(models.Model):

    tile=models.CharField(max_length=200)

    year=models.CharField(max_length=100)

    actor_object=models.ManyToManyField(Actor)

    director_object=models.ForeignKey(Director,on_delete=models.CASCADE)

    genre_object=models.ManyToManyField(Genre)

    def __str__(self):

        return self.tile



