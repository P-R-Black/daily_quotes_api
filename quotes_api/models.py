from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)
    date_posted = models.DateField(null=True, blank=True)


    def __str__(self):
        return f'"{self.text}" - {self.author.name}'
