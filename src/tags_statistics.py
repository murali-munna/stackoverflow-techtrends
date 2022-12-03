import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def get_tag_stats_data(path):
    """
    It takes a path to a CSV file, reads it in as a dataframe,
    explodes the tags column, groups by the tags, and then aggregates the data by summing the answer
    count, comment count, view count, and score. 
    
    Args:
      path: the path to the csv file
    
    Returns:
      A dataframe with the following columns:
    """
    assert isinstance(path, str)
    assert os.path.exists(path)
    
    df = pd.read_csv(path)
    tags_df = df[['creation_quarter', 'tags_filtered', 'answer_count', 'comment_count', 'view_count', 'score']]
    tags_df = tags_df.explode('tags_filtered')
    
    tag_qa = tags_df.groupby(['tags_filtered']).agg(
        questions=pd.NamedAgg(column='tags_filtered', aggfunc='count'), 
        answers=pd.NamedAgg(column='answer_count', aggfunc='sum'), 
        comments=pd.NamedAgg(column='comment_count', aggfunc='sum'), 
        views=pd.NamedAgg(column='view_count', aggfunc='sum'), 
        scores=pd.NamedAgg(column='score', aggfunc='sum'), 
    ).reset_index().sort_values('questions', ascending=True)
    
    tag_qa['avg_ans'] = tag_qa['answers']/tag_qa['questions']
    tag_qa['avg_comments'] = tag_qa['comments']/tag_qa['questions']
    tag_qa['avg_views'] = tag_qa['views']/tag_qa['questions']
    tag_qa['avg_score'] = tag_qa['scores']/tag_qa['questions']
    
    return tag_qa
 
    
def plot_tag_trends(tag_qa):
    """
    It plots the top 20 tags by questions, average answers, average views, and average score
    
    Args:
      tag_trends: a dataframe with the following columns:
    """
    assert isinstance(tag_qa, pd.DataFrame)
    assert set(['questions_log', 'avg_ans', 'avg_views', 'avg_score', 'tags_filtered']).issubset(tag_qa.columns)
    
    fig, axes = plt.subplots(1, 4, figsize=[20, 15])

    g1 = sns.barplot(x='questions_log', y='tags_filtered', data=tag_qa, ax=axes[0])
    g1.set_title('Questions (Log Scale)', fontsize=16)
    g1.set_ylabel('Tags', fontsize=14)
    g1.set(xlabel=None)

    g2 = sns.barplot(x='avg_ans', y='tags_filtered', data=tag_qa, ax=axes[1])
    g2.set(yticklabels=[])
    g2.set_title('Avg. Answers', fontsize=16)
    g2.set(ylabel=None)
    g2.set(xlabel=None)

    g3 = sns.barplot(x='avg_views', y='tags_filtered', data=tag_qa, ax=axes[2])
    g3.set(yticklabels=[])
    g3.set_title('Avg. Views', fontsize=16)
    g3.set(ylabel=None)
    g3.set(xlabel=None)

    g4 = sns.barplot(x='avg_score', y='tags_filtered', data=tag_qa, ax=axes[3])
    g4.set(yticklabels=[])
    g4.set_title('Avg. Score', fontsize=16)
    g4.set(ylabel=None)
    g4.set(xlabel=None)
    
    plt.savefig(os.path.join('../plots/', 'tags_statistics.png'))


if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions_filtered.csv'
    
    tag_qa = get_tag_stats_data(path)
    
    # Plot Tags Trend
    plot_tag_trends(tag_qa)