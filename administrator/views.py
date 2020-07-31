from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from django.core import serializers
from administrator.models import *


def Index(request):
	return HttpResponse("Test");

def AddCategory(request):
	if request.method=='GET':
		categories=Category.objects.filter()
		return render(request,"administrator/addcategory.html",{"categories":categories})
	else:
		parentid=request.POST.get("parentid")
		name=request.POST.get("name")
		desc=request.POST.get("desc")
		category=Category(parentid=parentid,name=name,desc=desc)
		category.save()
		return redirect("/admin/category/")


def DeleteCategory(request,id):
	Category.objects.get(id=id).delete()
	return redirect("/admin/category/")


def UpdateCategory(request,id):
	if request.method=='GET':
		category=Category.objects.get(id=id)
		categories=Category.objects.filter()		
		data={'category':category,'categories':categories}
		return render(request,"administrator/addcategory.html",data)
	else:		
		parentid=request.POST.get("parentid")
		name=request.POST.get("name")
		desc=request.POST.get("desc")

		category=Category.objects.get(id=id)
		category.name=name
		category.desc=desc
		category.parentid=parentid
		category.save()
		return redirect("/admin/category/")

def GetCategory(request,id):
	Pass


def GetCategories(request):
	categories=Category.objects.filter()
	data={'categories':[]}
	for category in categories:
		if(category.parentid==0):
			parent='None'
		else:
			parent=Category.objects.get(id=category.parentid).name
		category.parent=parent
		data['categories'].append(category)
	return render(request,"administrator/categories.html",data)



#Brand

def AddBrand(request):
	if request.method=='GET':
		return render(request,"administrator/addbrand.html",None)
	else:
		name=request.POST.get("name")
		logo=request.FILES.get("logo")
		desc=request.POST.get("desc")
		brand=Brand(name=name,logo=logo,desc=desc)
		brand.save()
		return redirect("/admin/brand/")

def DeleteBrand(request,id):
	Brand.objects.get(id=id).delete()
	return redirect("/admin/brand/")


def UpdateBrand(request,id):
	if request.method=='GET':
		brand=Brand.objects.get(id=id)		
		return render(request,"administrator/addbrand.html",{'brand':brand})
	else:		
		name=request.POST.get("name")
		logo=request.FILES.get("logo")
		desc=request.POST.get("desc")
		brand=Brand.objects.get(id=id)
		brand.name=name
		brand.desc=desc
		if logo!=None:
			brand.logo=logo
		brand.save()
		return redirect("/admin/brand/")


def GetBrand(request,id):
	Pass


def GetBrands(request):
	brands=Brand.objects.filter()
	return render(request,"administrator/brands.html",{"brands":brands})


#Product

def AddProduct(request):
	if request.method=='GET':
		data={}
		data['categories']=Category.objects.filter()
		data['brands']=Brand.objects.filter()
		return render(request,"administrator/addproduct.html",data)
	else:
		bid=request.POST.get("brandid")
		cid=request.POST.get("categoryid")
		name=request.POST.get("name")
		price=request.POST.get("price")
		brand=Brand.objects.get(id=bid)
		category=Category.objects.get(id=cid)
		
		product=Product(brandid=brand,categoryid=category,name=name,price=price)
		product.save()

		featurelookup=FeatureLookup.objects.filter(categoryid=category)
		for feature in featurelookup:
			featurevalue=FeatureValue()
			featurevalue.productid=product
			featurevalue.featureid=feature
			featurevalue.value=request.POST.get('features['+str(feature.id)+']')
			featurevalue.save()
		return redirect("/admin/product/")

def DeleteProduct(request,id):
	Product.objects.get(id=id).delete()
	return redirect("/admin/product/")


def UpdateProduct(request,id):
	if request.method=='GET':
		data={}
		data['product']=Product.objects.get(id=id)		
		data['categories']=Category.objects.filter()
		data['brands']=Brand.objects.filter()
		data['features']=FeatureValue.objects.filter(productid=data['product'])
		return render(request,"administrator/addproduct.html",data)
	else:		
		bid=request.POST.get("brandid")
		cid=request.POST.get("categoryid")
		name=request.POST.get("name")
		price=request.POST.get("price")

		brand=Brand.objects.get(id=bid)
		cat=Category.objects.get(id=cid)

		product=Product.objects.get(id=id)
		product.brandid=brand
		product.categoryid=cat
		product.name=name
		product.price=price
		product.save()


		FeatureValue.objects.filter(productid=product).delete()		

		featurelookup=FeatureLookup.objects.filter(categoryid=cat)
		for feature in featurelookup:
			featurevalue=FeatureValue()
			featurevalue.productid=product
			featurevalue.featureid=feature
			featurevalue.value=request.POST.get('features['+str(feature.id)+']')
			featurevalue.save()

		return redirect("/admin/product/")

def GetProduct(request,id):
	Pass


def GetProducts(request):
	products=Product.objects.filter()
	return render(request,"administrator/products.html",{"products":products})


#Product Images

def AddProductImage(request,id):
	if request.method=='GET':
		return render(request,"administrator/addproductimage.html",None)
	else:
		product=Product.objects.get(id=id)
		for image in request.FILES.getlist("image"):
			pi=ProductImage(productid=product,image=image)
			pi.save()
		return redirect("/admin/product/image/" + id)

def DeleteProductImage(request,id):
	pi=ProductImage.objects.get(id=id)
	parentid=pi.productid.id
	pi.delete()
	return redirect("/admin/product/image/"+str(parentid))

def GetProductImage(request,id):
	Pass

def GetProductImages(request,id):
	pis=ProductImage.objects.filter(productid=id)
	return render(request,"administrator/productimages.html",{"id":id,"images":pis})


def GetFeatures(request,cid):
	category=Category.objects.get(id=cid)
	featureslist=FeatureLookup.objects.filter(categoryid=category)
	data={}
	data['features']=featureslist
	data['category']=category
	return render(request,"administrator/features.html",data)


def GetFeaturesList(request,cid):
	category=Category.objects.get(id=cid)
	featureslist=FeatureLookup.objects.filter(categoryid=category)
	response_data={}
	response_data['features']=serializers.serialize("json", featureslist)
	return HttpResponse(json.dumps(response_data), content_type="application/json")


def GetFeaturesValues(request,pid):
	product=Product.objects.get(id=pid)
	featurevalues=FeatureValue.objects.filter(productid=product)
	
	features=[]
	for i in range(len(featurevalues)):
		feature={}
		feature['featureid']=featurevalues[i].featureid.id
		feature['name']=featurevalues[i].featureid.name
		feature['value']=featurevalues[i].value
		features.append(feature)
	#response_data={}
	#response_data['features']=serializers.serialize("json", featurevalues)
	return HttpResponse(json.dumps({'features':features}), content_type="application/json")

def AddFeature(request,cid):
	if(request.method=='GET'):
		categories=Category.objects.filter()
		data={'categories':categories}
		return render(request,"administrator/addfeature.html", data)
	else:
		featurelookup=FeatureLookup()
		featurelookup.categoryid=Category.objects.get(id=cid)
		featurelookup.name=request.POST.get('name')
		featurelookup.save()
		return redirect('/admin/features/' + str(cid))

def DeleteFeature(request,fid):
	featurelookup=FeatureLookup.objects.get(id=fid)
	cid=featurelookup.categoryid.id
	featurelookup.delete()
	return redirect('/admin/features/' + str(cid))
