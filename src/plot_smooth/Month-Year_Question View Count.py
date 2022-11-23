import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def process(tag_trends_python):
    tagsTwo = []
    questions = []
    date = []
    for t in ['views']:
        tt = tag_trends_python[t]
    # rolling
    #     temp = list(tag_trends_python[tag_trends_python["tags2"] == t]['questions'].rolling(window=5).mean())
    # ewm
        temp = list(tt.ewm(span=5).mean())
        date.extend(list(tag_trends_python["creation_month_yr"]))
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
    plt.figure(figsize=(33, 10))
    palette = sns.color_palette("dark")
    # palette = sns.xkcd_palette(["windows blue", "amber", "greyish", "faded green", "dusty purple", "red", "black"])
    # palette = sns.xkcd_palette(["amber"])
    # sns.palplot(sns.color_palette("dark",11))
    # sns.lineplot(x="time", y="count",hue="action",err_style="bars", ci=68, data=data, palette=palette)
    ax = sns.lineplot(x=new_tag_trends_python['creation_quarter'].astype(str), y='questions', hue='category', data=new_tag_trends_python, palette=palette, lw=5)
    plt.xlabel('Month-Year')
    plt.ylabel('Views')
    plt.title('Question View Count')
    ax.tick_params(axis='x', labelrotation=90)
    ax.tick_params(axis='x', which='major', labelsize=7)