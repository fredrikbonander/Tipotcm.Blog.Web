from google.appengine.ext import db

class Customer(db.Model):
    email = db.EmailProperty()
    password = db.StringProperty()
    firstname = db.StringProperty()
    lastname = db.StringProperty()
    address = db.StringProperty()
    zipcode = db.StringProperty()
    postal = db.StringProperty()
    phonenumber = db.StringProperty()

    @property
    def itemId(self):
        return self.key().id()

class Cart(db.Model):
    customerId = db.IntegerProperty()
    language = db.StringProperty()
    status = db.StringProperty(choices=set(["open", "ordered", "shipped"]), default="open")
    orderNumber = db.StringProperty()
    createdDate = db.DateTimeProperty(auto_now_add=True)
    orderDate = db.DateTimeProperty()
    transactionId = db.StringProperty()
    comments = db.TextProperty()
    voucherKeyName = db.StringProperty()
    totalPayed = db.IntegerProperty()

    @property
    def itemId(self):
        return self.key().id()


class CartItem(db.Model):
    cart = db.ReferenceProperty(Cart)
    productId = db.IntegerProperty()
    parts = db.ListProperty(db.Key)

    @property
    def itemId(self):
        return self.key().id()


class Products(db.Model):
    name = db.StringProperty()
    optionalParts = db.ListProperty(db.Key)
    defaultParts = db.ListProperty(db.Key)
    active = db.BooleanProperty(default=True)
    imageId = db.IntegerProperty(default=0)
    deleted = db.BooleanProperty(default=False)
    
    @property
    def itemId(self):
        return self.key().id()

class ProductPartTypes(db.Model):
    name = db.StringProperty()

    @property
    def itemId(self):
        return self.key().id()

class ProductParts(db.Model):    
    name = db.StringProperty()
    type = db.StringProperty()
    imageId = db.IntegerProperty(default=0)
    deleted = db.BooleanProperty(default=False)
    
    @property
    def itemId(self):
        return self.key().id()
       
class Labels(db.Model):
    identity = db.StringProperty()
    language = db.StringProperty()
    title = db.StringProperty()
    
class Prices(db.Model):
    identity = db.StringProperty()
    language = db.StringProperty()
    amount = db.IntegerProperty()

class Voucher(db.Model):
    language = db.StringProperty()
    startAmount = db.IntegerProperty()
    amount = db.IntegerProperty()
    status = db.StringProperty(choices=set(["open", "closed"]), default="open")

class Themes(db.Model):
    name = db.StringProperty()
    products = db.ListProperty(int)
    imageId = db.IntegerProperty(default=0)

    @property
    def itemId(self):
        return self.key().id()