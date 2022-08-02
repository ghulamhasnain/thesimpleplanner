"""foamsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from . import views

urlpatterns = [
	path('dashboard', views.Dashboard.as_view(), name='dashboard'),

    path('products', views.Products.as_view(), name='products'),
    path('products/add', views.AddProduct.as_view(), name='add_product'),
    path('products/<slug:productItemCode>/edit', views.EditProduct.as_view(), name='edit_product'),
    path('products/<slug:productItemCode>/view', views.ViewProduct.as_view(), name='view_product'),
    path('products/<slug:productItemCode>/delete', views.DeleteProduct.as_view(), name='delete_product'),

    path('materials', views.Materials.as_view(), name='materials'),
    path('materials/add', views.AddMaterial.as_view(), name='add_material'),
    path('materials/<slug:materialItemCode>/view', views.ViewMaterial.as_view(), name='view_material'),
    path('materials/<slug:materialItemCode>/edit', views.EditMaterial.as_view(), name='edit_material'),
    path('materials/<slug:materialItemCode>/delete', views.DeleteMaterial.as_view(), name='delete_material'),
    
    path('bom', views.BillOfMaterials.as_view(), name='bom'),
    path('bom/<slug:productItemCode>/add', views.AddBillOfMaterials.as_view(), name='add_bom'),
    path('bom/<slug:productItemCode>/edit', views.EditBillOfMaterials.as_view(), name='edit_bom'),
    path('bom/<slug:productItemCode>/delete', views.DeleteBillOfMaterials.as_view(), name='delete_bom'),

    path('inventory', views.Inventories.as_view(), name='inventory'),
    path('inventory/products/edit', views.EditProductsInventories.as_view(), name='edit_product_inventories'),
    path('inventory/materials/edit', views.EditMaterialsInventories.as_view(), name='edit_material_inventories'),

    path('forecasts', views.Forecasts.as_view(), name='forecasts'),
    path('forecasts/edit', views.EditForecasts.as_view(), name='edit_forecasts'),

    path('reordering', views.ReorderingPlans.as_view(), name='reordering_plan'),
    path('reordering/<slug:planId>/view', views.ViewReorderingPlan.as_view(), name='view_reordering_plan'),
    path('reordering/<slug:planId>/delete', views.DeleteReorderingPlan.as_view(), name='delete_reordering_plan'),
    path('reordering/add', views.AddReorderingPlan.as_view(), name='add_reordering_plan')
]