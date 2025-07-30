from django.db import models
from django.core.exceptions import ValidationError


class Node(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Relation(models.Model):
    origin = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='origins', db_index=True)
    destination = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='destinations')

    weight = models.IntegerField(default=1)

    data = models.TextField()

    created_at = models.DateTimeField(auto_now=True,)

    class Meta:
        unique_together = ('origin', 'destination')
        ordering = ['origin']

    def __str__(self):
        return f"{self.origin} -> {self.destination} (weight {self.weight})"

    def save(self, *args, **kwargs):
        if self.origin.id == self.destination.id:
            raise ValidationError("Origin and destination cannot be the same.")
        super(Relation, self).save(*args, **kwargs)
