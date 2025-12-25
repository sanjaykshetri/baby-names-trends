# Quick data generation script
# This script generates all required data files for the analysis

import pandas as pd
import numpy as np
from pathlib import Path

print("Loading baby names data...")
df = pd.read_csv('data/babynames.csv')
print(f"Loaded {len(df):,} records")

# Step 1: Generate top 1000 names file
print("\nStep 1: Generating top 1000 names...")
top_names_overall = df.groupby('Name')['Count'].sum().sort_values(ascending=False)

top_1000_names = top_names_overall.head(1000).reset_index()
top_1000_names.columns = ['Name', 'Total_Count']

# Add dominant gender
def get_dominant_gender(name):
    name_data = df[df['Name'] == name].groupby('Gender')['Count'].sum()
    return name_data.idxmax() if len(name_data) > 0 else 'U'

print("  Adding gender information...")
top_1000_names['Dominant_Gender'] = top_1000_names['Name'].apply(get_dominant_gender)

output_path = Path('data/top_1000_names_for_mapping.csv')
top_1000_names.to_csv(output_path, index=False)
print(f"  ✓ Saved {output_path}")

# Step 2: Generate name origin mapping
print("\nStep 2: Creating name origin mapping...")

# Define name patterns
latin_names = {
    'Jose', 'Juan', 'Luis', 'Carlos', 'Jesus', 'Miguel', 'Antonio', 'Francisco',
    'Pedro', 'Jorge', 'Manuel', 'Rafael', 'Ramon', 'Fernando', 'Ricardo', 'Roberto',
    'Eduardo', 'Julio', 'Enrique', 'Pablo', 'Raul', 'Mario', 'Sergio', 'Ruben',
    'Hector', 'Oscar', 'Cesar', 'Diego', 'Javier', 'Angel', 'Marco', 'Alejandro',
    'Maria', 'Carmen', 'Rosa', 'Ana', 'Elena', 'Teresa', 'Lucia', 'Gloria',
    'Isabel', 'Dolores', 'Guadalupe', 'Josefina', 'Beatriz', 'Catalina', 'Margarita',
    'Adriana', 'Alicia', 'Gabriela', 'Isabella', 'Sofia', 'Camila', 'Valentina',
    'Natalia', 'Daniela', 'Victoria', 'Andrea', 'Diana', 'Angelica', 'Selena', 'Santiago'
}

asian_names = {
    'Ming', 'Mei', 'Wei', 'Li', 'Chen', 'Wang', 'Zhang', 'Liu', 'Yang',
    'Yuki', 'Akira', 'Kenji', 'Sakura', 'Hiroshi', 'Takashi', 'Yumi',
    'Kim', 'Park', 'Lee', 'Jung', 'Min', 'Jin', 'Hyun', 'Ji', 'Sung',
    'Anh', 'Linh', 'Minh', 'Nguyen', 'Tran', 'Pham',
    'Priya', 'Ravi', 'Amit', 'Raj', 'Kumar', 'Arjun', 'Krishna', 'Deepak'
}

african_middle_eastern_names = {
    'Mohammed', 'Muhammad', 'Ahmad', 'Hassan', 'Omar', 'Ali', 'Ibrahim', 'Khalid',
    'Fatima', 'Aisha', 'Amina', 'Zahra', 'Layla', 'Noor', 'Mariam', 'Yasmin',
    'Jamal', 'Malik', 'Rashid', 'Kareem', 'Tariq', 'Karim',
    'Kwame', 'Kofi', 'Amara', 'Zuri', 'Imani', 'Nia', 'Aaliyah', 'Zara',
    'Tyrone', 'Darnell', 'Latoya', 'Keisha', 'Tanisha', 'Ebony', 'Mohamed'
}

irish_italian_names = {
    'Patrick', 'Sean', 'Connor', 'Liam', 'Ryan', 'Brendan', 'Brian', 'Kevin',
    'Colleen', 'Kathleen', 'Maureen', 'Bridget', 'Erin', 'Kelly', 'Shannon',
    'Giovanni', 'Giuseppe', 'Antonio', 'Salvatore', 'Vincenzo', 'Marco', 'Luigi',
    'Carla', 'Gina', 'Rosa', 'Francesca', 'Isabella', 'Lucia', 'Angela',
    'Gianna', 'Alessandra', 'Bianca', 'Chiara', 'Anthony', 'Angelo', 'Dante', 'Aidan', 'Ciara'
}

anglo_names = {
    'John', 'William', 'James', 'Robert', 'Michael', 'David', 'Richard', 'Charles',
    'Joseph', 'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Donald', 'Mark',
    'Paul', 'Steven', 'Andrew', 'Kenneth', 'Joshua', 'George', 'Edward',
    'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan',
    'Jessica', 'Sarah', 'Nancy', 'Karen', 'Betty', 'Helen', 'Dorothy', 'Margaret',
    'Emily', 'Emma', 'Olivia', 'Ava', 'Sophia', 'Mia', 'Charlotte', 'Amelia'
}

def classify_name(name):
    if name in latin_names:
        return 'Latin'
    elif name in asian_names:
        return 'Asian'
    elif name in african_middle_eastern_names:
        return 'African_MiddleEastern'
    elif name in irish_italian_names:
        return 'Irish_Italian'
    elif name in anglo_names:
        return 'Anglo'
    else:
        return 'Anglo'  # Default

print("  Classifying names...")
top_1000_names['Origin_Region'] = top_1000_names['Name'].apply(classify_name)

mapping_path = Path('data/name_origin_mapping.csv')
top_1000_names.to_csv(mapping_path, index=False)
print(f"  ✓ Saved {mapping_path}")
print(f"  Distribution: {top_1000_names['Origin_Region'].value_counts().to_dict()}")

# Step 3: Merge and calculate trends
print("\nStep 3: Calculating regional trends...")

mapping_df = top_1000_names[['Name', 'Origin_Region']].copy()
df_with_origin = df.merge(mapping_df, on='Name', how='left')
df_with_origin['Origin_Region'] = df_with_origin['Origin_Region'].fillna('Other')

print("  Computing yearly shares...")
yearly_totals = df_with_origin.groupby('Year')['Count'].sum().reset_index()
yearly_totals.columns = ['Year', 'Total_Births']

yearly_by_region = df_with_origin.groupby(['Year', 'Origin_Region'])['Count'].sum().reset_index()
yearly_by_region.columns = ['Year', 'Origin_Region', 'Region_Births']

yearly_by_region = yearly_by_region.merge(yearly_totals, on='Year')
yearly_by_region['Share'] = yearly_by_region['Region_Births'] / yearly_by_region['Total_Births'] * 100

regional_path = Path('data/regional_trends.csv')
yearly_by_region.to_csv(regional_path, index=False)
print(f"  ✓ Saved {regional_path}")

# Step 4: Calculate immigrant index
print("\nStep 4: Creating immigrant name share index...")

immigrant_regions = ['Irish_Italian', 'Latin', 'Asian', 'African_MiddleEastern']

immigrant_share = (
    yearly_by_region[yearly_by_region['Origin_Region'].isin(immigrant_regions)]
    .groupby('Year')['Share']
    .sum()
    .reset_index()
)
immigrant_share.columns = ['Year', 'Immigrant_Name_Share']

anglo_share = (
    yearly_by_region[yearly_by_region['Origin_Region'] == 'Anglo']
    [['Year', 'Share']]
    .copy()
)
anglo_share.columns = ['Year', 'Anglo_Name_Share']

index_df = immigrant_share.merge(anglo_share, on='Year', how='left')
index_df['Anglo_Name_Share'] = index_df['Anglo_Name_Share'].fillna(0)

index_path = Path('data/immigrant_name_index.csv')
index_df.to_csv(index_path, index=False)
print(f"  ✓ Saved {index_path}")

print("\n" + "="*60)
print("DATA GENERATION COMPLETE!")
print("="*60)
print(f"\nGenerated files:")
print(f"  ✓ top_1000_names_for_mapping.csv")
print(f"  ✓ name_origin_mapping.csv")
print(f"  ✓ regional_trends.csv")
print(f"  ✓ immigrant_name_index.csv")
print(f"\nYou can now run notebook 04 (plots_for_presentation.ipynb)")
