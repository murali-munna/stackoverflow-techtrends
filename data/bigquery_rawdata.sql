
WITH questions AS
(
select
id, title, accepted_answer_id, answer_count, comment_count, creation_date, favorite_count, owner_user_id, 
score, tags, view_count
from bigquery-public-data.stackoverflow.posts_questions
where 
EXISTS (SELECT *
              FROM UNNEST(split(tags,'|')) AS t
              WHERE t in (
                'python','c', 'c++', 'java','go','rust',
                'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
              'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
              'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
              'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
              'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services', 'gcp',
              'docker','airflow','mlflow', 'kubeflow')
      )
)
select a.*, b.location as q_user_location,
from questions a 
left join bigquery-public-data.stackoverflow.users as b
on a.owner_user_id = b.id

-- select *, SPLIT(tags, '|') as tags_split
-- from bigquery-public-data.stackoverflow.posts_questions
-- from bigquery-public-data.stackoverflow.posts_answers
-- from bigquery-public-data.stackoverflow.users
-- from bigquery-public-data.stackoverflow.badges
-- limit 100;
-- group by 1
-- order by 1
