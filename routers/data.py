from fastapi import APIRouter, Request, Query
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from utils import data_service
import io

# Define router with a prefix to group all data-related endpoints under /data
router = APIRouter(prefix="/data")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_data(
    request: Request,
    cols: list[str] = Query(None), 
    filter_col: str = Query(None),
    op: str = Query(None),
    value: str = Query(None),
    limit: int = Query(20)
):
    """
    Main data exploration endpoint. 
    Handles dynamic column selection, filtering logic, and HTML table rendering.
    """
    df = data_service.get_df()
    available_columns = data_service.get_columns()
    
    error_message = None
    result_html = None

    # Processing starts if user interacts with the filter form
    if cols or filter_col:
        try:
            # Step 1: Column Selection & Validation
            if cols:
                invalid_cols = [col for col in cols if col not in available_columns]
                if invalid_cols:
                    raise ValueError(f"Invalid columns: {', '.join(invalid_cols)}")
                df_view = df[cols]
            else:
                raise ValueError("Please select at least one column to display.")

            # Step 2: Dynamic Filtering Logic
            if filter_col and op and value:
                if filter_col not in df_view.columns:
                    raise ValueError(f"Filter column '{filter_col}' not found")
                
                # Apply filters based on the selected operator
                if op == "==":
                    df_view = df_view[df_view[filter_col].astype(str) == value]
                elif op == "!=":
                    df_view = df_view[df_view[filter_col].astype(str) != value]
                elif op == "contains":
                    df_view = df_view[df_view[filter_col].astype(str).str.contains(value, case=False, na=False)]
                elif op in [">", "<", ">=", "<="]:
                    try:
                        # Convert value to float for numeric comparisons
                        num_val = float(value)
                        if op == ">": df_view = df_view[df_view[filter_col] > num_val]
                        elif op == "<": df_view = df_view[df_view[filter_col] < num_val]
                        elif op == ">=": df_view = df_view[df_view[filter_col] >= num_val]
                        elif op == "<=": df_view = df_view[df_view[filter_col] <= num_val]
                    except ValueError:
                        raise ValueError(f"Value '{value}' must be numeric for operator '{op}'")
            
            # Step 3: Pagination (Limit) and HTML Conversion
            df_view = df_view.head(limit)
            if len(df_view) == 0:
                result_html = "<p class='text-warning text-center'>No results found.</p>"
            else:
                # Convert the Pandas DataFrame to a Bootstrap-styled HTML table
                result_html = df_view.to_html(
                    index=False,
                    classes='table table-hover',
                    border=0,
                    justify='center'
                )
        
        except Exception as e:
            # Capture any processing errors to display in the UI
            error_message = str(e)

    return templates.TemplateResponse("data.html", {
        "request": request,
        "available_columns": available_columns,
        "result_html": result_html,
        "error_message": error_message,
        "cols": cols or [],
        "filter_col": filter_col or "",
        "op": op or "==",
        "value": value or "",
        "limit": limit
    })

@router.get("/export")
async def export_data(
    cols: list[str] = Query(None), 
    filter_col: str = Query(None), 
    op: str = Query(None), 
    value: str = Query(None), 
    limit: int = 1000
):
    """
    Generates a downloadable CSV file based on the user's current filters.
    """
    df = data_service.get_df()
    df_view = df.copy() 

    # Re-apply the same logic as get_data for the export stream
    if cols:
        df_view = df_view[[c for c in cols if c in df_view.columns]]
    
    if filter_col and op and value:
        try:
            if op == "==":
                df_view = df_view[df_view[filter_col].astype(str) == value]
            elif op == "contains":
                df_view = df_view[df_view[filter_col].astype(str).str.contains(value, case=False, na=False)]
            elif op in [">", "<", ">=", "<="]:
                num_val = float(value)
                if op == ">": df_view = df_view[df_view[filter_col] > num_val]
                elif op == "<": df_view = df_view[df_view[filter_col] < num_val]
                elif op == ">=": df_view = df_view[df_view[filter_col] >= num_val]
                elif op == "<=": df_view = df_view[df_view[filter_col] <= num_val]
        except:
            pass    

    df_view = df_view.head(limit)

    # Use io.StringIO to create an in-memory text stream for the CSV
    stream = io.StringIO()
    df_view.to_csv(stream, index=False)
    
    # Return a StreamingResponse to trigger a file download in the browser
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=filtered_data.csv"
    return response