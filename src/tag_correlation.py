import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

'''
Created by Andy Fong (A15486467)
'''

tags_set = set(['python','c', 'c++', 'java','go','rust', 
           'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
           'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
           'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
           'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
           'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services',
           'docker','airflow','mlflow', 'kubeflow', 'python-3.x', 'dataframe', 'python-2.7'])

main_tags = ['python','c', 'c++', 'java','go','rust', 
           'data-science', 'machine-learning', 'deep-learning', 'computer-vision', 'artificial-intelligence', 'nlp','reinforcement-learning',
           'pandas','numpy', 'dask', 'pyspark', 'hadoop', 'spark', 'scipy', 'statsmodels', 'scikit-learn','pytorch','tensorflow','keras',
           'spacy','nltk','opencv','huggingface','matplotlib','seaborn', 'fastai',
           'bokeh', 'pyviz', 'pycaret', 'plotly', 'visualization', 'cloud', 'bigdata',
           'azure','google-cloud-platform','aws', 'mlops', 'amazon-web-services',
           'docker','airflow','mlflow', 'kubeflow']

# 

def tag_dict(m_tags, df_tags):
    '''
    creates dictionary for all of the main tags excluding each other based on frequency
    '''
    tag_relation_dict = dict()
    for prim_tag in m_tags:
        tag_relation_dict[prim_tag] = dict()
        for post_tags in df_tags:
            if prim_tag in post_tags:
                for curr_tag in post_tags:
                    if(curr_tag in tag_relation_dict[prim_tag].keys()):
                        tag_relation_dict[prim_tag][curr_tag] += 1
                    elif(curr_tag not in tags_set):
                        tag_relation_dict[prim_tag][curr_tag] = 1
                        # all_possible_tags.add(curr_tag)
                    else:
                        continue
    return tag_relation_dict
# primary_tags = pd.Series()

# plot_df = pd.DataFrame(columns = list(all_possible_tags))
# # output = sorted(tag_relation_dict.items(), key=lambda item: item[1], reverse=True)[:10]

# for i in tag_relation_dict.keys():
#     temp_tag = pd.Series([i])
#     primary_tags = primary_tags.append(temp_tag, ignore_index=True)
#     # j = dict(sorted(tag_relation_dict.items(), key=lambda item: item[1], reverse=True)[:10])
#     j = tag_relation_dict[i]
#     plot_df = plot_df.append(pd.Series(0, index=plot_df.columns), ignore_index=True)
#     for prim_tag in j.keys():
#             plot_df.at[plot_df.index[-1], prim_tag] = j[prim_tag]
#             plot_df = plot_df.copy()
# names = []
# values = []
# for i in range(len(output)):
#     names.append(output[i][0])
#     values.append(output[i][1])

# plt.barh(names, values)
# plt.show()

# data_csv = plot_df.to_csv()
# f = open('tag_data.csv', 'w')
# f.write(data_csv)
# f.close


if __name__=='__main__':
    df = pd.read_csv('sof_questions.csv')
    all_possible_tags = set()
    df['tags2'] = df['tags'].apply(lambda x: [i for i in x.split('|')])
    tag_relation_dict = tag_dict(main_tags,df['tags'])

    with open('top_tags.pkl', 'wb') as handle:
        pickle.dump(tag_relation_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)