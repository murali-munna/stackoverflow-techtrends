# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:01:20 2022

@author: raghu ram kishore (A59019906)
"""
from preprocess import get_tags_set
from preprocess import create_tag_fields
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt



def _get_co_occurence_matrix(df,tags_all_column,tags_set):
    '''
    Get co-occurence matrix based on if two words are present in the same sentence.
    It utilizes the sklearn Count Vectorizer to implement this.

    Parameters
    ----------
    df : datframe
        data from which to build co-occurences
    tags_all_column : string
        name of the column from which co-occurences are to be calculated
    tags_set : set
        tag names

    Returns
    -------
    co_occurence_df : dataframe
        co-occurences of tags

    '''
    
    assert(isinstance(df,pd.DataFrame))
    assert(isinstance(tags_set,set))
    assert(isinstance(tags_all_column, str))
    
    
    tags_list = df[tags_all_column].tolist()
    tags_sents = [' '.join(x) for x in tags_list]
    count_model = CountVectorizer(ngram_range=(1,1), vocabulary=list(tags_set))
    counts = count_model.fit_transform(tags_sents)
    co_occurence = (counts.T * counts)
    co_occurence.setdiag(0)
    co_occurence_matrix = co_occurence.todense()
    co_occurence_df = pd.DataFrame(co_occurence_matrix,columns = count_model.vocabulary_.keys())
    return co_occurence_df


def _remove_elements_from_set(tags_set,unwanted_elements):
    '''
    Only take the top tags that we are interested in

    Parameters
    ----------
    tags_set : set
        all tags
    unwanted_elements : list
        list of unwanted elements

    Returns
    -------
    tags_set : set
        filtered tags

    '''

    assert(isinstance(tags_set,set))
    assert(isinstance(unwanted_elements,list))
    
    
    unwanted_elements = set(unwanted_elements)
    for x in unwanted_elements:
        tags_set.remove(x)
            
    return tags_set


def _filter_required_columns(df,filter_cols):
    '''
    Filter the columns of the dataframe
    
    Parameters
    ----------
    df : dataframe
        input data
    filter_cols : list
        list of required columns

    Returns
    -------
    df : dataframe
        filtered dataframe

    '''
    
    assert(isinstance(df,pd.DataFrame))
    assert(isinstance(filter_cols,list))
    
    df = df[filter_cols]
    return df
    
   
def _get_heatmaps(df):
    '''
    Plot the heatmap of the co-occurence matrix

    Parameters
    ----------
    df : dataframe
        co-occurence dataframe from which heat map is to be plotted

    Returns
    -------
    None.

    '''
    
    assert(isinstance(df,pd.DataFrame))
    
    # plot parameters
    figure(figsize=(18, 18), dpi=200)
    plt.imshow(df, cmap ="nipy_spectral")#nipy_spectral,Dark2
    plt.colorbar()
      
    # Assigning labels of x-axis 
    # according to dataframe
    plt.xticks(range(len(df)), df.columns,rotation='vertical')
      
    # Assigning labels of y-axis 
    # according to dataframe
    plt.yticks(range(len(df)), df.columns)
      
    # Displaying the figure
    plt.show()


if __name__=='__main__':
    

    path = 'C:/Users/raghu/3D Objects/AAAAcads/143/Project/sdf.csv'
    data = pd.read_csv(path)
    
    
    filter_cols = ['id', 'tags', 'q_user_location']
    data = _filter_required_columns(data,filter_cols)

    tags_set = get_tags_set()
    unwanted_elements = ['machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence','python','bigdata']
    tags_set = _remove_elements_from_set(tags_set,unwanted_elements)
    
    
    tags_all_column ='tags_all'
    tags_column = 'tags'
    tags_main ='tags_main'
    
    data  = create_tag_fields(data)
    
    co_occurence_df = _get_co_occurence_matrix(data,tags_all_column,tags_set)
    _get_heatmaps(co_occurence_df)
    


