import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def get_overall_trend_data(path):
    """
    Gropus the dataframe by the creation quarter, and then aggregates the data 
    by questions count, summing the number of answers, comments, score, and views
    
    Args:
      path: the path to the CSV file
    
    Returns:
      A dataframe with the following columns:
    creation_quarter, questions, answers, comments, score, views
    """
    df = pd.read_csv(path)
    
    overall_trends = df.groupby('creation_quarter').agg(
        questions=pd.NamedAgg(column='id', aggfunc='count'), 
        answers=pd.NamedAgg(column='answer_count', aggfunc='sum'),
        comments=pd.NamedAgg(column='comment_count', aggfunc='sum'),
        score=pd.NamedAgg(column='score', aggfunc='sum'),
        views=pd.NamedAgg(column='view_count', aggfunc='sum'),
    ).reset_index()
    
    return overall_trends


def plot_ques_ans_cmts(overall_trends):
    """
    It plots the number of questions, answers, and comments posted on Stack Overflow over time
    
    Args:
      overall_trends: a dataframe with the following columns:
    """
    plt.figure(figsize=(20, 8))
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['questions'], label='Questions', linewidth=2)
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['answers'], label='Answers', linewidth=2)
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['comments'], label='Comments', linewidth=2)
    plt.xlabel('Quarter')
    plt.ylabel('Value')
    plt.title('Quarterly Aggregated Statistics')
    ax.tick_params(axis='x', labelrotation=90)

    plt.savefig(os.path.join('../plots/', 'overall_stats_trend.png'))


def plot_views(overall_trends):
    """
    It takes a dataframe as input, and plots a line graph of the number of views per quarter
    
    Args:
      overall_trends: This is the dataframe that contains the data for the overall trends.
    """

    plt.figure(figsize=(25, 8))
    ax = sns.lineplot(x=overall_trends["creation_quarter"].astype(str), y=overall_trends['views'], label='Question Views', linewidth=2)
    plt.xlabel('Month-Year')
    plt.ylabel('Views')
    plt.title('Question View Count')
    ax.tick_params(axis='x', labelrotation=90)
    ax.tick_params(axis='x', which='major', labelsize=7)

    plt.savefig(os.path.join('../plots/', 'overall_views_trend.png'))
    

if __name__=='__main__':
    
    # Have the GCP BQ downloaded data in data/ folder
    path = '../data/sof_questions_filtered.csv'
    
    overall_trends = get_overall_trend_data(path)
    
    # Plot Metrics Trend
    plot_ques_ans_cmts(overall_trends)
    
    plot_views(overall_trends)
    
    