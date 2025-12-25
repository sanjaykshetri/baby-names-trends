"""
Compute trends and indices for immigration analysis.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


def calculate_yearly_shares(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the share of births by origin region for each year.
    
    Args:
        df: DataFrame with Year, Origin_Region, and Count columns
        
    Returns:
        DataFrame with Year, Origin_Region, Region_Births, Total_Births, and Share
    """
    # Calculate total births per year
    yearly_totals = df.groupby('Year')['Count'].sum().reset_index()
    yearly_totals.columns = ['Year', 'Total_Births']
    
    # Calculate births by region per year
    yearly_by_region = df.groupby(['Year', 'Origin_Region'])['Count'].sum().reset_index()
    yearly_by_region.columns = ['Year', 'Origin_Region', 'Region_Births']
    
    # Merge and calculate shares
    result = yearly_by_region.merge(yearly_totals, on='Year')
    result['Share'] = result['Region_Births'] / result['Total_Births'] * 100
    
    return result


def calculate_immigrant_index(
    yearly_shares: pd.DataFrame,
    immigrant_regions: List[str] = None
) -> pd.DataFrame:
    """
    Calculate the immigrant name share index.
    
    Args:
        yearly_shares: DataFrame from calculate_yearly_shares
        immigrant_regions: List of regions to include (default: all non-Anglo)
        
    Returns:
        DataFrame with Year, Immigrant_Name_Share, and Anglo_Name_Share
    """
    if immigrant_regions is None:
        immigrant_regions = ['Irish_Italian', 'Latin', 'Asian', 'African_MiddleEastern']
    
    # Calculate immigrant share
    immigrant_share = (
        yearly_shares[yearly_shares['Origin_Region'].isin(immigrant_regions)]
        .groupby('Year')['Share']
        .sum()
        .reset_index()
    )
    immigrant_share.columns = ['Year', 'Immigrant_Name_Share']
    
    # Get Anglo share
    anglo_share = (
        yearly_shares[yearly_shares['Origin_Region'] == 'Anglo']
        [['Year', 'Share']]
        .copy()
    )
    anglo_share.columns = ['Year', 'Anglo_Name_Share']
    
    # Merge
    result = immigrant_share.merge(anglo_share, on='Year', how='left')
    result['Anglo_Name_Share'] = result['Anglo_Name_Share'].fillna(0)
    
    return result


def analyze_policy_periods(
    index_df: pd.DataFrame,
    periods: Dict[str, Tuple[int, int]] = None
) -> pd.DataFrame:
    """
    Analyze average shares for different policy periods.
    
    Args:
        index_df: DataFrame with Year and Immigrant_Name_Share
        periods: Dictionary of period_name: (start_year, end_year)
        
    Returns:
        DataFrame with period statistics
    """
    if periods is None:
        periods = {
            'Pre-1924': (1880, 1923),
            'Quota Era (1924-1964)': (1924, 1964),
            'Post-1965': (1965, 2014)
        }
    
    results = []
    for period_name, (start, end) in periods.items():
        period_data = index_df[
            (index_df['Year'] >= start) & (index_df['Year'] <= end)
        ]
        
        if len(period_data) > 0:
            results.append({
                'Period': period_name,
                'Start_Year': start,
                'End_Year': end,
                'Avg_Immigrant_Share': period_data['Immigrant_Name_Share'].mean(),
                'Min_Immigrant_Share': period_data['Immigrant_Name_Share'].min(),
                'Max_Immigrant_Share': period_data['Immigrant_Name_Share'].max()
            })
    
    return pd.DataFrame(results)


def calculate_change_around_policy(
    index_df: pd.DataFrame,
    policy_year: int,
    before_years: int = 10,
    after_years: int = 10
) -> Dict[str, float]:
    """
    Calculate change in immigrant share around a policy year.
    
    Args:
        index_df: DataFrame with Year and Immigrant_Name_Share
        policy_year: Year of policy change
        before_years: Years before policy to average
        after_years: Years after policy to average
        
    Returns:
        Dictionary with before, after, and change statistics
    """
    before_data = index_df[
        (index_df['Year'] >= policy_year - before_years) &
        (index_df['Year'] < policy_year)
    ]
    
    after_data = index_df[
        (index_df['Year'] > policy_year) &
        (index_df['Year'] <= policy_year + after_years)
    ]
    
    before_avg = before_data['Immigrant_Name_Share'].mean()
    after_avg = after_data['Immigrant_Name_Share'].mean()
    
    return {
        'policy_year': policy_year,
        'before_avg': before_avg,
        'after_avg': after_avg,
        'absolute_change': after_avg - before_avg,
        'percent_change': ((after_avg / before_avg) - 1) * 100 if before_avg > 0 else np.nan
    }


def calculate_name_diversity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate name diversity metrics over time.
    
    Args:
        df: Baby names DataFrame with Year, Name, and Count
        
    Returns:
        DataFrame with diversity metrics by year
    """
    diversity = df.groupby('Year').agg({
        'Name': 'nunique',
        'Count': 'sum'
    }).reset_index()
    
    diversity.columns = ['Year', 'Unique_Names', 'Total_Births']
    diversity['Names_Per_1000_Births'] = (
        diversity['Unique_Names'] / diversity['Total_Births'] * 1000
    )
    
    return diversity
