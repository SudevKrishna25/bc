from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Define the path to the JSON file where data will be stored
DATA_FILE = "profiles.json"

# Pydantic model for profile data
class Profile(BaseModel):
    name: str
    lastname: str
    email: str
    number: str
    bio: str

# Helper function to load profiles from the JSON file
def load_profiles():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Helper function to save profiles to the JSON file
def save_profiles(profiles):
    with open(DATA_FILE, "w") as file:
        json.dump(profiles, file, indent=4)

# Endpoint to create a new profile
@app.post("/profiles/")
def create_profile(profile: Profile):
    profiles = load_profiles()
    
    # Check if the email already exists
    if any(p["email"] == profile.email for p in profiles):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Add the new profile
    profiles.append(profile.dict())
    save_profiles(profiles)
    
    return {"message": "Profile created successfully", "profile": profile}

# Endpoint to get all profiles
@app.get("/profiles/")
def get_profiles():
    profiles = load_profiles()
    return {"profiles": profiles}

# Endpoint to get a profile by email
@app.get("/profiles/{email}")
def get_profile_by_email(email: str):
    profiles = load_profiles()
    profile = next((p for p in profiles if p["email"] == email), None)
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {"profile": profile}

# Endpoint to update a profile by email
@app.put("/profiles/{email}")
def update_profile(email: str, updated_profile: Profile):
    profiles = load_profiles()
    
    # Find the profile to update
    profile_index = next((i for i, p in enumerate(profiles) if p["email"] == email), None)
    
    if profile_index is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update the profile
    profiles[profile_index] = updated_profile.dict()
    save_profiles(profiles)
    
    return {"message": "Profile updated successfully", "profile": updated_profile}

# Endpoint to delete a profile by email
@app.delete("/profiles/{email}")
def delete_profile(email: str):
    profiles = load_profiles()
    
    # Find the profile to delete
    profile_index = next((i for i, p in enumerate(profiles) if p["email"] == email), None)
    
    if profile_index is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Remove the profile
    deleted_profile = profiles.pop(profile_index)
    save_profiles(profiles)
    
    return {"message": "Profile deleted successfully", "profile": deleted_profile}