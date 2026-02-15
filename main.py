import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# Import logic modules (Routers) to keep the main file clean and organized
from routers import core, questions, data 

# Initialize the FastAPI application
# Setting a title helps with the automatically generated documentation (/docs)
app = FastAPI(title="Seaborn Web Explorer - Planets Dataset")

# Mount static files (CSS, JS, Images)
# This allows the frontend to access files stored in the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registering Routers
# We separate the endpoints into different modules for better maintainability and scalability
app.include_router(core.router)      # Core application logic (e.g., Home page)
app.include_router(questions.router) # Endpoints related to specific questions/tasks
app.include_router(data.router)      # Data processing and API endpoints

if __name__ == "__main__":
    # Run the application using Uvicorn (ASGI server)
    # 'reload=True' enables auto-restart during development when code changes
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)