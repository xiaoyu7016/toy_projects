import os 
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PIL
from PIL import Image

comments = pd.read_csv("../data/clean_comments.txt",sep="|",index_col=0)
comments.columns = ['raw']

names = ['maki','kokichi','rantaro','ryoma','gonta','kaito','kibo','himiko','kaede', 'shuichi','miu','tsumugi','korekiyo','kirumi','tenko','angie']
comments['word_list'] = comments['raw'].map(lambda x: re.split('[^a-z]',str(x).lower()))
for name in names:
    comments[name] = comments['word_list'].map(lambda x: int(name in x))

ranking = comments[names].sum().sort_values(ascending=False)

def resize_keep_ratio(pic_path, desired_width):
    img = Image.open(pic_path)
    
    # Keep the ratio
    ratio = img.size[1]/img.size[0]
    desired_height = int(desired_width * ratio)
    
    # Resize
    thumbnail = img.resize((desired_width, desired_height), Image.ANTIALIAS)
    
    # Change to numpy array
    # figimage takes only float array in range 0-1 instead of 0-255
    img_array = np.array(thumbnail).astype(float) / 255
    return thumbnail

  


# Plot
bar_widths = 0.9
ind = np.arange(len(ranking))
ticks = ind+bar_widths/2
names = list(ranking.index)

fig, ax = plt.subplots(figsize=(20,8))

rects = ax.bar(ind+0.5,ranking.values,bar_widths,color='black')

# Format Axes
ax.set_xlim([-0,16])
ax.set_xticks(ticks)
ax.set_xticklabels([name.title() for name in names])
ax.set_ylim([0,60])
ax.set_yticks([])

# change bar width from coordinate system to display system
img_size = ax.transData.transform((bar_widths,0)) - ax.transData.transform((0,0)) 

# Read in images here since we now know the target size of resizing
imgs = {}
for root,_,files in os.walk("../images/"):
    for img in files:
        img_name = re.sub("\.png","",img)
        img_path = os.path.join(root,img)
        imgs[img_name] = resize_keep_ratio(img_path,int(img_size[0]))  

# Add images on above the bar
for i,img in enumerate(imgs):
    loc = ax.transData.transform((ind[i],ranking.values[i]))
    fig.figimage(imgs[names[i]], loc[0], loc[1], zorder=1)

for i,rect in enumerate(rects):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., 0.95 * height, ranking.values[i],color='white',ha='center',size=12, va='top')

plt.title("# Mentions in 165 Steam Comments",size=20,loc='left')
fig.savefig("../output/Mention.png")