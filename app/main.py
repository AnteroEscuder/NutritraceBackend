from fastapi import FastAPI
from app.routes import auth, users, foods, meals, goals
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    # title="NutriTrace API",
    # description="API para seguimiento nutricional",
    # version ="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(goals.router)
app.include_router(auth.router)