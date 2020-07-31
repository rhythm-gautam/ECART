from django.db import models

class Login(models.Model):
	email=models.EmailField(max_length=100)
	password=models.SlugField(max_length=30)
	isactive=models.BooleanField(max_length=10)

class Customer(models.Model):
	loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
	name=models.CharField(max_length=20)
	gender=models.CharField(max_length=10)
	phone=models.CharField(max_length=13)

class ShippingAddress(models.Model):
	loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
	title=models.CharField(max_length=20)
	hno=models.CharField(max_length=20)
	area=models.CharField(max_length=20)
	city=models.CharField(max_length=20)
	pin=models.IntegerField()
	landmark=models.CharField(max_length=100)

class Category(models.Model):
	parentid = models.IntegerField()
	name = models.CharField(max_length=100)
	desc = models.TextField()


class Brand(models.Model):
	name = models.CharField(max_length=100)
	logo = models.FileField(upload_to="")
	desc = models.TextField()

class Product(models.Model):
	brandid = models.ForeignKey(Brand,on_delete=models.CASCADE)
	categoryid = models.ForeignKey(Category,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=10,decimal_places=2)

class ProductImage(models.Model):
	productid = models.ForeignKey(Product,on_delete=models.CASCADE)
	image = models.FileField()

class FeatureLookup(models.Model):
	categoryid=models.ForeignKey(Category,on_delete=models.CASCADE)
	name=models.CharField(max_length=50)

class FeatureValue(models.Model):
	productid=models.ForeignKey(Product,on_delete=models.CASCADE)
	featureid=models.ForeignKey(FeatureLookup,on_delete=models.CASCADE)
	value=models.CharField(max_length=40)

class Cart(models.Model):
	loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
	productid=models.ForeignKey(Product,on_delete=models.CASCADE)

class Order(models.Model):
	loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
	addressid=models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)
	datetime=models.DateTimeField()
	amount=models.DecimalField(max_digits=10,decimal_places=2)

class OrderItem(models.Model):
	orderid=models.ForeignKey(Order,on_delete=models.CASCADE)
	productid=models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity=models.IntegerField()

class Shipping(models.Model):
	orderid=models.ForeignKey(Order,on_delete=models.CASCADE)
	status=models.CharField(max_length=20)


class ActiveLogin(models.Model):
	loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
	xtoken=models.CharField(max_length=32)
	datetime=models.DateTimeField()	