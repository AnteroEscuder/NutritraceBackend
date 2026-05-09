from fastapi import FastAPI
from app.routes import auth, users, foods, meals, goals, allergens, profile, community
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    # title="NutriTrace API",
    # description="API para seguimiento nutricional",
    # version ="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/profile_photos", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(goals.router)
app.include_router(auth.router)
app.include_router(allergens.router)
app.include_router(profile.router)
app.include_router(community.router)