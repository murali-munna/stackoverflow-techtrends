import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings("ignore")

def process(tag_trends_python, topic:str, xlabel:str, ylabel:str, span = 5):
    """
    Smoothens the line plot across each category for better visualization and trend study
    
    Args:
        tag_trends_python (_type_): DataFrame of questions trend across each category
        topic (str): _description_ 
        xlabel (str): _description_
        ylabel (str): _description_
        span (int, optional): _description_. Defaults to 5.
    """
    assert isinstance(tag_trends_python, pd.DataFrame)
    assert isinstance(topic, str)
    assert isinstance(xlabel, str)
    assert isinstance(ylabel, str)
    assert isinstance(span, int)
    assert set(['tags2', 'questions', 'creation_quarter']).issubset(tag_trends_python.columns)
    
    a_tags = list(tag_trends_python["tags2"])
    tagsTwo = []
    questions = []
    date = []
    for t in a_tags:
        tt = tag_trends_python[tag_trends_python["tags2"] == t]

    # rolling
    #     temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].rolling(window=5).mean())

    # ewm
        temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].ewm(span = span).mean())
        date.extend(list(tt["creation_quarter"]))
        length = len(temp)
        if len(temp) >= 4:
            temp[0] = temp[4]/6
            temp[1] = temp[4]/4
            temp[2] = temp[4]/3
            temp[2] = temp[4]/2
        tagsTwo.extend(length*[t])
        questions.extend(temp)
    new_tag_trends_python = pd.DataFrame()
    new_tag_trends_python["creation_quarter"] = date
    new_tag_trends_python["tags2"] = tagsTwo
    new_tag_trends_python["questions"] = questions

    palette = sns.color_palette("colorblind")
    plt.figure(figsize=(12, 8))
    ax = sns.lineplot(x=new_tag_trends_python['creation_quarter'].astype(str), y='questions', hue='tags2', data=new_tag_trends_python,palette = palette,lw=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(topic)
    ax.tick_params(axis='x', labelrotation=90)
    
    plt.savefig(os.path.join('../plots/', 'python_pkg_trend.png'))