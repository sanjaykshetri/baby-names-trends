"""
Visualization utilities for baby names analysis.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional, Dict


def add_policy_markers(
    fig: go.Figure,
    show_1924: bool = True,
    show_1965: bool = True,
    **kwargs
) -> go.Figure:
    """
    Add vertical lines for key immigration policy dates.
    
    Args:
        fig: Plotly figure object
        show_1924: Whether to show 1924 Immigration Act line
        show_1965: Whether to show 1965 Hart-Celler Act line
        **kwargs: Additional arguments passed to add_vline
        
    Returns:
        Modified figure
    """
    if show_1924:
        fig.add_vline(
            x=1924,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text="1924 Immigration Act",
            annotation_position="top left",
            **kwargs
        )
    
    if show_1965:
        fig.add_vline(
            x=1965,
            line_dash="dash",
            line_color="green",
            line_width=2,
            annotation_text="1965 Hart-Celler Act",
            annotation_position="top right",
            **kwargs
        )
    
    return fig


def plot_immigrant_index(
    index_df: pd.DataFrame,
    title: str = "Baby Names as Immigration Time Capsules",
    height: int = 600,
    width: int = 1200
) -> go.Figure:
    """
    Create the main immigrant name share index plot.
    
    Args:
        index_df: DataFrame with Year, Immigrant_Name_Share, Anglo_Name_Share
        title: Plot title
        height: Figure height in pixels
        width: Figure width in pixels
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Immigrant share
    fig.add_trace(go.Scatter(
        x=index_df['Year'],
        y=index_df['Immigrant_Name_Share'],
        mode='lines',
        name='Immigrant-Origin Names',
        line=dict(color='#2E86AB', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 134, 171, 0.2)'
    ))
    
    # Anglo share (baseline)
    fig.add_trace(go.Scatter(
        x=index_df['Year'],
        y=index_df['Anglo_Name_Share'],
        mode='lines',
        name='Anglo Names',
        line=dict(color='#A4A4A4', width=2, dash='dot'),
        opacity=0.6
    ))
    
    # Add policy markers
    fig = add_policy_markers(fig)
    
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title='Share of Births (%)',
        template='plotly_white',
        height=height,
        width=width,
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98)
    )
    
    return fig


def plot_regional_composition(
    regional_df: pd.DataFrame,
    immigrant_regions: List[str] = None,
    title: str = "Regional Composition of Immigrant-Origin Names",
    height: int = 600,
    width: int = 1200
) -> go.Figure:
    """
    Create area chart showing regional composition over time.
    
    Args:
        regional_df: DataFrame with Year, Origin_Region, Share
        immigrant_regions: List of regions to plot
        title: Plot title
        height: Figure height
        width: Figure width
        
    Returns:
        Plotly figure
    """
    if immigrant_regions is None:
        immigrant_regions = ['Irish_Italian', 'Latin', 'Asian', 'African_MiddleEastern']
    
    plot_data = regional_df[regional_df['Origin_Region'].isin(immigrant_regions)]
    
    color_map = {
        'Irish_Italian': '#E63946',
        'Latin': '#F4A261',
        'Asian': '#2A9D8F',
        'African_MiddleEastern': '#E76F51'
    }
    
    fig = px.area(
        plot_data,
        x='Year',
        y='Share',
        color='Origin_Region',
        color_discrete_map=color_map,
        title=title,
        labels={'Share': 'Share of Births (%)', 'Origin_Region': 'Region'},
        template='plotly_white'
    )
    
    # Add policy markers
    fig = add_policy_markers(fig)
    
    fig.update_layout(
        height=height,
        width=width,
        hovermode='x unified'
    )
    
    return fig


def plot_period_comparison(
    period_stats: pd.DataFrame,
    title: str = "Immigrant Name Share by Policy Era",
    height: int = 600,
    width: int = 1000
) -> go.Figure:
    """
    Create bar chart comparing different policy periods.
    
    Args:
        period_stats: DataFrame with Period and Avg_Immigrant_Share
        title: Plot title
        height: Figure height
        width: Figure width
        
    Returns:
        Plotly figure
    """
    fig = px.bar(
        period_stats,
        x='Period',
        y='Avg_Immigrant_Share',
        color='Avg_Immigrant_Share',
        color_continuous_scale='Blues',
        title=title,
        labels={'Avg_Immigrant_Share': 'Average Share (%)'},
        text='Avg_Immigrant_Share'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    
    fig.update_layout(
        height=height,
        width=width,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def save_figure(
    fig: go.Figure,
    filename: str,
    output_dir: str = '../reports/figures',
    formats: List[str] = ['html', 'png']
) -> None:
    """
    Save a Plotly figure in multiple formats.
    
    Args:
        fig: Plotly figure to save
        filename: Base filename (without extension)
        output_dir: Output directory path
        formats: List of formats to save ('html', 'png', 'pdf', etc.)
    """
    from pathlib import Path
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for fmt in formats:
        if fmt == 'html':
            fig.write_html(str(output_path / f"{filename}.html"))
        else:
            fig.write_image(str(output_path / f"{filename}.{fmt}"))
