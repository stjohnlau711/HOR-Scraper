import requests
from bs4 import BeautifulSoup as soup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"

response = requests.get(url)

page_soup = soup(response.text, "html.parser")

table = page_soup.find("table", {"id": "votingmembers"})
table_body = table.body

representatives = table.tbody.findAll("tr") # row of representatives (array)
header = representatives[0] # headers

headings = [] # (columns)

for th in header.findAll("th"):
	headings.append(th.text.strip())

df = pd.DataFrame(columns=headings)

for i in range(1, len(representatives)):
	tds = representatives[i].findAll('td')

	values = [td.text.replace('\n', '').replace('\xa0', ' ') for td in tds]
	values.remove('')

	df = df.append(pd.Series(values, index=headings), ignore_index=True)

	df.to_csv('FILEPATH/HoRMembers.csv',index=False)

