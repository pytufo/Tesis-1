from django.db import models
from accounts.models import User

from django.urls import reverse


class Cuota(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2,blank=False, null=False)
    created_by = models.ForeignKey(User, related_name="Tesorero", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="Cobros", on_delete=models.CASCADE)

    def get_absoulte_url(self):
        return reverse("cobros-view", args=[str(self.id)])
    
    def __str__(self):
        return str(self.owner.email)
    
    class Meta:
        ordering = ["-fecha"]