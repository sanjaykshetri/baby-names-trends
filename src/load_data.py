"""
Load and preprocess baby names data.
"""
import pandas as pd
from pathlib import Path
from typing import Tuple


def load_babynames(data_path: str = '../data/babynames.csv') -> pd.DataFrame:
    """
    Load the baby names dataset.
    
    Args:
        data_path: Path to the baby names CSV file
        
    Returns:
        DataFrame with baby names data
    """
    df = pd.read_csv(data_path)
    return df


def load_name_mapping(mapping_path: str = '../data/name_origin_mapping.csv') -> pd.DataFrame:
    """
    Load the name-to-origin mapping.
    
    Args:
        mapping_path: Path to the mapping CSV file
        
    Returns:
        DataFrame with name-origin mappings
    """
    df = pd.read_csv(mapping_path)
    return df[['Name', 'Origin_Region']]


def merge_with_origins(
    names_df: pd.DataFrame,
    mapping_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge baby names dataset with origin mapping.
    
    Args:
        names_df: Baby names DataFrame
        mapping_df: Name-origin mapping DataFrame
        
    Returns:
        Merged DataFrame with origin information
    """
    merged = names_df.merge(mapping_df, on='Name', how='left')
    merged['Origin_Region'] = merged['Origin_Region'].fillna('Other')
    return merged


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for the dataset.
    
    Args:
        df: Baby names DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    return {
        'total_records': len(df),
        'total_births': df['Count'].sum(),
        'unique_names': df['Name'].nunique(),
        'year_range': (df['Year'].min(), df['Year'].max()),
        'years_covered': df['Year'].nunique()
    }
