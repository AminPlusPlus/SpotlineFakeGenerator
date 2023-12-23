#!/usr/bin/env python3
import json
import random
import uuid
import requests

from faker import Faker
from google.api_core.client_options import ClientOptions
from google.cloud import firestore

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

# Create an array to store category objects
categories = []

def generate_fake_categories():
    db = firestore.Client(project="spotline-645ce")
    for i in range(1, 11):
        category = Category()
        json_data = json.dumps(category.to_dict())
        doc_ref = db.collection("Categories").document(category.id)
        doc_ref.set(category.to_dict())
        categories.append(category)
    
    print("All categories have been set in Firestore")

    # Convert the list of categories to a list of dictionaries
    category_dicts = [category.to_dict() for category in categories]

    # Save all categories as an array in a single local JSON file
    local_json_file_path = "all_fake_categories_data.json"
    with open(local_json_file_path, "w") as json_file:
        json.dump(category_dicts, json_file)
    print("All category data has been saved in a single JSON file")

if __name__ == "__main__":
    generate_fake_categories()