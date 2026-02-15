from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from utils import analysis_service # Import the analysis logic service

# Group all question-related routes under the "/questions" prefix
router = APIRouter(prefix="/questions")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def questions_page(request: Request):
    """
    Renders the initial questions list page.
    'question_selected' is set to False to show the list without results.
    """
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "question_selected": False,

    })

@router.get("/{question_id}")
async def question_result(request: Request, question_id: int):
    """
    Handles dynamic routing based on the selected question ID.
    Fetches analytical results and visualizations from analysis_service.
    """
    # Validation: Ensure the requested question exists in our defined range
    if question_id < 1 or question_id > 5:
        return templates.TemplateResponse("questions.html", {
            "request": request,
            "question_selected": False,
            "error": "Invalid question ID. Please select a question between 1-5."
        })
    
    # Execute the specific analysis logic based on the ID
    result_data = analysis_service.run_question(question_id)
    
    # Inject analysis data into the template
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "question_selected": True,
        "question_id": question_id,
        "title": result_data.get('title', 'No Title'),     # Human-readable question title
        "result": result_data.get('result', ''),           # Textual analysis or summary table
        "graph_html": result_data.get('graph_html'),       # Plotly HTML div (if applicable)
        "is_plotly": result_data.get('is_plotly', False),  # Flag to determine rendering method in HTML
        "plot_filename": result_data.get('plot_filename')  # Path to static image (if not Plotly)
    })