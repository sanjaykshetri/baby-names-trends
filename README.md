# Baby Names as Time Capsules of U.S. Immigration

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![Notebook](https://img.shields.io/badge/View-Interactive%20Notebook-orange?logo=jupyter)](https://nbviewer.org/github/sanjaykshetri/baby-names-trends/blob/main/notebooks/05_complete_story.ipynb)

> **How do baby names act as time capsules of U.S. immigration history?**

## 🚀 **Quick Start: View the Complete Analysis**

**📊 [View Interactive Notebook on NBViewer](https://nbviewer.org/github/sanjaykshetri/baby-names-trends/blob/main/notebooks/05_complete_story.ipynb)** *(Recommended - all visualizations render properly)*

> ⚠️ **Note:** Interactive Plotly visualizations don't render on GitHub's notebook viewer. Use NBViewer for the full experience!

This project explores how U.S. baby name trends mirror waves of immigration and immigration policy changes, focusing on the 1924 Immigration Act (restrictive quotas) and the 1965 Hart-Celler Act (removal of national-origin quotas).

## 📊 Project Overview

Using the U.S. Social Security Administration (SSA) baby names dataset (1880-2014), we:

1. **Map names to regions of origin** (Anglo, Irish/Italian, Latin, Asian, African/Middle Eastern)
2. **Calculate regional name trends** over time
3. **Create an "Immigrant Name Share Index"** tracking immigrant-origin names
4. **Analyze correlations** with major immigration policy events

## 🎯 Key Findings

- **1924 Immigration Act Impact**: Restrictive national-origin quotas correspond with shifts in naming patterns
- **1965 Hart-Celler Act**: Dramatic increase in immigrant-origin names following quota removal
- **Modern Diversity**: Latin and Asian names show strongest growth post-1965
- **Cultural Memory**: Baby names preserve immigration history across generations

## 📁 Project Structure

```
baby-names-trends/
├── data/
│   ├── babynames.csv                   # Main SSA dataset (1.8M+ records)
│   ├── name_origin_mapping.csv         # Top 1000 names with origin classifications
│   ├── immigrant_name_index.csv        # Computed immigrant share index
│   └── regional_trends.csv             # Regional share trends by year
│
├── notebooks/
│   ├── 01_eda_babynames.ipynb         # Exploratory data analysis
│   ├── 02_name_origin_mapping.ipynb   # Name-to-origin classification
│   ├── 03_region_trends_and_index.ipynb  # Trend calculation & analysis
│   ├── 04_plots_for_presentation.ipynb   # Publication-ready visualizations
│   └── 05_complete_story.ipynb        # 🌟 COMPREHENSIVE SYNTHESIS NOTEBOOK
│
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── load_data.py                   # Data loading utilities
│   ├── compute_trends.py              # Trend calculation functions
│   ├── visuals.py                     # Visualization tools
│   └── utils.py                       # Helper functions
│
├── reports/
│   └── figures/                       # Exported charts (HTML & PNG)
│
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   cd baby-names-trends
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify data files**
   - The main dataset `data/babynames.csv` should be present
   - Dataset: 1,825,435 records covering 1880-2014

### Running the Analysis

**Option 1: Run notebooks sequentially**

Open Jupyter and run notebooks in order:

```bash
jupyter notebook
```

1. `01_eda_babynames.ipynb` - Initial exploration
2. `02_name_origin_mapping.ipynb` - Create name classifications
3. `03_region_trends_and_index.ipynb` - Calculate trends
4. `04_plots_for_presentation.ipynb` - Generate visualizations

**Option 2: Use Python modules directly**

```python
import sys
sys.path.append('src')

from load_data import load_babynames, load_name_mapping, merge_with_origins
from compute_trends import calculate_yearly_shares, calculate_immigrant_index
from visuals import plot_immigrant_index

# Load data
df = load_babynames()
mapping = load_name_mapping()
df_merged = merge_with_origins(df, mapping)

# Calculate trends
yearly_shares = calculate_yearly_shares(df_merged)
index = calculate_immigrant_index(yearly_shares)

# Visualize
fig = plot_immigrant_index(index)
fig.show()
```

## 📈 Key Visualizations

The analysis produces several publication-ready charts:

1. **Main Story Chart**: Immigrant Name Share Index with policy markers
2. **Regional Composition**: Area chart showing changing regional mix
3. **Individual Trends**: Four-panel view of each region's trajectory
4. **Period Comparison**: Bar chart comparing pre-1924, quota era, and post-1965
5. **Name Diversity**: Unique names per 1,000 births as cultural diversity proxy

All figures are saved in `reports/figures/` in both HTML (interactive) and PNG formats.

## 🔬 Methodology

### Name Classification

Names are classified into five regional origins:

- **Anglo**: Traditional English/Western European baseline (John, Mary, William, etc.)
- **Irish/Italian**: Early European immigration waves (Patrick, Giovanni, etc.)
- **Latin**: Spanish/Portuguese/Latin American (Jose, Maria, Sofia, etc.)
- **Asian**: East/South/Southeast Asian (Ming, Priya, Kim, etc.)
- **African/Middle Eastern**: African, Arabic, Middle Eastern (Muhammad, Aaliyah, etc.)

Classification uses:
1. Rule-based pattern matching
2. Manual review and adjustment
3. Coverage: ~85% of all births mapped to top 1000 names

### Immigrant Name Share Index

**Formula**: 
```
Immigrant Share (%) = (Sum of non-Anglo regional births / Total births) × 100
```

This index tracks the combined share of Irish/Italian, Latin, Asian, and African/Middle Eastern names over time.

### Policy Analysis

We analyze three key periods:

1. **Pre-1924**: Era of relatively open immigration (1880-1923)
2. **Quota Era**: National-origin restrictions (1924-1964)
3. **Post-1965**: Hart-Celler Act and renewed immigration (1965-2014)

## 📊 Data Sources

- **Primary Dataset**: U.S. Social Security Administration (SSA) National Baby Names
  - Years: 1880-2014
  - Records: 1,825,435
  - Fields: Id, Name, Year, Gender, Count
  - [SSA Baby Names Data](https://www.ssa.gov/oact/babynames/)

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **matplotlib/seaborn**: Static plots
- **Jupyter**: Interactive development environment

## 📝 Key Statistics

From the analysis:

- **1880**: ~15% immigrant-origin names
- **1924 Impact**: Shift in naming patterns during quota era
- **1965 Impact**: Sustained 3-4x increase in immigrant names post-Hart-Celler
- **2014**: ~40%+ immigrant-origin names
- **Fastest Growth**: Latin and Asian names post-1965

## 🎤 Presentation Guide

This project is designed for a 10-15 minute data storytelling presentation:

1. **Hook** (1 min): "What if baby names could tell us America's immigration story?"
2. **Data & Method** (2 min): Dataset overview and classification approach
3. **The 1924 Story** (3 min): Restrictive quotas and their cultural impact
4. **The 1965 Transformation** (4 min): Hart-Celler Act and naming revolution
5. **Modern Diversity** (3 min): Current trends and regional analysis
6. **Conclusion** (2 min): Names as cultural time capsules

Key talking points and statistics are documented in notebook 04.

## 📚 Future Extensions

Potential areas for further research:

- State-level geographic analysis
- Gender differences in naming patterns
- Correlation with actual immigration data (INS/DHS records)
- Name popularity dynamics (rise/fall rates)
- Generation-level analysis (naming of 2nd/3rd generation immigrants)
- Machine learning classification of name origins
- Social network analysis of name adoption patterns

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Enhanced name-origin classification algorithms
- Additional regional categories
- Extended time series (2015+)
- International comparisons
- Alternative diversity metrics

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- U.S. Social Security Administration for public baby names data
- Immigration historians and demographers whose work inspired this analysis
- The data science community for tools and best practices

## 📖 References

Key immigration policies analyzed:

1. **Immigration Act of 1924** (Johnson-Reed Act)
   - Established national-origin quotas
   - Favored Northern/Western European immigration
   - Severely limited Asian immigration

2. **Immigration and Nationality Act of 1965** (Hart-Celler Act)
   - Abolished national-origin quota system
   - Established family reunification preferences
   - Led to increased immigration from Asia, Latin America, and Africa

---

**Questions?** Open an issue or reach out via email.

**Citation**: If you use this analysis in your work, please cite:
```
Baby Names as Time Capsules of U.S. Immigration
[Your Name], 2025
https://github.com/yourusername/baby-names-trends
```
