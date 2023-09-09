from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Nest(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participants',blank=True) 
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # '-' is used to create nests in descending order means newest one on top
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nest = models.ForeignKey(Nest, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
    # '-' is used to create messages in ascending order means newest one on top
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[0:50]

class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nest = models.ForeignKey(Nest, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
    # '-' is used to create messages in ascending order means newest one on top
      ordering = ['updated', 'created']
