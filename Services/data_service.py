"""
DataService - Handles loading and providing access to the Planets dataset.
This service acts as the central data hub for the entire application.
"""
import pandas as pd
import seaborn as sns

# Global variable to pre-load or check the dataset existence from Seaborn's library
planets_data = sns.load_dataset('planets')

class DataService:  # Service for managing the dataset operations
    def __init__(self):
        """
        Initializes the service. 
        Setting _df to None ensures we start with a clean state before loading.
        """
        self._df = None
        self._dataset_name = 'planets'
        self.load_dataset()

    def load_dataset(self): 
        """
        Loads the dataset directly from the Seaborn library into a Pandas DataFrame.
        Seaborn provides built-in datasets which are excellent for practicing data analysis.
        """
        print(f"Loading {self._dataset_name} dataset...")
        # We use sns.load_dataset to fetch the 'planets' data 
        # as a standard Pandas DataFrame object.
        self._df = sns.load_dataset(self._dataset_name)
        
        # Logging dataset info to the console for development tracking
        print(f"Dataset loaded successfully! Shape: {self._df.shape}")
        print(f"Columns: {list(self._df.columns)}")

    def get_df(self) -> pd.DataFrame:
        """Returns the main DataFrame object for analysis."""
        return self._df
    
    def get_dataset_name(self) -> str:
        """Returns the name of the dataset being used."""
        return self._dataset_name
    
    def get_columns(self) -> list:
        """Returns a list of all column names in the dataset."""
        return list(self._df.columns)
    
    def get_shape(self) -> tuple:
        """Returns a tuple indicating the number of (rows, columns)."""
        return self._df.shape