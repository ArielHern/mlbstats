import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import matplotlib.pyplot as plt


# fetches the webpage from the url
r = requests.get("https://www.baseball-reference.com/players/b/bondsba01.shtml")

# parse the html with BeautifulSoup
page_soup = soup(r.text, 'html.parser')

# get the table headers from html
header = page_soup.find_all('thead')


# [:-1] eliminates awards
columns = [headers.get_text() for headers in header[0].find_all('th')][:-1]

# dataframe that will be use for the graph
df_bonds = pd.DataFrame(columns=columns)

# get the needed data
results = page_soup.find_all('tr', attrs={'class': 'full'})

# loop to get all the results from the site
for year in results:

    # [:-1] eliminates awards
    contents = [result.get_text() for result in year][:-1]
    df_tem = pd.DataFrame(contents).transpose()
    df_tem.columns = columns
    df_bonds = pd.concat([df_bonds, df_tem], sort=False)

# make the year on which he played the index
df_bonds.set_index('Year', inplace=True)

years = list(map(str, range(1986, 2007)))

# change the HR to int - to be use as the Y-axis
df_bonds['HR'] = df_bonds['HR'].astype('int')

# plot HR by years
plt.style.use('ggplot')
ax = df_bonds.plot(kind='bar', alpha=0.35, figsize=(20, 10))
ax.set_title('Barry Bonds Home Runs By Years')
ax.set_ylabel('Number of Home Runs')
ax.set_xlabel('Year')
# Save the fig
plt.savefig('hr_track.png')


plt.show()
