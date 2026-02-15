from Services.data_service import DataService
from Services.analysis_service import AnalysisService

# --- Singleton Pattern Implementation ---
# We instantiate these services only ONCE here.
# This ensures that the dataset is loaded into memory only one time, 
# saving RAM and improving application performance.

# Initialize the data hub
data_service = DataService()

# Initialize the analysis engine and 'inject' the data_service into it.
# This is called Dependency Injection: AnalysisService depends on DataService to get its data.
analysis_service = AnalysisService(data_service)

# Helper functions (Dependency Providers)
# These functions provide a clean way for FastAPI routers to access the services.

def get_data_service():
    """Returns the globally shared DataService instance."""
    return data_service

def get_analysis_service():
    """Returns the globally shared AnalysisService instance."""
    return analysis_service