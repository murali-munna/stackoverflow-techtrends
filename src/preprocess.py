import pandas as pd
import os


def get_tags_set():
    """
    It returns a set of tags that we are interested in
    
    Returns:
      A set of tags
    """
    tags_set = set(['python','c', 'c++', 'java','go','rust',
                'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
              'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
              'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
              'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
              'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services', 'gcp',
              'docker','airflow','mlflow', 'kubeflow'])
    return tags_set


def get_topic_tags():
    """
    It returns a dictionary mapping the key topic to a list of tags
    
    Returns:
      A dictionary of lists.
    """
    topic_tags = { 
        'prog': ['c', 'c++', 'java', 'python', 'go', 'rust'],
        'python_pkgs': ['bokeh', 'dask', 'huggingface', 'keras', 'matplotlib', 'mlflow', 'airflow', 'fastai', 'nltk', 'numpy', 
                        'opencv', 'pandas', 'plotly', 'pycaret', 'pyspark', 'pytorch', 'pyviz', 'scikit-learn', 'scipy', 'seaborn',
                        'spacy', 'statsmodels', 'tensorflow'],
        'big_data': ['dask', 'bigdata', 'hadoop', 'spark', 'pyspark'],
        'ds': ['artificial-intelligence', 'computer-vision', 'data-science', 'deep-learning', 'machine-learning', 'nlp', 'reinforcement-learning', 'visualization'],
        'ds_fields': ['artificial-intelligence', 'computer-vision', 'nlp', 'reinforcement-learning', 'visualization'],
        'cloud': ['aws', 'amazon-web-services', 'azure', 'cloud', 'google-cloud-platform', ],
        'mlops': ['airflow', 'docker', 'fastai', 'kubeflow', 'mlflow', 'mlops', ],
    }
    return topic_tags


def create_tag_fields(df):
    """
    It takes a dataframe and creates two new columns: one with all the tags and one with only the tags
    that are in the tags_set
    
    Args:
      df: the dataframe
    
    Returns:
      A dataframe with two new columns: tags_all and tags_filtered.
    """
    tags_set = get_tags_set()
    df['tags_all'] = df['tags'].apply(lambda x: x.split('|'))
    df['tags_filtered'] = df['tags'].apply(lambda x: [i for i in x.split('|') if i in tags_set])
    return df


def create_date_fields(df):
    """
    It takes a dataframe and creates two new columns, one for the month and year of the creation date,
    and one for the quarter of the creation date
    
    Args:
      df: the dataframe you want to create the fields in
    
    Returns:
      A dataframe with the new columns
    """
    df['creation_month_yr'] = pd.to_datetime(df['creation_date']).dt.to_period('M')
    df['creation_quarter'] = pd.to_datetime(df['creation_date']).dt.to_period('Q')
    return df


def data_preprocess(path):
    """
    It takes a path to a csv file, reads it, filters the main tags , and then
    saves the stratified sampled dataframe to a new csv file
    
    Args:
      path: The path to the file that you want to preprocess.
    """
    df = pd.read_csv(path)
    
    tags_set = get_tags_set()
    
    df = create_tag_fields(df)
    
    # Stratified Sampling
    df1 = df.groupby('tags_filtered_split', group_keys=False).apply(lambda x: x.sample(frac=0.5))
    
    df1 = create_date_fields(df1)
    
    df1.to_csv(os.path.join(os.path.dirname(os.path.dirname(path)), 
                            'sof_questions_filtered.csv', header=True, index=False))



if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions.csv'
    
    data_preprocess(path)