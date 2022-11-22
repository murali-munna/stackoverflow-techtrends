import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def get_tag_trends_data(path):
    """
    Explodes the tags column into a new row for each tag, groups the data by quarter
    and tag, and then pivots the dataframe so that each tag is a column
    
    Args:
      path: the path to the data file
    
    Returns:
      A dataframe with the number of questions per quarter per tag.
    """
    df = pd.read_csv(path)
    tags_df = df[['creation_quarter', 'tags2', 'answer_count', 'comment_count', 'view_count', 'score']]
    tags_df = tags_df.explode('tags_filtered')
    
    tag_trends = tags_df.groupby(['creation_quarter','tags_filtered']).agg(
        questions=pd.NamedAgg(column='tags2', aggfunc='count'), 
    ).reset_index()
    
    tag_trends_wide = tag_trends.pivot(index='creation_quarter', columns='tags_filtered', values='questions')
    
    return tag_trends_wide
 
    
def plot_tag_trends(tag_trends):
    """
    Plots a stacked bar chart of the number of questions asked for each tag in each quarter
    
    Args:
      tag_trends: a dataframe with the following columns:
    """
    
    f=  plt.figure(figsize=(20, 8))
    ax = tag_trends.plot(kind='bar', stacked=True, ax=f.gca())
    plt.xlabel('Quarter')
    plt.ylabel('Questions')
    plt.title('Questions by different tags')
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), ncol=2)
    ax.tick_params(axis='x', labelrotation=90)
    
    plt.savefig(os.path.join('../plots/', 'trend_by_tags.png'))


if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions_filtered.csv'
    
    tag_trends = get_tag_trends_data(path)
    
    # Plot Tags Trend
    plot_tag_trends(tag_trends)