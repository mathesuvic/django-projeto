from decimal import Decimal
from django.db import models

CATEGORIA = [
    ("OBR", "Obrigatório"),
    ("REG", "Regulatório"),
    ("ESS", "Essencial"),
    ("IMP", "Importante"),
]

class Plan(models.Model):
    code = models.CharField(max_length=50)              # ex.: 1.1.2
    name = models.CharField(max_length=255)             # ex.: Linhas de Transmissão
    categoria = models.CharField(max_length=3, choices=CATEGORIA, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    rev3_meta = models.DecimalField(max_digits=16, decimal_places=3, default=Decimal("0.000"))  # R$ mil
    responsavel = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("parent", "code")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class MonthlyCapex(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="mensal")
    year = models.PositiveIntegerField(default=2025)
    mes = models.PositiveSmallIntegerField()  # 1..12
    realizado = models.DecimalField(max_digits=16, decimal_places=3, default=Decimal("0.000"))
    previsto = models.DecimalField(max_digits=16, decimal_places=3, default=Decimal("0.000"))

    class Meta:
        unique_together = ("plan", "year", "mes")
        ordering = ["plan__code", "mes"]

class Transferencia(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="transferencias")
    year = models.PositiveIntegerField(default=2025)
    valor = models.DecimalField(max_digits=16, decimal_places=3, default=Decimal("0.000"))  # +recebe / -envia
    de_para = models.TextField(blank=True)

    class Meta:
        unique_together = ("plan", "year")