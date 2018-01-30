from django.db import models

class Photo(models.Model):
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=120)
    pic = models.ForeignKey(Photo,on_delete=models.DO_NOTHING,null=True,blank=True)
    summary = models.TextField()
    des = models.TextField()

    def __str__(self):
        return self.title

class View(models.Model):
    ip = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip