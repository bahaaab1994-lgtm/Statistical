# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 21:16:47 2025

@author: bahaa
"""

################## Stastical Analysis
import pandas as pd
import numpy as np

def get_available_seasons():
    """Get list of available seasons from Excel files"""
    import glob
    import re
    
    # Look for files with spaces in names (your actual file pattern)
    excel_files = glob.glob('Predicted Freeze-Thaw Cycles (*.xlsx')
    seasons = []
    
    for file in excel_files:
        # Extract season from filename with parentheses
        match = re.search(r'\((\d{4}-\d{4})\)', file)
        if match:
            seasons.append(match.group(1))
    
    return sorted(seasons)

def load_freeze_thaw_data_by_season(season=None):
    """
    Load freeze-thaw cycle data for a specific season.
    If no season specified, loads the most recent available season.
    """
    import glob
    import re
    
    if season is None:
        # Get the most recent season
        available_seasons = get_available_seasons()
        if not available_seasons:
            return pd.DataFrame({
                'State': [], 'County': [], 'Latitude': [], 'Longitude': [],
                'Total_Freeze_Thaw_Cycles': [], 'Damaging_Freeze_Thaw_Cycles': []
            })
        season = available_seasons[-1]  # Most recent
    
    # Find the file for the specified season (with parentheses)
    file_pattern = f"Predicted Freeze-Thaw Cycles ({season}).xlsx"
    matching_files = glob.glob(file_pattern)
    
    if not matching_files:
        return pd.DataFrame({
            'State': [], 'County': [], 'Latitude': [], 'Longitude': [],
            'Total_Freeze_Thaw_Cycles': [], 'Damaging_Freeze_Thaw_Cycles': []
        })
    
    file_path = matching_files[0]
    
    try:
        # Load the Excel file
        temp_data = pd.read_excel(file_path)
        
        # Standardize column names (case-insensitive matching)
        column_mapping = {}
        for col in temp_data.columns:
            col_lower = col.lower().strip()
            if col_lower in ['state']:
                column_mapping[col] = 'State'
            elif col_lower in ['county']:
                column_mapping[col] = 'County'
            elif col_lower in ['lat', 'latitude']:
                column_mapping[col] = 'Latitude'
            elif col_lower in ['lon', 'lng', 'longitude']:
                column_mapping[col] = 'Longitude'
            elif col_lower in ['total_freeze_thaw_cycles', 'total_cycles', 'total', 'total freeze thaw cycles']:
                column_mapping[col] = 'Total_Freeze_Thaw_Cycles'
            elif col_lower in ['damaging_freeze_thaw_cycles', 'damaging_cycles', 'damaging', 'damaging freeze thaw cycles']:
                column_mapping[col] = 'Damaging_Freeze_Thaw_Cycles'
        
        # Rename columns
        temp_data = temp_data.rename(columns=column_mapping)
        
        # Check if we have required columns
        required_columns = ['State', 'County', 'Latitude', 'Longitude', 
                          'Total_Freeze_Thaw_Cycles', 'Damaging_Freeze_Thaw_Cycles']
        
        missing_columns = [col for col in required_columns if col not in temp_data.columns]
        if missing_columns:
            print(f"Warning: File '{file_path}' is missing columns: {missing_columns}")
            return pd.DataFrame({
                'State': [], 'County': [], 'Latitude': [], 'Longitude': [],
                'Total_Freeze_Thaw_Cycles': [], 'Damaging_Freeze_Thaw_Cycles': []
            })
        
        # Clean and validate data
        temp_data['Latitude'] = pd.to_numeric(temp_data['Latitude'], errors='coerce')
        temp_data['Longitude'] = pd.to_numeric(temp_data['Longitude'], errors='coerce')
        temp_data['Total_Freeze_Thaw_Cycles'] = pd.to_numeric(temp_data['Total_Freeze_Thaw_Cycles'], errors='coerce')
        temp_data['Damaging_Freeze_Thaw_Cycles'] = pd.to_numeric(temp_data['Damaging_Freeze_Thaw_Cycles'], errors='coerce')
        
        # Remove rows with missing critical data
        temp_data = temp_data.dropna(subset=['Latitude', 'Longitude', 'Total_Freeze_Thaw_Cycles', 'Damaging_Freeze_Thaw_Cycles'])
        
        # Validate coordinate ranges
        temp_data = temp_data[(temp_data['Latitude'] >= -90) & (temp_data['Latitude'] <= 90)]
        temp_data = temp_data[(temp_data['Longitude'] >= -180) & (temp_data['Longitude'] <= 180)]
        
        # Ensure damaging cycles don't exceed total cycles
        temp_data['Damaging_Freeze_Thaw_Cycles'] = np.minimum(
            temp_data['Damaging_Freeze_Thaw_Cycles'], 
            temp_data['Total_Freeze_Thaw_Cycles']
        )
        
        return temp_data
        
    except Exception as e:
        print(f"Error loading file '{file_path}': {str(e)}")
        return pd.DataFrame({
            'State': [], 'County': [], 'Latitude': [], 'Longitude': [],
            'Total_Freeze_Thaw_Cycles': [], 'Damaging_Freeze_Thaw_Cycles': []
        })

def load_freeze_thaw_data():
    """Load the most recent season's data for backward compatibility"""
    return load_freeze_thaw_data_by_season()