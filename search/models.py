from django.db import models

class Paragraph(models.Model):
    paragraph = models.CharField(max_length=5000)

class Word(models.Model):
    word = models.CharField(max_length=50, unique=True)

class WordParagraphMap(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    count = models.IntegerField()
