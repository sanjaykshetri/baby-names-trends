"""
Utility functions for baby names analysis.
"""
import pandas as pd
from typing import List, Dict, Any


def classify_name_origin(name: str) -> str:
    """
    Classify a name into an origin region using rule-based approach.
    
    Args:
        name: The name to classify
        
    Returns:
        Origin region string
    """
    # Define name patterns
    latin_names = {
        'Jose', 'Juan', 'Luis', 'Carlos', 'Jesus', 'Miguel', 'Antonio',
        'Francisco', 'Pedro', 'Jorge', 'Manuel', 'Maria', 'Carmen', 'Rosa',
        'Ana', 'Sofia', 'Isabella', 'Camila', 'Valentina', 'Diego', 'Santiago'
    }
    
    asian_names = {
        'Ming', 'Wei', 'Li', 'Chen', 'Yuki', 'Hiroshi', 'Kim', 'Park',
        'Nguyen', 'Priya', 'Raj', 'Arjun'
    }
    
    african_middle_eastern_names = {
        'Mohammed', 'Muhammad', 'Ahmad', 'Hassan', 'Omar', 'Ali', 'Ibrahim',
        'Fatima', 'Aisha', 'Aaliyah', 'Jamal', 'Malik'
    }
    
    irish_italian_names = {
        'Patrick', 'Sean', 'Connor', 'Liam', 'Ryan', 'Brendan', 'Brian',
        'Kevin', 'Colleen', 'Kathleen', 'Erin', 'Giovanni', 'Giuseppe',
        'Antonio', 'Marco', 'Angela', 'Gianna'
    }
    
    # Classify
    if name in latin_names:
        return 'Latin'
    elif name in asian_names:
        return 'Asian'
    elif name in african_middle_eastern_names:
        return 'African_MiddleEastern'
    elif name in irish_italian_names:
        return 'Irish_Italian'
    else:
        return 'Anglo'


def get_top_names(
    df: pd.DataFrame,
    n: int = 1000,
    by_gender: bool = False
) -> pd.DataFrame:
    """
    Get the top N most common names from the dataset.
    
    Args:
        df: Baby names DataFrame
        n: Number of top names to return
        by_gender: If True, get top N for each gender separately
        
    Returns:
        DataFrame with top names and their total counts
    """
    if by_gender:
        top_names = []
        for gender in df['Gender'].unique():
            gender_df = df[df['Gender'] == gender]
            top = (
                gender_df.groupby('Name')['Count']
                .sum()
                .sort_values(ascending=False)
                .head(n)
                .reset_index()
            )
            top['Gender'] = gender
            top_names.append(top)
        result = pd.concat(top_names, ignore_index=True)
    else:
        result = (
            df.groupby('Name')['Count']
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
    
    result.columns = ['Name', 'Total_Count'] if not by_gender else ['Name', 'Total_Count', 'Gender']
    return result


def filter_by_year_range(
    df: pd.DataFrame,
    start_year: int,
    end_year: int
) -> pd.DataFrame:
    """
    Filter DataFrame to a specific year range.
    
    Args:
        df: DataFrame with Year column
        start_year: Start year (inclusive)
        end_year: End year (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)].copy()


def print_summary_stats(stats: Dict[str, Any]) -> None:
    """
    Pretty print summary statistics.
    
    Args:
        stats: Dictionary of statistics
    """
    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    for key, value in stats.items():
        if isinstance(value, tuple):
            print(f"{key.replace('_', ' ').title()}: {value[0]} to {value[1]}")
        elif isinstance(value, (int, float)):
            if isinstance(value, int):
                print(f"{key.replace('_', ' ').title()}: {value:,}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("=" * 60)


def create_mapping_template(
    top_names: pd.DataFrame,
    output_path: str = '../data/name_origin_template.csv'
) -> None:
    """
    Create a template CSV for manual name-origin mapping.
    
    Args:
        top_names: DataFrame with Name and Total_Count columns
        output_path: Path to save the template
    """
    template = top_names.copy()
    template['Origin_Region'] = template['Name'].apply(classify_name_origin)
    template['Notes'] = ''
    
    template.to_csv(output_path, index=False)
    print(f"Template saved to {output_path}")
    print("Please review and adjust the Origin_Region assignments as needed.")
