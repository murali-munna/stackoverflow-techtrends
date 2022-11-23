import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def process(tag_trends_python):
    a_tags = list(tag_trends_python["tags2"])
    set(a_tags)
    
#     a_tags.remove('pandas')
    tagsTwo = []
    questions = []
    date = []
    for t in a_tags:
        if t == "pandas":
            continue
        tt = tag_trends_python[tag_trends_python["tags2"] == t]
    # rolling
    #     temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].rolling(window=5).mean())
    # ewm
        temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].ewm(span=7).mean())
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
    plt.xlabel('Quarter')
    plt.ylabel('Questions')
    plt.title('DS/ML Fields')
    ax.tick_params(axis='x', labelrotation=90)
