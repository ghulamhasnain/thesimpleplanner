from contextlib import closing
from itertools import product
from time import strftime
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .helpers import *

class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		user = request.user
		return render(request, 'dashboard.html', {'user': user})

class Products(LoginRequiredMixin, View):
	def get(self, request):
		products = Product.objects.filter(user__username = request.user.username).order_by('itemcode')
		return render(request, 'products.html', {'products': products})

class EditProduct(LoginRequiredMixin, View):
	def get(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		return render(request, 'product-edit.html', {'product': product})
	
	def post(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		name = request.POST.get('name')
		batch_size = request.POST.get('batch_size')
		uom = request.POST.get('unit_of_measure')
		selling_price = request.POST.get('selling_price')
		
		product.name = name if regex_pattern_match(name_regex_pattern, name) else ''
		product.batch_size = batch_size if regex_pattern_match(float_regex_pattern, batch_size) else 1
		product.unit_of_measure = uom if regex_pattern_match(uom_regex_pattern, uom) else ''
		product.selling_price = selling_price if regex_pattern_match(float_regex_pattern, selling_price) else 0
		
		if name != '':
			product.save()
		return redirect('/planning/products')

class AddProduct(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'product-add.html')
	
	def post(self, request):
		import re

		product = Product()
		itemcode = request.POST.get('itemcode')
		name = request.POST.get('name')
		batch_size = request.POST.get('batch_size')
		uom = request.POST.get('unit_of_measure')
		selling_price = request.POST.get('selling_price')

		product.user = request.user
		product.itemcode = itemcode.lower() if regex_pattern_match(itemcode_regex_pattern, itemcode) else ''
		product.name = name if regex_pattern_match(name_regex_pattern, name) else ''
		product.batch_size = batch_size if regex_pattern_match(float_regex_pattern, batch_size) else 1
		product.unit_of_measure = uom if regex_pattern_match(uom_regex_pattern, uom) else ''
		product.selling_price = selling_price if regex_pattern_match(float_regex_pattern, selling_price) else 0
		
		if itemcode != '' and name != '':
			try:
				product.save()
				return redirect('/planning/products')
			except:
				error = 'This item code is already in use. Kindly choose another item code.'
				return render(request, 'product-add.html', {'error': error})
		else:
			error = 'The item code and name fields need to be filled'
			return render(request, 'product-add.html', {'error': error})

class ViewProduct(LoginRequiredMixin, View):
	def get(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		bom_list = BillOfMaterial.objects.filter(product = product)
		return render(request, 'product-view.html', {'product': product, 'bom_list': bom_list})

class DeleteProduct(LoginRequiredMixin, View):
	def post(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		product.delete()
		return redirect('/planning/products')

class Materials(LoginRequiredMixin, View):
	def get(self, request):
		materials = Material.objects.filter(user__username = request.user.username).order_by('itemcode')
		return render(request, 'materials.html', {'materials': materials})

class EditMaterial(LoginRequiredMixin, View):
	def get(self, request, materialItemCode):
		materialItemCode = materialItemCode.lower()
		material = Material.objects.get(itemcode = materialItemCode)
		return render(request, 'material-edit.html', {'material': material})
	
	def post(self, request, materialItemCode):
		materialItemCode = materialItemCode.lower()
		material = Material.objects.get(itemcode = materialItemCode)
		name = request.POST.get('name')
		lead_time = request.POST.get('lead_time')
		moq = request.POST.get('minimum_order_quantity')
		uom = request.POST.get('unit_of_measure')
		cost = request.POST.get('cost')
		
		material.name = name if regex_pattern_match(name_regex_pattern, name) else ''
		material.lead_time = lead_time if regex_pattern_match(integer_regex_pattern, lead_time) else 1
		material.minimum_order_quantity = moq if regex_pattern_match(integer_regex_pattern, moq) else 1
		material.unit_of_measure = uom if regex_pattern_match(uom_regex_pattern, uom) else ''
		material.cost = cost if regex_pattern_match(float_regex_pattern, cost) else 0
		
		if name != '':
			material.save()
		return redirect('/planning/materials')

class DeleteMaterial(LoginRequiredMixin, View):
	def post(self, request, materialItemCode):
		materialItemCode = materialItemCode.lower()
		material = Material.objects.get(itemcode = materialItemCode)
		material.delete()
		return redirect('/planning/materials')

class AddMaterial(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'material-add.html')
	
	def post(self, request):
		import re

		material = Material()
		itemcode = request.POST.get('itemcode')
		name = request.POST.get('name')
		lead_time = request.POST.get('lead_time')
		moq = request.POST.get('minimum_order_quantity')
		uom = request.POST.get('unit_of_measure')
		cost = request.POST.get('cost')

		material.user = request.user
		material.itemcode = itemcode.lower() if regex_pattern_match(itemcode_regex_pattern, itemcode) else ''
		material.name = name if regex_pattern_match(name_regex_pattern, name) else ''
		material.lead_time = lead_time if regex_pattern_match(integer_regex_pattern, lead_time) else 1
		material.minimum_order_quantity = moq if regex_pattern_match(integer_regex_pattern, moq) else 1
		material.unit_of_measure = uom if regex_pattern_match(uom_regex_pattern, uom) else ''
		material.cost = cost if regex_pattern_match(float_regex_pattern, cost) else 0
		
		if itemcode != '' and name != '':
			try:
				material.save()
				return redirect('/planning/materials')
			except:
				error = 'This item code is already in use. Kindly choose another item code.'
				return render(request, 'material-add.html', {'error': error})
		else:
			error = 'The item code and name fields need to be filled'
			return render(request, 'material-add.html', {'error': error})

class BillOfMaterials(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'bom.html')

class AddBillOfMaterials(LoginRequiredMixin, View):
	def get(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		materials = Material.objects.filter(user__username = request.user.username)
		bom_list = BillOfMaterial.objects.filter(product = product)
		if len(bom_list) > 0:
			return redirect('/planning/bom/'+productItemCode+'/edit')
		return render(request, 'bom-add.html', {'product': product, 'materials': materials})
	
	def post(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		materials = Material.objects.filter(user__username = request.user.username)
		bom_list = []
		for m in materials:
			base_quantity_post = request.POST.get(m.itemcode)
			base_quantity = float(base_quantity_post) if regex_pattern_match(float_regex_pattern, base_quantity_post) else 0
			if base_quantity > 0:
				bom = BillOfMaterial()
				bom.user = request.user
				bom.product = product
				bom.material = m
				bom.base_quantity = base_quantity
				bom_list.append(bom)
		if len(bom_list) > 0:
			BillOfMaterial.objects.bulk_create(bom_list)
		return redirect('/planning/products/'+productItemCode+'/view')

class EditBillOfMaterials(LoginRequiredMixin, View):
	def get(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		materials = Material.objects.filter(user__username = request.user.username)
		bom_list = BillOfMaterial.objects.filter(product = product)
		if len(bom_list) == 0:
			return redirect('/planning/bom/'+productItemCode+'/add')
		return render(request, 'bom-edit.html', {'product': product, 'materials': materials, 'bom_list': bom_list})
	
	def post(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		bom_list = BillOfMaterial.objects.filter(product = product)
		if len(bom_list) > 0:
			for bom in bom_list:	
				base_quantity_post = request.POST.get(bom.material.itemcode)
				base_quantity = float(base_quantity_post) if regex_pattern_match(float_regex_pattern, base_quantity_post) else 0
				bom.base_quantity = base_quantity
			BillOfMaterial.objects.bulk_update(bom_list, ['base_quantity'])
		return redirect('/planning/products/'+productItemCode+'/view')

class DeleteBillOfMaterials(LoginRequiredMixin, View):
	def post(self, request, productItemCode):
		productItemCode = productItemCode.lower()
		product = Product.objects.get(itemcode = productItemCode)
		bom_list = BillOfMaterial.objects.filter(product = product).delete()
		return redirect('/planning/products/'+productItemCode+'/view')

class Inventories(LoginRequiredMixin, View):
	def get(self, request):
		materials = Material.objects.filter(user = request.user)
		products = Product.objects.filter(user = request.user)
		materials_inv = []
		products_inv = []
		for m in materials:
			inv = Inventory.objects.get_or_create(material = m, defaults = {'user': request.user, 'stock': 0})
			materials_inv.append(inv)
		for p in products:
			inv = Inventory.objects.get_or_create(product = p, defaults = {'user': request.user, 'stock': 0})
			products_inv.append(inv)
		return render(request, 'inventory.html', {'materials_inv': materials_inv, 'products_inv': products_inv})

class EditProductsInventories(LoginRequiredMixin, View):
	def get(self, request):
		products = Product.objects.filter(user = request.user)
		products_inv = []
		for p in products:
			inv = Inventory.objects.get_or_create(product = p, defaults = {'user': request.user, 'stock': 0})
			products_inv.append(inv)
		return render(request, 'edit-products-inventory.html', {'products_inv': products_inv})
	
	def post(self, request):
		products = Product.objects.filter(user = request.user)
		products_inv = []
		for p in products:
			inv = Inventory.objects.get(product = p)
			stock_post = request.POST.get(p.itemcode)
			stock = float(stock_post) if regex_pattern_match(float_regex_pattern, stock_post) else 0
			if inv.stock != stock:
				inv.stock = stock
				products_inv.append(inv)
		Inventory.objects.bulk_update(products_inv, ['stock'])
		return redirect('/planning/inventory')

class EditMaterialsInventories(LoginRequiredMixin, View):
	def get(self, request):
		materials = Material.objects.filter(user = request.user)
		materials_inv = []
		for m in materials:
			inv = Inventory.objects.get_or_create(material = m, defaults = {'user': request.user, 'stock': 0})
			materials_inv.append(inv)
		return render(request, 'edit-materials-inventory.html', {'materials_inv': materials_inv})
	
	def post(self, request):
		materials = Material.objects.filter(user = request.user)
		materials_inv = []
		for m in materials:
			inv = Inventory.objects.get(material = m)
			stock_post = request.POST.get(m.itemcode)
			stock = float(stock_post) if regex_pattern_match(float_regex_pattern, stock_post) else 0
			if inv.stock != stock:
				inv.stock = stock
				materials_inv.append(inv)
		Inventory.objects.bulk_update(materials_inv, ['stock'])
		return redirect('/planning/inventory')

class Forecasts(LoginRequiredMixin, View):
	def get(self, request):
		products = Product.objects.filter(user = request.user)
		forecasts_list = []
		for p in products:
			forecast = Forecast.objects.get_or_create(product = p, defaults = {'user': request.user, 'quantity': 0})
			forecasts_list.append(forecast)
		return render(request, 'forecasts.html', {'forecasts_list': forecasts_list})

class EditForecasts(LoginRequiredMixin, View):
	def get(self, request):
		products = Product.objects.filter(user = request.user)
		forecasts_list = []
		for p in products:
			forecast = Forecast.objects.get_or_create(product = p, defaults = {'user': request.user, 'quantity': 0})
			forecasts_list.append(forecast)
		return render(request, 'edit-forecasts.html', {'forecasts_list': forecasts_list})
	
	def post(self, request):
		products = Product.objects.filter(user = request.user)
		forecasts_list = []
		for p in products:
			forecast = Forecast.objects.get(product = p)
			quantity_post = request.POST.get(p.itemcode)
			quantity = float(quantity_post) if regex_pattern_match(float_regex_pattern, quantity_post) else 0
			if forecast.quantity != quantity:
				forecast.quantity = quantity
				forecasts_list.append(forecast)
		Forecast.objects.bulk_update(forecasts_list, ['quantity'])
		return redirect('/planning/forecasts')

class ReorderingPlans(LoginRequiredMixin, View):
	def get(self, request):
		plans = ReorderingPlan.objects.filter(user = request.user)
		return render(request, 'reordering-plans.html', {'plans': plans})

class ViewReorderingPlan(LoginRequiredMixin, View):
	def get(self, request, planId):
		plan = ReorderingPlan.objects.get(id = planId)
		plan_lines = ReorderingPlanLine.objects.filter(plan = plan)
		return render(request, 'reordering-plan-view.html', {'plan': plan, 'plan_lines': plan_lines})

class DeleteReorderingPlan(LoginRequiredMixin, View):
	def get(self, request, planId):
		plan = ReorderingPlan.objects.get(id = planId)
		plan_lines = ReorderingPlanLine.objects.filter(plan = plan)
		plan_lines.delete()
		plan.delete()
		return redirect('/planning/reordering')

class AddReorderingPlan(LoginRequiredMixin, View):
	def get(self, request):
		import math

		materials = Material.objects.filter(user = request.user)
		table_list = []
		for m in materials:
			bom_list = BillOfMaterial.objects.filter(material = m)
			forecast = 0
			for bom in bom_list:
				product_forecast = Forecast.objects.get(product = bom.product).quantity
				base_quantity = bom.base_quantity
				batch_size = bom.product.batch_size
				forecast_calculation = product_forecast * base_quantity / batch_size
				forecast = forecast + forecast_calculation
			
			safety_stock_days = m.lead_time + 1
			current_inventory = Inventory.objects.get(material = m).stock
			safety_stock = math.ceil(forecast * (safety_stock_days / 30))
			minimum_order_quantity = m.minimum_order_quantity
			proposal = 0 if current_inventory > safety_stock + forecast else math.ceil((safety_stock + forecast - current_inventory)/minimum_order_quantity) * minimum_order_quantity
			closing_inventory = current_inventory - forecast + proposal

			mat_plan = ReorderingPlan()
			mat_plan.user = request.user
			mat_plan.material = m
			mat_plan.minimum_order_quantity = minimum_order_quantity
			mat_plan.lead_time = m.lead_time
			mat_plan.safety_stock_days = safety_stock_days
			mat_plan.current_inventory = current_inventory
			mat_plan.forecast = forecast
			mat_plan.safety_stock = safety_stock
			mat_plan.proposal = proposal
			mat_plan.closing_inventory = closing_inventory
			
			table_list.append(mat_plan)
		return render(request, 'reordering-plan-add.html', {'table_list': table_list})

	def post(self, request):
		from datetime import datetime

		name_post = request.POST.get('name')
		contingency_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		mat_plan = ReorderingPlan()
		mat_plan.user = request.user
		mat_plan.name = name_post if regex_pattern_match(plan_regex_pattern, name_post) else 'Reorderplan ' + contingency_name

		materials = Material.objects.filter(user = request.user)
		table_list = []

		for m in materials:
			mat_plan_line = ReorderingPlanLine()
			itemcode = m.itemcode
			moq_post = request.POST.get(itemcode+'_moq')
			lead_time_post = request.POST.get(itemcode+'_lead_time')
			safety_stock_days_post = request.POST.get(itemcode+'_safety_stock_days')
			current_inventory_post = request.POST.get(itemcode+'_current_inventory')
			forecast_post = request.POST.get(itemcode+'_forecast')
			safety_stock_post = request.POST.get(itemcode+'_safety_stock')
			proposal_post = request.POST.get(itemcode+'_proposal')
			closing_inventory_post = request.POST.get(itemcode+'_closing_inventory')

			mat_plan_line.plan = mat_plan
			mat_plan_line.material = m
			mat_plan_line.minimum_order_quantity = stringToInt(moq_post) if regex_pattern_match(integer_regex_pattern, str(stringToInt(moq_post))) else 0
			mat_plan_line.lead_time = stringToInt(lead_time_post) if regex_pattern_match(integer_regex_pattern, str(stringToInt(lead_time_post))) else 0
			mat_plan_line.safety_stock_days = stringToInt(safety_stock_days_post) if regex_pattern_match(integer_regex_pattern, str(stringToInt(safety_stock_days_post))) else 0
			mat_plan_line.current_inventory = stringToFloat(current_inventory_post) if regex_pattern_match(float_regex_pattern, str(stringToFloat(current_inventory_post))) else 0
			mat_plan_line.forecast = stringToFloat(forecast_post) if regex_pattern_match(float_regex_pattern, str(stringToFloat(forecast_post))) else 0
			mat_plan_line.safety_stock = stringToInt(safety_stock_post) if regex_pattern_match(integer_regex_pattern, str(stringToInt(safety_stock_post))) else 0
			mat_plan_line.proposal = stringToInt(proposal_post) if regex_pattern_match(integer_regex_pattern, str(stringToInt(proposal_post))) else 0
			mat_plan_line.closing_inventory = stringToFloat(closing_inventory_post) if regex_pattern_match(float_regex_pattern, str(stringToFloat(closing_inventory_post))) else 0

			table_list.append(mat_plan_line)
		mat_plan.save()
		ReorderingPlanLine.objects.bulk_create(table_list)
		return redirect('/planning/reordering')
