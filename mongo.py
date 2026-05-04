import os

def load_dotenv(dotenv_path=".env"):
    if not os.path.exists(dotenv_path):
        return False
    with open(dotenv_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    return True

from pymongo import MongoClient # pyright: ignore[reportMissingImports]
from pymongo.errors import PyMongoError # type: ignore


load_dotenv()


FALLBACK_PROFILE = {
    "name": "Abubakar Siddiq",
    "role": "Frontend Developer",
    "tagline": "Building modern portfolio experiences with Django, React, and MongoDB.",
    "about": (
        "I create polished user interfaces with strong visual identity, animated openings, "
        "and clear frontend structure. This starter project uses Django for the backend and "
        "React for the portfolio frontend."
    ),
    "highlights": [
        "Animated portfolio opening",
        "Django API backend",
        "React frontend served by Django",
        "MongoDB-ready data layer",
    ],
    "projects": [
        {
            "title": "Portfolio Launch Experience",
            "summary": "A cinematic personal site opening with layered motion and strong first-screen branding.",
        },
        {
            "title": "Frontend Showcase",
            "summary": "A responsive React interface that presents skills, work, and contact details cleanly.",
        },
        {
            "title": "API Integration Starter",
            "summary": "A Django endpoint that can switch between fallback data and MongoDB collection data.",
        },
    ],
    "contact": {
        "email": "pgnrabubakar@gmail.com",
        "location": "India",
        "linkedin": "https://www.linkedin.com/in/abubakar-siddiq-9a1b4b1a0/",
        "github": "https://github.com/abubakarsiddiq",
        "Phone" : "+91 9100254955"
    },
}


def _get_collection():
    mongo_uri = os.getenv("MONGO_URI", "").strip()
    db_name = os.getenv("MONGO_DB_NAME", "portfolio_db").strip() or "portfolio_db"
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "profiles").strip() or "profiles"

    if not mongo_uri:
        return None

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2500)
    database = client[db_name]
    return database[collection_name]


def fetch_portfolio_profile():
    collection = _get_collection()
    if collection is None:
        return {"source": "fallback", "data": FALLBACK_PROFILE}

    try:
        document = collection.find_one({"slug": "main-portfolio"}, {"_id": 0})
        if not document:
            return {"source": "fallback", "data": FALLBACK_PROFILE}
        return {"source": "mongodb", "data": document}
    except PyMongoError:
        return {"source": "fallback", "data": FALLBACK_PROFILE}
