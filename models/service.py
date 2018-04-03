from mongoengine import Document, StringField, ListField, ReferenceField
class Category(Document):
    name = StringField()

class Comment(Document):
    author = StringField()
    content = StringField()

class Item(Document):
    name = StringField()
    phone = StringField()
    address = StringField()
    image = ListField()
    story = StringField()
    price = StringField()
    title = StringField()
    category = ListField(ReferenceField(Category))
    comments = ListField(ReferenceField(Comment))

class User(Document):
    user_name = StringField()
    password = StringField()
    email = StringField()
    phone = StringField()
