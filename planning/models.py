from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Material(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    itemcode = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=64)
    lead_time = models.IntegerField(default=1)
    minimum_order_quantity = models.IntegerField(default=1)
    unit_of_measure = models.CharField(max_length=16, default='')
    cost = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.itemcode

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    itemcode = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=64)
    batch_size = models.FloatField(default=1)
    unit_of_measure = models.CharField(max_length=16, default='')
    selling_price = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.itemcode

class BillOfMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_bom', null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='material_bom', null=True, blank=True)
    base_quantity = models.FloatField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.itemcode

class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_inventory', null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='material_inventory', null=True, blank=True)
    stock = models.FloatField(default = 0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return self.product.itemcode
        else:
            return self.material.itemcode

class Forecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_forecast', null=True, blank=True)
    quantity = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.itemcode

class ProductionPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64, default='')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductionPlanLine(models.Model):
    plan = models.ForeignKey(ProductionPlan, on_delete=models.PROTECT, related_name='production_plan', null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_production', null=True, blank=True)
    batch_size = models.FloatField(default=1)
    safety_stock_days = models.IntegerField(default=1)
    current_inventory = models.FloatField(default = 0)
    forecast = models.FloatField(default=0)
    safety_stock = models.FloatField(default = 0)
    batches = models.FloatField(default = 0)
    quantity = models.FloatField(default = 0)
    closing_inventory = models.FloatField(default = 0)
    closing_inventory_days = models.IntegerField(default=1)

    def __str__(self):
        return self.plan.name + ' ' + self.product.name

class ReorderingPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64, default='')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ReorderingPlanLine(models.Model):
    plan = models.ForeignKey(ReorderingPlan, on_delete=models.PROTECT, related_name='reordering_plan', null=False, blank=False)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='material_reordering', null=True, blank=True)
    minimum_order_quantity = models.IntegerField(default=1)
    lead_time = models.IntegerField(default=1)
    safety_stock_days = models.IntegerField(default=1)
    current_inventory = models.FloatField(default = 0)
    forecast = models.FloatField(default=0)
    safety_stock = models.FloatField(default = 0)
    proposal = models.FloatField(default=0)
    closing_inventory = models.FloatField(default = 0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan.name + ' ' + self.material.name