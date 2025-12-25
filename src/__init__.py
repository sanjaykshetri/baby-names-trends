"""
Baby Names Immigration Analysis Package

This package provides tools for analyzing U.S. baby names as indicators
of immigration trends and cultural change.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .load_data import (
    load_babynames,
    load_name_mapping,
    merge_with_origins,
    get_data_summary
)

from .compute_trends import (
    calculate_yearly_shares,
    calculate_immigrant_index,
    analyze_policy_periods,
    calculate_change_around_policy,
    calculate_name_diversity
)

from .visuals import (
    add_policy_markers,
    plot_immigrant_index,
    plot_regional_composition,
    plot_period_comparison,
    save_figure
)

from .utils import (
    classify_name_origin,
    get_top_names,
    filter_by_year_range,
    print_summary_stats
)

__all__ = [
    'load_babynames',
    'load_name_mapping',
    'merge_with_origins',
    'get_data_summary',
    'calculate_yearly_shares',
    'calculate_immigrant_index',
    'analyze_policy_periods',
    'calculate_change_around_policy',
    'calculate_name_diversity',
    'add_policy_markers',
    'plot_immigrant_index',
    'plot_regional_composition',
    'plot_period_comparison',
    'save_figure',
    'classify_name_origin',
    'get_top_names',
    'filter_by_year_range',
    'print_summary_stats'
]
