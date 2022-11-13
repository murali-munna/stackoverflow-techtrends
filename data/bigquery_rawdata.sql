-- select *, SPLIT(tags, '|') as tags_split
-- from bigquery-public-data.stackoverflow.posts_questions
-- from bigquery-public-data.stackoverflow.posts_answers
-- from bigquery-public-data.stackoverflow.users
-- from bigquery-public-data.stackoverflow.badges
-- limit 100;
-- group by 1
-- order by 1

select id, title, accepted_answer_id, answer_count, comment_count, creation_date, favorite_count, owner_user_id, 
score, tags, view_count
from bigquery-public-data.stackoverflow.posts_questions
where 
-- tags like '%c%'
-- REGEXP_CONTAINS(tags, 
-- 'python|java|go|rust|pandas|numpy|scipy|scikit-learn|pytorch|tensorflow|keras|spacy|nltk|opencv|huggingface|matplotlib|seaborn|azure|google-cloud-platform|aws|docker|airflow|mlflow'
-- )
EXISTS (SELECT *
              FROM UNNEST(split(tags,'|')) AS t
              WHERE t in (
                'python','c', 'c++', 'java','go','rust',
                'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
              'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
              'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
              'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
              'azure','google-cloud-platform','aws', 'mlops',
              'docker','airflow','mlflow', 'kubeflow')
      );

-- select post_type_id, count(1)
-- from bigquery-public-data.stackoverflow.posts_questions
-- group by 1
-- order by 1
