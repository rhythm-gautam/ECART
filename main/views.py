from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
import datetime
from administrator.models import *
from django.http import HttpResponse
import json


def Register(request):
	if(request.method=='GET'):
		return render(request,'main/register.html',None)
	else:
		login=Login()
		login.email=request.POST.get('email')
		login.password=request.POST.get('password')
		login.isactive=True
		login.save()

		customer=Customer()
		customer.loginid=login
		customer.name=request.POST.get('name')
		customer.gender=request.POST.get('gender')
		customer.phone=request.POST.get('phone')
		customer.save()

		address=ShippingAddress()
		address.loginid=login
		address.title=request.POST.get('title')
		address.hno=request.POST.get('hno')
		address.area=request.POST.get('area')
		address.city=request.POST.get('city')
		address.pin=request.POST.get('pin')
		address.landmark=request.POST.get('landmark')
		return redirect('/')

def Home(request):
	products=Product.objects.filter()
	categories=Category.objects.filter(parentid=0)
	
	productlist=[]
	for product in products:
		image=ProductImage.objects.filter(productid=product.id)		
		if image.__len__()!=0:
			image=image[0].image
		else:
			image=""		
		product.image=image
		productlist.append(product)

	categorylist=[]
	for category in categories:
		name=category.name
		subcategories=Category.objects.filter(parentid=category.id)
		for subcategory in subcategories:			
			subcategory.numproducts=len(Product.objects.filter(categoryid=subcategory))
		categorylist.append({"name":name,"subcategories":subcategories})

	data={}
	data['products']=productlist
	data['categories']=categorylist

	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):
		try:
			activeLogin=ActiveLogin.objects.get(xtoken=xtoken)
			profile=Customer.objects.get(loginid=activeLogin.loginid)
			data['profile']=profile
		except:
			pass

	return render(request,"main/home.html",data)


def ProductDetails(request,id):
	product=Product.objects.get(id=id)
	images=ProductImage.objects.filter(productid=product.id)		
	product.images=[]
	for image in images:
		product.images.append(image.image)

	categories=Category.objects.filter(parentid=0)
	categorylist=[]
	for category in categories:
		name=category.name
		subcategories=Category.objects.filter(parentid=category.id)
		for subcategory in subcategories:			
			subcategory.numproducts=len(Product.objects.filter(categoryid=subcategory))
		categorylist.append({"name":name,"subcategories":subcategories})

	featurevalues=FeatureValue.objects.filter(productid=product)	

	highlights=[]
	if(product.categoryid.name=='Smart Phones'):
		for features in featurevalues:
			if(features.featureid.name=='Primary Camera'):
				highlights.append(features.value + " Primary Camera")
			if(features.featureid.name=='RAM'):
				highlights.append(features.value)
			if(features.featureid.name=='Color'):
				highlights.append(features.value + " Color")

	data={}

	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):
		try:
			activeLogin=ActiveLogin.objects.get(xtoken=xtoken)
			profile=Customer.objects.get(loginid=activeLogin.loginid)
			data['profile']=profile
		except:
			pass


	data['categories']=categorylist
	data['product']=product
	data['features']=featurevalues
	data['highlights']=highlights
	return render(request,'main/productdetails.html',data)


def CartList(request):
	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):

		categories=Category.objects.filter(parentid=0)
		categorylist=[]
		for category in categories:
			name=category.name
			subcategories=Category.objects.filter(parentid=category.id)
			categorylist.append({"name":name,"subcategories":subcategories})

		data={}
		data['categories']=categorylist

		activeLogin=ActiveLogin.objects.get(xtoken=xtoken)

		profile=Customer.objects.get(loginid=activeLogin.loginid)
		data['profile']=profile

		cart=Cart.objects.filter(loginid=activeLogin.loginid)

		grandtotal=0
		for i in range(len(cart)):
			cart[i].productid.tax=round(float(cart[i].productid.price)*.18,1)
			cart[i].productid.total=round(cart[i].productid.price,1)
			cart[i].productid.price=round(float(cart[i].productid.price)*.82,1)
			cart[i].productid.image=ProductImage.objects.filter(productid=cart[i].productid).first().image
			grandtotal=grandtotal+cart[i].productid.total
		data['cart']=cart
		data['grandtotal']=grandtotal
		return render(request,'main/cart.html',data)
	else:
		return redirect('/')



def AddCart(request,id):
	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):
		try:
			activeLogin=ActiveLogin.objects.get(xtoken=xtoken)
			if(id!="0"):
				product=Product.objects.get(id=id)
				if(Cart.objects.filter(productid=product,loginid=activeLogin.loginid).exists()):
					response='Duplicate Record'
				else:
					cart=Cart()
					cart.loginid=activeLogin.loginid
					cart.productid=product
					cart.save()
					response='Item Added'
			else:
				response='No Item Added'
			cart=Cart.objects.filter(loginid=activeLogin.loginid)
			response_data={'response':response,'cartitems':len(cart)}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		except:
			return HttpResponse('error')
	else:
		response_data={'response':'User Not Logged In','cartitems':-1}
		return HttpResponse(json.dumps(response_data), content_type="application/json")


def DeleteCart(request,id):
	cart=Cart.objects.filter(id=id)
	cart.delete()
	return redirect('/cart/')


def Users(request):
	logins=Login.objects.values_list()
	return HttpResponse(logins)


def LoginVerify(request):
	if(request.method=="GET"):
		return render(request,'main/login.html',None)
	else:
		email=request.POST.get('email')
		password=request.POST.get('password')
		login=Login.objects.filter(email=email,password=password).first()
		if(login):
			xtoken = get_random_string(length=32)
			activeLogin=ActiveLogin()
			activeLogin.loginid=login
			activeLogin.xtoken=xtoken
			activeLogin.datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			activeLogin.save()
			response=redirect('/')
			response.set_cookie('xtoken',xtoken,max_age=60*24*365)
			return response
		else:
			return HttpResponse('Login Failed')

def Logout(request):
	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):
		activeLogin=ActiveLogin.objects.get(xtoken=xtoken)
		activeLogin.delete()
		response=redirect('/')
		response.delete_cookie('xtoken')
		return response
	else:
		return redirect('/')


def CategoryWiseProducts(request,id):
	curcategory=Category.objects.get(id=id)
	products=Product.objects.filter(categoryid=curcategory)
	categories=Category.objects.filter(parentid=0)
	
	productlist=[]
	for product in products:
		image=ProductImage.objects.filter(productid=product.id)		
		if image.__len__()!=0:
			image=image[0].image
		else:
			image=""		
		product.image=image
		productlist.append(product)

	categorylist=[]
	for category in categories:
		name=category.name
		subcategories=Category.objects.filter(parentid=category.id)
		for subcategory in subcategories:			
			subcategory.numproducts=len(Product.objects.filter(categoryid=subcategory))
		categorylist.append({"name":name,"subcategories":subcategories})

	data={}
	data['products']=productlist
	data['categories']=categorylist
	data['curcategory']=curcategory

	xtoken=request.COOKIES.get('xtoken')
	if(xtoken):
		try:
			activeLogin=ActiveLogin.objects.get(xtoken=xtoken)
			profile=Customer.objects.get(loginid=activeLogin.loginid)
			data['profile']=profile
		except:
			pass

	return render(request,"main/categorywiseproducts.html",data)
