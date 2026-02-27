import pandas as pd
from typing import Dict, Any, List
import os

class TitanicDataLoader:
    def __init__(self, data_path: str = None):
        """
        Initialize the Titanic data loader.
        
        Args:
            data_path: Path to the Titanic CSV file. If None, uses default path.
        """
        if data_path is None:
            # Default to data/titanic.csv relative to this file's location
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "..", "..", "data", "titanic.csv")
        
        self.data_path = data_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load the Titanic dataset from CSV file."""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} rows of Titanic data")
        except FileNotFoundError:
            raise FileNotFoundError(f"Titanic dataset not found at {self.data_path}")
    
    def get_dataframe(self):
        """Return the loaded dataframe."""
        return self.df
    
    def get_column_stats(self, column: str) -> Dict[str, Any]:
        """
        Get statistics for a specific column.
        
        Args:
            column: Name of the column to analyze
            
        Returns:
            Dictionary containing various statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded")
        
        series = self.df[column]
        stats = {
            'count': len(series),
            'unique_values': series.nunique(),
            'missing_values': series.isnull().sum(),
        }
        
        # For numeric columns, add more statistics
        if pd.api.types.is_numeric_dtype(series):
            stats.update({
                'mean': series.mean() if not series.empty else None,
                'median': series.median() if not series.empty else None,
                'std': series.std() if not series.empty else None,
                'min': series.min() if not series.empty else None,
                'max': series.max() if not series.empty else None,
            })
        else:
            # For categorical columns, add value counts
            top_counts = series.value_counts().head(10)
            stats['top_values'] = top_counts.to_dict()
        
        return stats
    
    def calculate_percentage(self, column: str, value: Any) -> float:
        """
        Calculate the percentage of a specific value in a column.
        
        Args:
            column: Name of the column
            value: Value to calculate percentage for
            
        Returns:
            Percentage as a float
        """
        if self.df is None:
            raise ValueError("Data not loaded")
        
        count = len(self.df[self.df[column] == value])
        total = len(self.df)
        return (count / total) * 100 if total > 0 else 0
    
    def get_value_counts(self, column: str) -> Dict[Any, int]:
        """
        Get value counts for a specific column.
        
        Args:
            column: Name of the column
            
        Returns:
            Dictionary mapping values to their counts
        """
        if self.df is None:
            raise ValueError("Data not loaded")
        
        return self.df[column].value_counts().to_dict()
    
    def get_average(self, column: str) -> float:
        """
        Calculate the average value of a numeric column.
        
        Args:
            column: Name of the numeric column
            
        Returns:
            Average value as a float
        """
        if self.df is None:
            raise ValueError("Data not loaded")
        
        return self.df[column].mean()
    
    def get_age_distribution(self) -> Dict[str, Any]:
        """Get age distribution data."""
        if self.df is None:
            raise ValueError("Data not loaded")
        
        age_data = self.df['Age'].dropna()
        return {
            'count': len(age_data),
            'mean': age_data.mean(),
            'median': age_data.median(),
            'min': age_data.min(),
            'max': age_data.max(),
            'histogram_data': age_data.values.tolist()
        }

# Create a global instance for easy access
titanic_data = TitanicDataLoader()