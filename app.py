from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(name)

API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

def get_places(keyword, location):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}+in+{location}&key={API_KEY}"
    res = requests.get(url)
    return res.json().get("results", [])

def extract_email(website):
    try:
        res = requests.get(website, timeout=5)
        emails = re.findall(r"[\w\.-]+@[\w\.-]+", res.text)
        return emails[0] if emails else None
    except:
        return None

@app.route("/leads", methods=["POST"])
def leads():
    data = request.json
    keyword = data["keyword"]
    country = data["country"]
    limit = int(data["limit"])

    places = get_places(keyword, country)

    results = []

    for place in places[:limit]:
        name = place.get("name")
        address = place.get("formatted_address")

        website = None
        email = None

        if "website" in place:
            website = place["website"]
            email = extract_email(website)

        results.append({
            "name": name,
            "address": address,
            "website": website,
            "email": email
        })

    return jsonify(results)

app.run(host="0.0.0.0", port=5000)
