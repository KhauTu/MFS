from mongoengine import Document, StringField, ListField
class Item(Document):
    name = StringField()
    phone = StringField()
    address = StringField()
    image = ListField()
    story = StringField()
    price = StringField()
    category = StringField()
