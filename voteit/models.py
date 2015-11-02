from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from . import managers


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    weight = models.IntegerField(default=1)

    objects = managers.VotableQuerySet.as_manager()

    class Meta:
        unique_together = (
            ('user', 'content_type', 'object_id'),
        )


class Votable(models.Model):
    votes = GenericRelation('Vote')

    class Meta:
        abstract = True

    @cached_property
    def tally(self):
        return self.votes.aggregate(Sum('weight')).values()[0]
