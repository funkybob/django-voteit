from django.db import models


class VotableQuerySet(models.QuerySet):

    def with_tally(self):
        return self.annotate(tally=models.Sum('votes__weight'))
