import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def process(tag_trends_python):
    tagsTwo = []
    questions = []
    date = []
    for t in ['questions',"answers","comments"]:
        tt = tag_trends_python[t]
    # rolling
    #     temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].rolling(window=5).mean())
    # ewm
        temp = list(tt.ewm(span=4).mean())
        date.extend(list(tag_trends_python["creation_quarter"]))
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
    new_tag_trends_python["category"] = tagsTwo
    new_tag_trends_python["questions"] = questions
    new_tag_trends_python
    plt.figure(figsize=(25, 8))
    palette = sns.color_palette("colorblind", 3)
    # sns.lineplot(x="time", y="count",hue="action",err_style="bars", ci=68, data=data, palette=palette)
    ax = sns.lineplot(x=new_tag_trends_python['creation_quarter'].astype(str), y='questions', hue='category', data=new_tag_trends_python, palette=palette, lw=5)
    plt.xlabel('Quarter')
    plt.ylabel('Value')
    plt.title('Quarterly Aggregated Statistics')
    ax.tick_params(axis='x', labelrotation=90)
    ax.tick_params(axis='x', which='major', labelsize=9)
    ax.tick_params(axis='y', which='major', labelsize=9)