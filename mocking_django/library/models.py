from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    page_length = models.IntegerField()
    authors = models.ManyToManyField('library.Author', related_name="books")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["page_length"]
