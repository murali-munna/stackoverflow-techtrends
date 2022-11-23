# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:57:42 2022

@author: raghu
"""


from heatmaps import _filter_required_columns
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame


def _replace_country_name_for_consistency(df,location_column,replace_map):
    '''


    Parameters
    ----------
    df : datframe
        dataframe in which values are to be replaced
    location_column : string
        column containing location
    replace_map : dict
        dictionary with alternate names

    Returns
    -------
    df : dataframe
        dataframe with replaced names

    '''
    
    assert(isinstance(df,pd.DataFrame))
    assert(isinstance(location_column,str))
    assert(isinstance(replace_map, dict))
    
    df[location_column] = df[location_column].replace(replace_map)
    return df


def _plot_geographical_map(df,column_to_plot,title_of_plot):
    '''
    

    Parameters
    ----------
    df : dataframe
        dataframe with co-occurences
    column_to_plot : str
        column to plot
    title_of_plot : str
        plot title

    Returns
    -------
    None.

    '''
    
    assert(isinstance(df,pd.DataFrame))
    assert(isinstance(column_to_plot,str))
    assert(isinstance(title_of_plot, str))
    
    df[column_to_plot]=df[column_to_plot].fillna(0)
    fig, ax = plt.subplots(1, figsize=(12, 12))
    ax.axis('off')
    ax.set_title(title_of_plot,fontdict={'fontsize': '15', 'fontweight' : '3'})
    fig = df.plot(column=column_to_plot, cmap='Dark2', linewidth=0.5, ax=ax, edgecolor='0.2',legend=True)


def _merge_worldmap_data_with_locationss(locations_df):
    '''
    

    Parameters
    ----------
    locations_df : dataframe
        dataframe with location data

    Returns
    -------
    merged_df : dataframe
        dataframe merged with world map data

    '''
    assert(isinstance(locations_df,pd.DataFrame))
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world.merge(locations_df, how='left', left_on=['name'], right_on=['q_user_location'])
    merged_df = GeoDataFrame(world)
    return merged_df


def _aggregate_location_data(raw_df,locations):
    '''
    

    Parameters
    ----------
    raw_df : dataframe
        dataframe with all locations
    locations : list
        locations of interest

    Returns
    -------
    locations_df : dataframe
        dataframe with locations of interest

    '''
    
    assert(isinstance(raw_df,pd.DataFrame))
    assert(isinstance(locations,list))
    
    loc_df = raw_df[raw_df['q_user_location'].isin(locations)]
    locations_df = loc_df.groupby(['q_user_location']).agg(
        questions=pd.NamedAgg(column='q_user_location', aggfunc='count')).reset_index().sort_values('questions', ascending=False)
    return locations_df
    

if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = 'C:/Users/raghu/3D Objects/AAAAcads/143/Project/sdf.csv'
    data = pd.read_csv(path)
    
    
    filter_cols = ['id', 'tags', 'q_user_location']
    data = _filter_required_columns(data,filter_cols)
    
    location_column='q_user_location'
    replace_map= {'United States': 'United States of America'}
    data = _replace_country_name_for_consistency(data,location_column,replace_map)
    
    locations = ['India','Germany','United States of America','United Kingdom','Israel',\
            'France','Canada','Italy','Netherlands','Australia','China','Russia',\
                'Japan','Sweden','Brazil','Switzerland']
        
    locations_df = _aggregate_location_data(data,locations)
    merged_location_data = _merge_worldmap_data_with_locationss(locations_df)
    
    column_to_plot = 'questions'
    title_of_plot = 'No. of Questions from each country'
    _plot_geographical_map(merged_location_data,column_to_plot,title_of_plot)
    

    
    
