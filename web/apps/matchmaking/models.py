from django.db import models


class League(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True, editable=False)
    name = models.CharField(null=False, unique=True, max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
