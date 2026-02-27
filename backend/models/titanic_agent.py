from langchain.tools import BaseTool
from langchain_core.tools import Tool
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from typing import Optional
from pydantic import Field, BaseModel
import re

# Import our utilities
from ..utils.data_loader import titanic_data
from ..utils.visualizer import titanic_visualizer


class PassengerPercentageTool(BaseTool):
    name: str = "passenger_percentage_calculator"
    description: str = "Calculate the percentage of passengers with a specific characteristic. Input should be a dictionary with 'column' and 'value' keys."

    def _run(self, query: str) -> str:
        """Use the tool to calculate passenger percentages."""
        try:
            # Parse the query to extract column and value
            # For example: "percentage of male passengers" -> column="Sex", value="male"
            query_lower = query.lower()
            
            # Handle common percentage queries
            if "male" in query_lower or "men" in query_lower:
                percentage = titanic_data.calculate_percentage("Sex", "male")
                return f"The percentage of male passengers was {percentage:.2f}%"
            elif "female" in query_lower or "women" in query_lower:
                percentage = titanic_data.calculate_percentage("Sex", "female")
                return f"The percentage of female passengers was {percentage:.2f}%"
            elif "survived" in query_lower:
                percentage = titanic_data.calculate_percentage("Survived", 1)
                return f"The percentage of passengers who survived was {percentage:.2f}%"
            elif "died" in query_lower or "perished" in query_lower:
                percentage = titanic_data.calculate_percentage("Survived", 0)
                return f"The percentage of passengers who died was {percentage:.2f}%"
            elif "first class" in query_lower or "1st class" in query_lower:
                percentage = titanic_data.calculate_percentage("Pclass", 1)
                return f"The percentage of passengers in first class was {percentage:.2f}%"
            elif "second class" in query_lower or "2nd class" in query_lower:
                percentage = titanic_data.calculate_percentage("Pclass", 2)
                return f"The percentage of passengers in second class was {percentage:.2f}%"
            elif "third class" in query_lower or "3rd class" in query_lower:
                percentage = titanic_data.calculate_percentage("Pclass", 3)
                return f"The percentage of passengers in third class was {percentage:.2f}%"
            elif "southampton" in query_lower or "s port" in query_lower:
                percentage = titanic_data.calculate_percentage("Embarked", "S")
                return f"The percentage of passengers who embarked from Southampton was {percentage:.2f}%"
            elif "cherbourg" in query_lower or "c port" in query_lower:
                percentage = titanic_data.calculate_percentage("Embarked", "C")
                return f"The percentage of passengers who embarked from Cherbourg was {percentage:.2f}%"
            elif "queenstown" in query_lower or "q port" in query_lower:
                percentage = titanic_data.calculate_percentage("Embarked", "Q")
                return f"The percentage of passengers who embarked from Queenstown was {percentage:.2f}%"
            else:
                # More general parsing - try to extract column and value
                # This is a simplified parser - in a real app, you'd want more robust NLP
                if "sex" in query_lower and ("male" in query_lower or "female" in query_lower):
                    value = "male" if "male" in query_lower else "female"
                    percentage = titanic_data.calculate_percentage("Sex", value)
                    return f"The percentage of {value} passengers was {percentage:.2f}%"
                
                return "I couldn't parse your request. Please ask about passenger percentages in a clearer way."
        except Exception as e:
            return f"Error calculating percentage: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the run method."""
        raise NotImplementedError("PassengerPercentageTool does not support async")


class PassengerCountTool(BaseTool):
    name: str = "passenger_count_tool"
    description: str = "Count the number of passengers with a specific characteristic. Input should describe what to count."

    def _run(self, query: str) -> str:
        """Use the tool to count passengers."""
        try:
            query_lower = query.lower()
            
            # Handle common count queries
            if "embark" in query_lower and ("southampton" in query_lower or "s port" in query_lower):
                counts = titanic_data.get_value_counts("Embarked")
                s_count = counts.get("S", 0)
                return f"{s_count} passengers embarked from Southampton (S)"
            elif "embark" in query_lower and ("cherbourg" in query_lower or "c port" in query_lower):
                counts = titanic_data.get_value_counts("Embarked")
                c_count = counts.get("C", 0)
                return f"{c_count} passengers embarked from Cherbourg (C)"
            elif "embark" in query_lower and ("queenstown" in query_lower or "q port" in query_lower):
                counts = titanic_data.get_value_counts("Embarked")
                q_count = counts.get("Q", 0)
                return f"{q_count} passengers embarked from Queenstown (Q)"
            elif "embark" in query_lower:
                counts = titanic_data.get_value_counts("Embarked")
                s_count = counts.get("S", 0)
                c_count = counts.get("C", 0)
                q_count = counts.get("Q", 0)
                return f"Passengers embarked from: Southampton: {s_count}, Cherbourg: {c_count}, Queenstown: {q_count}"
            elif "surviv" in query_lower:
                counts = titanic_data.get_value_counts("Survived")
                survived_count = counts.get(1, 0)
                died_count = counts.get(0, 0)
                return f"Number of survivors: {survived_count}, Number who died: {died_count}"
            elif "male" in query_lower or "men" in query_lower:
                counts = titanic_data.get_value_counts("Sex")
                male_count = counts.get("male", 0)
                return f"There were {male_count} male passengers"
            elif "female" in query_lower or "women" in query_lower:
                counts = titanic_data.get_value_counts("Sex")
                female_count = counts.get("female", 0)
                return f"There were {female_count} female passengers"
            elif "first class" in query_lower or "1st class" in query_lower:
                counts = titanic_data.get_value_counts("Pclass")
                first_class_count = counts.get(1, 0)
                return f"There were {first_class_count} first-class passengers"
            elif "second class" in query_lower or "2nd class" in query_lower:
                counts = titanic_data.get_value_counts("Pclass")
                second_class_count = counts.get(2, 0)
                return f"There were {second_class_count} second-class passengers"
            elif "third class" in query_lower or "3rd class" in query_lower:
                counts = titanic_data.get_value_counts("Pclass")
                third_class_count = counts.get(3, 0)
                return f"There were {third_class_count} third-class passengers"
            else:
                return "I couldn't parse your request. Please ask about passenger counts in a clearer way."
        except Exception as e:
            return f"Error counting passengers: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the run method."""
        raise NotImplementedError("PassengerCountTool does not support async")


class AverageValueTool(BaseTool):
    name: str = "average_value_calculator"
    description: str = "Calculate average values for numeric columns like age or fare."

    def _run(self, query: str) -> str:
        """Use the tool to calculate averages."""
        try:
            query_lower = query.lower()
            
            if "age" in query_lower:
                avg_age = titanic_data.get_average("Age")
                return f"The average age of passengers was {avg_age:.2f} years"
            elif "fare" in query_lower or "ticket price" in query_lower or "price" in query_lower:
                avg_fare = titanic_data.get_average("Fare")
                return f"The average ticket fare was ${avg_fare:.2f}"
            else:
                return "I can calculate averages for age and fare. Please specify which one you're interested in."
        except Exception as e:
            return f"Error calculating average: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the run method."""
        raise NotImplementedError("AverageValueTool does not support async")


class AgeHistogramTool(BaseTool):
    name: str = "age_histogram_generator"
    description: str = "Generate a histogram of passenger ages."

    def _run(self, query: str) -> str:
        """Generate age histogram."""
        try:
            # Generate the age distribution histogram
            html_fig = titanic_visualizer.create_age_distribution_histogram()
            return f"I've created a histogram showing the distribution of passenger ages. Here it is:\n{html_fig}"
        except Exception as e:
            return f"Error generating age histogram: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the run method."""
        raise NotImplementedError("AgeHistogramTool does not support async")


class ColumnAnalysisTool(BaseTool):
    name: str = "column_analyzer"
    description: str = "Analyze any column in the dataset to get statistics."

    def _run(self, query: str) -> str:
        """Analyze a column."""
        try:
            # Extract column name from query
            query_lower = query.lower()
            
            # Map common phrases to column names
            column_mapping = {
                'sex': 'Sex',
                'gender': 'Sex',
                'class': 'Pclass',
                'ticket_class': 'Pclass',
                'embarked': 'Embarked',
                'port': 'Embarked',
                'survived': 'Survived'
            }
            
            for key, col_name in column_mapping.items():
                if key in query_lower:
                    stats = titanic_data.get_column_stats(col_name)
                    
                    # Format response based on column type
                    if col_name == 'Sex':
                        male_pct = titanic_data.calculate_percentage('Sex', 'male')
                        female_pct = titanic_data.calculate_percentage('Sex', 'female')
                        return f"Passenger sex breakdown:\nMale: {male_pct:.2f}% ({stats['top_values'].get('male', 0)} passengers)\nFemale: {female_pct:.2f}% ({stats['top_values'].get('female', 0)} passengers)"
                    elif col_name == 'Pclass':
                        class1_pct = titanic_data.calculate_percentage('Pclass', 1)
                        class2_pct = titanic_data.calculate_percentage('Pclass', 2)
                        class3_pct = titanic_data.calculate_percentage('Pclass', 3)
                        return f"Passenger class breakdown:\nFirst Class: {class1_pct:.2f}% ({stats['top_values'].get(1, 0)} passengers)\nSecond Class: {class2_pct:.2f}% ({stats['top_values'].get(2, 0)} passengers)\nThird Class: {class3_pct:.2f}% ({stats['top_values'].get(3, 0)} passengers)"
                    elif col_name == 'Embarked':
                        s_pct = titanic_data.calculate_percentage('Embarked', 'S')
                        c_pct = titanic_data.calculate_percentage('Embarked', 'C')
                        q_pct = titanic_data.calculate_percentage('Embarked', 'Q')
                        return f"Port of embarkation breakdown:\nSouthampton (S): {s_pct:.2f}% ({stats['top_values'].get('S', 0)} passengers)\nCherbourg (C): {c_pct:.2f}% ({stats['top_values'].get('C', 0)} passengers)\nQueenstown (Q): {q_pct:.2f}% ({stats['top_values'].get('Q', 0)} passengers)"
                    elif col_name == 'Survived':
                        survived_pct = titanic_data.calculate_percentage('Survived', 1)
                        died_pct = titanic_data.calculate_percentage('Survived', 0)
                        return f"Survival breakdown:\nSurvived: {survived_pct:.2f}% ({stats['top_values'].get(1, 0)} passengers)\nDied: {died_pct:.2f}% ({stats['top_values'].get(0, 0)} passengers)"
                    else:
                        return f"Statistics for {col_name}: {stats}"
                        
            return "I couldn't identify which column you want analyzed. Try asking about sex, class, embarkation, or survival."
        except Exception as e:
            return f"Error analyzing column: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the run method."""
        raise NotImplementedError("ColumnAnalysisTool does not support async")


def create_titanic_agent():
    """
    Create and return a simple function to handle Titanic dataset queries.
    """
    # Just return a simple function that can handle queries directly
    def simple_query_handler(query: str) -> str:
        """
        Handle queries using our tools directly without needing a complex LLM.
        """
        # Try to identify what type of query this is and use the appropriate tool
        query_lower = query.lower()
        
        # Create instances of our tools
        percentage_tool = PassengerPercentageTool()
        count_tool = PassengerCountTool()
        avg_tool = AverageValueTool()
        hist_tool = AgeHistogramTool()
        analysis_tool = ColumnAnalysisTool()
        
        # Route to appropriate tool based on query content
        if "percentage" in query_lower or "%" in query_lower:
            return percentage_tool._run(query)
        elif "count" in query_lower or "how many" in query_lower or "number" in query_lower:
            return count_tool._run(query)
        elif "average" in query_lower or "mean" in query_lower or "fare" in query_lower:
            return avg_tool._run(query)
        elif "histogram" in query_lower or "distribution" in query_lower or "ages" in query_lower:
            return hist_tool._run(query)
        else:
            # Default to column analysis for general queries
            return analysis_tool._run(query)
    
    return simple_query_handler
