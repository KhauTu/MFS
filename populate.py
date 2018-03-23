import mlab
from models.service import Item
from random import randint, choice
from faker import Faker

fake = Faker()
mlab.connect()

for i in range(10):
    print("Saving Item", i + 1, ">>>>>>>>>>>>")
    mfs = Item(name=fake.name(),
    phone=fake.phone_number(),
    address=fake.address(),
    image="http://sohanews.sohacdn.com/k:2014/2-77d35baa-c8c7-4b7a-9bc1-28a9b2ff30cc-1403051680900/nhung-ki-vat-tinh-yeu-ngot-ngao-khien-fa-phat-them-.jpg", story='abc',
    price = "500.000 VNĐ")

    mfs.save()
