import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List
import base64
from io import BytesIO
import os

# Import here to avoid circular imports
from .data_loader import titanic_data

class TitanicVisualizer:
    def __init__(self, data_loader):
        """
        Initialize the Titanic visualizer.
        
        Args:
            data_loader: Instance of TitanicDataLoader
        """
        self.data_loader = data_loader
        self.df = data_loader.get_dataframe()
    
    def create_histogram(self, column: str, title: str = None) -> str:
        """
        Create a histogram for a specified column.
        
        Args:
            column: Name of the column to visualize
            title: Title for the chart
            
        Returns:
            HTML string of the plotly figure
        """
        if title is None:
            title = f"Distribution of {column}"
        
        fig = px.histogram(
            self.df,
            x=column,
            title=title,
            labels={column: column.replace('_', ' ').title()},
            color_discrete_sequence=['#1f77b4']
        )
        
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Count',
            width=800,
            height=500
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_bar_chart(self, column: str, title: str = None) -> str:
        """
        Create a bar chart for a specified column.
        
        Args:
            column: Name of the column to visualize
            title: Title for the chart
            
        Returns:
            HTML string of the plotly figure
        """
        if title is None:
            title = f"Bar Chart of {column}"
        
        value_counts = self.df[column].value_counts()
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            title=title,
            labels={'x': column.replace('_', ' ').title(), 'y': 'Count'},
            color_discrete_sequence=['#ff7f0e']
        )
        
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Count',
            width=800,
            height=500
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_pie_chart(self, column: str, title: str = None) -> str:
        """
        Create a pie chart for a specified column.
        
        Args:
            column: Name of the column to visualize
            title: Title for the chart
            
        Returns:
            HTML string of the plotly figure
        """
        if title is None:
            title = f"Pie Chart of {column}"
        
        value_counts = self.df[column].value_counts()
        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        
        fig.update_layout(
            width=800,
            height=500
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_age_distribution_histogram(self) -> str:
        """
        Create a histogram specifically for age distribution.
        
        Returns:
            HTML string of the plotly figure
        """
        # Drop NaN values for age
        age_data = self.df.dropna(subset=['Age'])
        
        fig = px.histogram(
            age_data,
            x='Age',
            nbins=30,
            title='Distribution of Passenger Ages',
            labels={'Age': 'Age'},
            color_discrete_sequence=['#2ca02c']
        )
        
        fig.update_layout(
            xaxis_title='Age',
            yaxis_title='Count',
            width=800,
            height=500
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def create_survival_by_category(self, category: str) -> str:
        """
        Create a bar chart showing survival rates by category.
        
        Args:
            category: Column name to group by (e.g., 'Sex', 'Pclass')
            
        Returns:
            HTML string of the plotly figure
        """
        # Create a crosstab of survival by category
        crosstab = pd.crosstab(self.df[category], self.df['Survived'], normalize='index') * 100
        
        # Convert to long format for plotting
        survival_rates = []
        categories = []
        for idx in crosstab.index:
            categories.append(idx)
            survival_rates.append(crosstab.loc[idx, 1])  # Survival rate (Survived=1)
        
        fig = px.bar(
            x=categories,
            y=survival_rates,
            title=f'Survival Rate by {category}',
            labels={'x': category.replace('_', ' ').title(), 'y': 'Survival Rate (%)'},
            color_discrete_sequence=['#d62728']
        )
        
        fig.update_layout(
            xaxis_title=category.replace('_', ' ').title(),
            yaxis_title='Survival Rate (%)',
            width=800,
            height=500
        )
        
        return fig.to_html(include_plotlyjs='cdn')

# Create a global instance for easy access
# Create a global instance for easy access
titanic_visualizer = TitanicVisualizer(titanic_data)