from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from utils import data_service  # Import shared data logic from utils

# Initialize the router for core application pages
router = APIRouter()

# Configure Jinja2 templates directory
# This allows FastAPI to render HTML files and inject dynamic data
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    """
    Main landing page. 
    Fetches basic dataset metadata and renders it using the index.html template.
    """
    
    # Retrieve dataset metadata using the data_service utility
    dataset_name = data_service.get_dataset_name()
    shape = data_service.get_shape() # Returns a tuple (rows, columns)
    columns = data_service.get_columns()

    # Return a TemplateResponse which combines the HTML file with Python data
    return templates.TemplateResponse("index.html", {
        "request": request,             # Mandatory for Jinja2 in FastAPI
        "dataset_name": dataset_name,   # Name of the Seaborn dataset
        "num_rows": shape[0],           # Number of records in the dataset
        "num_cols": shape[1],           # Number of features/columns
        "columns": columns              # List of column names for display
    })