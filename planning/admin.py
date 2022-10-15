from django.contrib import admin
from .models import *

# Register your models here
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(BillOfMaterial)
admin.site.register(Inventory)
admin.site.register(Forecast)
admin.site.register(ProductionPlan)
admin.site.register(ProductionPlanLine)
admin.site.register(ReorderingPlan)
admin.site.register(ReorderingPlanLine)