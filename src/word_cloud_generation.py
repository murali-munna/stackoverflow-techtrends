import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import string
import os

# Set of tags by topic
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

# Set of tags
tags_set = set(['python','c', 'c++', 'java','go','rust',
                'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
              'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
              'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
              'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
              'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services', 'gcp',
              'docker','airflow','mlflow', 'kubeflow'])

# List of irrelevant words in titles
irrelevant = ['one', 'two', 'three', 'another', 'statement', 'problem', 'word', 'instead', 'group', 'studio', 'problems', 'connection', 'trouble', 
               'items', 'unit', 'status', 'will', 'issues', 'member', 'action', 'difference', 'already', 'size', 'line', 'really', 'always',
               'example', 'way', 'thing', 'may', 'nothing', 'number', 'anyone', 'well', 'anything', 'using', 'different', 'without', 'via',
               'specific', 'working', 'need', 'work', 'single', 'doesnt', 'adding', 'want', 'given', 'simple', 'use']

def str_preprocess(s):
  s = s.lower()
  s = "".join([char for char in s if char not in string.punctuation])
  return s

def topic_retrieval(s):
  topic_list = []
  for tag in s:
    for topic in topic_tags:
      if tag in topic_tags[topic]:
        topic_list.append(topic)
  return topic_list

def df_transforms(df):
  df['title'] = df.title.transform(str_preprocess)
  df['tags1'] = df['tags'].apply(lambda x: x.split('|'))
  df['tags2'] = df['tags'].apply(lambda x: [i for i in x.split('|') if i in tags_set])
  df['tag_topic'] = df['tags2'].apply(topic_retrieval)
  return df

def text_generation(df):
  return " ".join(s for s in df.title)

def generate_cloud(text, stopwords, filename='word_cloud.png'):
  wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400).generate(text)
  plt.figure(figsize=(20, 20))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.title("Most Commonly Found Words in the Title of StackOverflow Posts")
  plt.savefig(os.path.join('/'.join(path.split('/')[:-1]), filename))


if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions_filtered.csv'
    
    df = pd.read_csv(path)

    # Apply necessary df transforms before generating clouds
    df = df_transforms(df)

    # Define two sets of stopwords
    stopwords_wo_tags = set(set(list(STOPWORDS) + irrelevant))
    stopwords_w_tags =  set(list(STOPWORDS) + list(tags_set) + irrelevant)

    # Generate word cloud of overall df with irrelevant words removed
    text = text_generation(df)
    generate_cloud(text, stopwords_wo_tags, 'overall_word_cloud_w_tags.png')

    # Generate same word cloud with tag words filtered out
    generate_cloud(text, stopwords_w_tags, 'overall_word_cloud_wo_tags.png')

    # Generate word cloud for each tag topic
    for topic in topic_tags:
      sub_df = df[[topic in d for d in list(df['tag_topic'])]]
      sub_text = text_generation(sub_df)
      generate_cloud(sub_text, stopwords_w_tags, topic + '_word_cloud.png')



