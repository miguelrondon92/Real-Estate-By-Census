import requests
from pymongo import MongoClient


census_vars = requests.get("https://api.census.gov/data/2020/dec/pl/variables.json")
