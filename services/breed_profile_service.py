"""
breed_profile_service.py — Load and serve breed profile data.
"""
import json
from pathlib import Path

_PROFILES_PATH = Path(__file__).parent.parent / "data" / "breed_profiles.json"

_DOG_BREEDS = [
    "German Shepherd",
    "Labrador Retriever",
    "Golden Retriever",
    "Pug",
    "Siberian Husky",
]

_CAT_BREEDS = [
    "Persian",
    "Maine Coon",
    "Siamese",
    "British Shorthair",
    "Sphynx",
]

_profiles_cache = None


def _load_profiles() -> dict:
    global _profiles_cache
    if _profiles_cache is None:
        with open(_PROFILES_PATH, "r") as f:
            _profiles_cache = json.load(f)
    return _profiles_cache


def get_dog_breeds() -> list:
    return _DOG_BREEDS


def get_cat_breeds() -> list:
    return _CAT_BREEDS


def get_breed_profile(breed_name: str) -> dict:
    profiles = _load_profiles()
    profile = profiles.get(breed_name)
    if not profile:
        raise ValueError(f"Breed '{breed_name}' not supported in this MVP.")
    # Ensure sun_exposure_sensitivity exists (Sphynx-specific)
    profile.setdefault("sun_exposure_sensitivity", 0.0)
    return profile


def get_all_profiles() -> dict:
    return _load_profiles()