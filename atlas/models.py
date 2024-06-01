from django.db import models


class Atlas(models.Model):
    STACK = ((0, "Unknown"), (4, "IPv4"), (6, "IPv6"))
    unicodetld = models.CharField(max_length=100)
    stack = models.IntegerField(default=0, choices=STACK)
    measurement = models.IntegerField(default=0, blank=True, null=True)
    lastEdition = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unicodetld

    class Meta:
        indexes = [
            models.Index(fields=['stack', 'unicodetld']),
        ]
