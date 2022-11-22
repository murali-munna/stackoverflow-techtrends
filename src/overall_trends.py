import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def overall_trends(path):
    """
    This function takes in a path to a csv file and returns a line plot of the quarterly aggregated
    statistics of the questions, answers, and comments
    
    Args:
      path: the path to the csv file
    """
    
    df1 = pd.read_csv(path)
    
    overall_trends = df1.groupby('creation_quarter').agg(
    questions=pd.NamedAgg(column='id', aggfunc='count'), 
    answers=pd.NamedAgg(column='answer_count', aggfunc='sum'),
    comments=pd.NamedAgg(column='comment_count', aggfunc='sum'),
    score=pd.NamedAgg(column='score', aggfunc='sum'),
    views=pd.NamedAgg(column='view_count', aggfunc='sum'),
    ).reset_index()

    plt.figure(figsize=(20, 8))
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['questions'], label='Questions', linewidth=2)
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['answers'], label='Answers', linewidth=2)
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['comments'], label='Comments', linewidth=2)
    plt.xlabel('Quarter')
    plt.ylabel('Value')
    plt.title('Quarterly Aggregated Statistics')
    ax.tick_params(axis='x', labelrotation=90)

    plt.savefig(os.path.join('/'.join(path.split('/')[:-1]), 'overall_stats_trend.png'))


if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions_filtered.csv'
    
    overall_trends(path)