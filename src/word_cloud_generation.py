import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import string
import os
from preprocess import get_tags_set, get_topic_tags, create_tag_fields

# Set of tags by topic
topic_tags = get_topic_tags()

# Set of tags
tags_set = get_tags_set()

# List of irrelevant words in titles
irrelevant = ['one', 'two', 'three', 'another', 'statement', 'problem', 'word', 'instead', 'group', 'studio', 'problems', 'connection', 'trouble', 
               'items', 'unit', 'status', 'will', 'issues', 'member', 'action', 'difference', 'already', 'size', 'line', 'really', 'always',
               'example', 'way', 'thing', 'may', 'nothing', 'number', 'anyone', 'well', 'anything', 'using', 'different', 'without', 'via',
               'specific', 'working', 'need', 'work', 'single', 'doesnt', 'adding', 'want', 'given', 'simple', 'use']


def str_preprocess(s):
  """
  It takes a string, makes it lowercase, and removes all punctuation
  
  Args:
    s: the string to be processed
  
  Returns:
    A string with all lowercase letters and no punctuation.
  """
  assert isinstance(s, str)
  
  s = s.lower()
  s = "".join([char for char in s if char not in string.punctuation])
  return s


def topic_retrieval(s):
  """
  Retrieve the list of topics associated with the tags
  
  Args:
    s: a list of tags
  
  Returns:
    A list of topics that are associated with the tags in the input string.
  """
  assert isinstance(s, list)
  
  topic_list = []
  for tag in s:
    for topic in topic_tags:
      if tag in topic_tags[topic]:
        topic_list.append(topic)
  return topic_list


def df_transforms(df):
  """
  It takes a dataframe, transforms the title column, creates new columns for tags and topics
  
  Args:
    df: the dataframe
  
  Returns:
    A dataframe with the following columns:
  """
  assert isinstance(df, pd.DataFrame)
  
  df['title'] = df.title.transform(str_preprocess)
  df = create_tag_fields(df)
  df['tag_topic'] = df['tags_filtered'].apply(topic_retrieval)
  return df


def text_generation(df):
  """
  It takes a dataframe as input, and returns a string of all the titles in the dataframe
  
  Args:
    df: the dataframe
  
  Returns:
    A string of the title column
  """
  assert isinstance(df, pd.DataFrame)
  
  return " ".join(s for s in df.title)


def generate_cloud(text, stopwords, filename='word_cloud.png'):
  """
  It takes in a string of text, a list of stopwords, and a filename, and generates a word cloud image
  of the text
  
  Args:
    text: The text that you want to generate the word cloud for.
    stopwords: a list of words that you want to exclude from the word cloud.
    filename: The name of the file that will be saved to the plots folder. Defaults to word_cloud.png
  """
  assert isinstance(text, str)
  assert isinstance(stopwords, list)
  assert isinstance(filename, str)
  
  wordcloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400).generate(text)
  plt.figure(figsize=(20, 20))
  plt.imshow(wordcloud)
  plt.axis("off")
  plt.title("Most Commonly Found Words in the Title of StackOverflow Posts")
  plt.savefig(os.path.join('../plots/', filename))


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
