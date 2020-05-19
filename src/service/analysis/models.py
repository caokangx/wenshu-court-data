from django.db import models


# Create your models here.
class Document(models.Model):
    docId = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    name = models.CharField(max_length=99999)
    court = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    causeOfAction = models.CharField(max_length=100)
    processing = models.CharField(max_length=100)
    litigant = models.CharField(max_length=100)
    productName = models.CharField(max_length=100)
    criteria = models.CharField(max_length=100)
    publishDate = models.DateTimeField()

class Product(models.Model):

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
