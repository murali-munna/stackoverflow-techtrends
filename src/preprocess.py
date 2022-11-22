import pandas as pd
import os

def data_preprocess(path):
    """
    It takes a path to a csv file, reads it, filters the main tags , and then
    saves the stratified sampled dataframe to a new csv file
    
    Args:
      path: The path to the file that you want to preprocess.
    """
    df = pd.read_csv(path)
    
    tags_set = set(['python','c', 'c++', 'java','go','rust',
                'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
              'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
              'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
              'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
              'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services', 'gcp',
              'docker','airflow','mlflow', 'kubeflow'])
    
    df['tags1'] = df['tags'].apply(lambda x: x.split('|'))
    df['tags2'] = df['tags'].apply(lambda x: [i for i in x.split('|') if i in tags_set])
    
    # Stratified Sampling
    df1 = df.groupby('tags2_split', group_keys=False).apply(lambda x: x.sample(frac=0.5))
    
    df1['creation_month_yr'] = pd.to_datetime(df1['creation_date']).dt.to_period('M')
    df1['creation_quarter'] = pd.to_datetime(df1['creation_date']).dt.to_period('Q')
    
    df1.to_csv(os.path.join('/'.join(path.split()[:-1]), 'sof_questions_filtered.csv', header=True, index=False))



if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions.csv'
    
    data_preprocess(path)