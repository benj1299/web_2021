from django.contrib import admin
from comparator.models import Operators

class OperatorsAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Operators"

admin.site.register(Operators, OperatorsAdmin)