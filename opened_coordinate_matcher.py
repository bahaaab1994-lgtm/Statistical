# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 21:27:27 2025

@author: bahaa
"""

##################### Stastical Analysis
import numpy as np
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def find_nearest_location(target_lat, target_lon, data, max_distance_km=50):
    """
    Find the nearest location in the dataset to the target coordinates
    
    Parameters:
    - target_lat: Target latitude
    - target_lon: Target longitude  
    - data: DataFrame with location data
    - max_distance_km: Maximum distance to consider (default 50 km)
    
    Returns:
    - Tuple of (nearest_location_row, distance_km) or (None, None) if no location found
    """
    
    if data.empty:
        return None, None
    
    # Calculate distances to all locations
    distances = []
    
    for idx, row in data.iterrows():
        distance = haversine_distance(
            target_lat, target_lon,
            row['Latitude'], row['Longitude']
        )
        distances.append(distance)
    
    # Convert to numpy array for easier manipulation
    distances = np.array(distances)
    
    # Find the minimum distance
    min_distance_idx = np.argmin(distances)
    min_distance = distances[min_distance_idx]
    
    # Check if within acceptable range
    if min_distance <= max_distance_km:
        nearest_location = data.iloc[min_distance_idx]
        return nearest_location, min_distance
    else:
        return None, None