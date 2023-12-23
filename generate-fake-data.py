#!/usr/bin/env python3
import json
import random
import uuid
import requests

from faker import Faker
from google.api_core.client_options import ClientOptions
from google.cloud import firestore



UNSPLASH_ACCESS_KEY = "WujoI1Lz6Lids0I1lfJgtFjST2t8Sl0lKS5plCoCsnw"

def get_image_url(query, width=None, height=None):
    url = f"https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "orientation": "landscape"
    }

    if width and height:
        params["w"] = width
        params["h"] = height

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        image_data = response.json()
        image_url = image_data["urls"]["regular"]
        return image_url
    else:
        return ""

class AdventureItem:
    def __init__(self, id=None, image=None, title=None, subTitle=None, isFavorite=False, category = None, adventures=None):
        self.id = id if id else str(uuid.uuid4())
        self.image = image if image else get_image_url("nature", 1024, 765)
        self.title = title if title else Faker().sentence(nb_words=3)
        self.subTitle = subTitle if subTitle else Faker().sentence(nb_words=5)
        self.isFavorite = isFavorite if isFavorite is not None else random.choice([True, False])
        self.category = category if category else Category()
        self.adventures = adventures if adventures else []

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "title": self.title,
            "subTitle": self.subTitle,
            "isFavorite": self.isFavorite,
            "category": self.category.to_dict(),
            "adventures": [adventure.to_dict() for adventure in self.adventures]
        }

class Adventure:
    def __init__(self, id=None, images=None, isFavorite=None, title=None, description=None,
                 rating=None, address=None, weather=None, type=None, amenities=None, accessibilities=None):
        self.id = id if id else str(uuid.uuid4())
        self.images = images if images else [f"image{i}.jpg" for i in range(3)]
        self.isFavorite = isFavorite if isFavorite is not None else random.choice([True, False])
        self.title = title if title else Faker().sentence(nb_words=3)
        self.description = description if description else Faker().paragraph()
        self.rating = rating if rating else str(round(random.uniform(1.0, 5.0), 1))
        self.address = address if address else []
        self.weather = weather if weather else []
        self.type = type if type else []
        self.amenities = amenities if amenities else []
        self.accessibilities = accessibilities if accessibilities else []

    def to_dict(self):
        return {
            "id": self.id,
            "images": self.images,
            "isFavorite": self.isFavorite,
            "title": self.title,
            "description": self.description,
            "rating": self.rating,
            "address": self.address.to_dict(),
            "weather": self.weather.to_dict(),
            "type": self.type.to_dict(),
            "amenties": [amenity.to_dict() for amenity in self.amenities],
            "accessibilities": [accessibility.to_dict() for accessibility in self.accessibilities]
        }

class Category:
    def __init__(self, id = None, name = None, emoji = None):
        self.id = id if id else str(uuid.uuid4())
        self.name = name if name else random.choice(["Beach Vacation","City Break", "Mountain Retreat", "Cultural Exploration","Adventure Trip", "Road Trip", "Ski Vacation",  "Luxury Getaway", "Backpacking Adventure", "Romantic Getaway"])
        self.emoji = emoji if emoji else random.choice([ "🏖️","🌆","🏞️", "🌍", "🌄", "🚗", "⛷️","🏨", "🎒","❤️"])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "emoji": self.emoji
        }
        
    
class Weather:
    def __init__(self, id=None, iconName=None, title=None):
        self.id = id if id else str(uuid.uuid4())
        self.iconName = iconName if iconName else random.choice(["cloud.fill", "cloud.fog.fill", "cloud.drizzle.fill", "cloud.sleet.fill"])
        self.title = title if title else random.choice(["100F", "34F", "72F", "88F"])

    def to_dict(self):
        return {
            "id": self.id,
            "iconName": self.iconName,
            "title": self.title
        }

class Amentie:
    def __init__(self, id=None, iconName=None, title=None):
        self.id = id if id else str(uuid.uuid4())
        self.iconName = iconName if iconName else random.choice(["parkingsign", "info.square.fill", "pawprint.fill", "figure.2.and.child.holdinghands", "takeoutbag.and.cup.and.straw.fill"])
        self.title = title if title else random.choice(["Parking available", "information centers", "Pet-friendly", "Good for kids", "Picnic areas"])

    def to_dict(self):
        return {
            "id": self.id,
            "iconName": self.iconName,
            "title": self.title
        }

class PlaceType:
    def __init__(self, id=None, name=None, iconName=None):
        self.id = id if id else str(uuid.uuid4())
        self.name = name if name else random.choice([
            "Beach",
            "Mountain",
            "City",
            "Historical Site",
            "National Park",
        ])
        self.iconName = iconName if iconName else random.choice(["figure.hiking", 
                                                                 "beach.umbrella.fill", 
                                                                 "building.2.crop.circle.fill", 
                                                                 "building.columns.fill", 
                                                                 "mountain.2.fill"])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "iconName": self.iconName
        }

class Accessibility:
    def __init__(self, id=None, iconName=None, title=None):
        self.id = id if id else str(uuid.uuid4())
        self.iconName = iconName if iconName else random.choice(["figure.roll", 
                                                                 "hearingdevice.ear.fill", 
                                                                 "toilet.fill", 
                                                                 "door.right.hand.closed", 
                                                                 "parkingsign.circle.fill"])
        self.title = title if title else random.choice([
            "Wheelchair Accessible",
            "Hearing Aid Assistance",
            "Accessible Restrooms",
            "Elevator Access",
            "Accessible Parking"
        ])

    def to_dict(self):
        return {
            "id": self.id,
            "iconName": self.iconName,
            "title": self.title
        }

class Address:
    def __init__(self, street, city, state, postalCode, country, latitude=None, longitude=None):
        self.street = street
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
    
    def to_dict(self):
        address_dict = {
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postalCode,
            "country": self.country
        }
        
        if self.latitude is not None and self.longitude is not None:
            address_dict["latitude"] = self.latitude
            address_dict["longitude"] = self.longitude

        return address_dict

def generate_fake_address():
    fake = Faker()
    street = fake.street_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.zipcode()
    country = fake.country()

    # Generate random latitude and longitude
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)

    return Address(street, city, state, postal_code, country, latitude, longitude)

# Function to generate fake Adventure data
def generate_fake_adventure_item():
    fake = Faker()

    weather_data = [Weather() for _ in range(3)]
    place_type_data = [PlaceType() for _ in range(3)]
    amentie_data = [Amentie() for _ in range(10)]
    accessibility_data = [Accessibility() for _ in range(3)]
    address_data = [generate_fake_address() for _ in range(3)]

    adventure_data = Adventure(
        images=[get_image_url("nature", 1024, 765) for _ in range(3)],
        isFavorite=fake.boolean(),
        title=fake.sentence(nb_words=3),
        description=fake.paragraph(),
        rating=str(round(random.uniform(1.0, 5.0), 1)),
        address= random.choice(address_data),
        weather= random.choice(weather_data),
        type=random.choice(place_type_data),
        amenities=amentie_data,
        accessibilities=accessibility_data
    )

    return adventure_data

        

def generate_fake_adventure():
    db = firestore.Client(project="spotline-645ce")

    listOfAdventures = [generate_fake_adventure_item() for _ in range(6)] 
    fakeAdventureItem = AdventureItem(adventures = listOfAdventures)
    json_data = json.dumps(fakeAdventureItem.to_dict())
    doc_ref = db.collection("Adventures").document(fakeAdventureItem.id)
    doc_ref.set(json.loads(json_data))

    print("Adventure_Stored On Emulator")

    local_json_file_path = "fake_adventure_data.json"
    with open(local_json_file_path, "w") as json_file:
        json.dump(fakeAdventureItem.to_dict(), json_file)
    print("Adventure_json saved")

if __name__ == "__main__":
    generate_fake_adventure()
