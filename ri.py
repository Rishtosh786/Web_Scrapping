import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob

url = "https://www.amazon.in/New-Apple-iPhone-Mini-128GB/product-reviews/B08L5VN68Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
code = requests.get(url)

soup = BeautifulSoup(code.content,'html.parser')


names = soup.select('span.a-profile-name')[2:12]
print(names,"\n\n")
print("____________________________________________________________________________________________________________________________________")

titles = soup.select('a.review-title span')[2:13]
print(titles,"\n\n")
print("____________________________________________________________________________________________________________________________________")

dates = soup.select('span.review-date')[2:13]
print(dates,"\n\n")
print("____________________________________________________________________________________________________________________________________")

stars = soup.select('i.review-rating span.a-icon-alt')[2:13]
print(stars,"\n\n")
print("____________________________________________________________________________________________________________________________________")

reviews = soup.select('span.review-text-content span')
print(reviews,"\n\n")

cust_name = []
rev_date = []
ratings = []
rev_title = []
rev_content = []
for i in range(len(names)):
  cust_name.append(names[i].get_text())
  rev_date.append(dates[i].get_text().replace("Reviewed in India","")) 
  ratings.append(stars[i].get_text())
  rev_title.append(titles[i].get_text())
  rev_content.append(reviews[i].get_text().strip("\n "))


print("\n\n")
print("____________________________________________________________________________________________________________________________________\n\n")
result = 0
for rate in rev_title:
    analysis = TextBlob(rate)
    positive = analysis.sentiment.polarity > 0
    neutral = analysis.sentiment.polarity == 0
    negative = analysis.sentiment.polarity < 0

    if positive > negative:
        result+=1
    elif positive < negative:
        result-=1
    else:
        result=result
if result>0:
    print("The overall sentiment for this product is POSITIVE\n")
elif result<0:
    print("The overall sentiment for this product is NEGATIVE\n")
else:
    print("The overall sentiment for this product is NEUTRAL\n")

print("____________________________________________________________________________________________________________________________________\n\n")
df = pd.DataFrame()
df['Customer Name'] = cust_name
df['Date'] = rev_date
df['Ratings'] = ratings
df['Review Title'] = rev_title
df['Reviews'] = rev_content

print(df,"\n\n")
print("____________________________________________________________________________________________________________________________________")
df.to_csv("amazon.csv")




