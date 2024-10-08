from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import time
import math
import pandas as pd
from fake_useragent import UserAgent # fake user agent library
from random import choice
from utils.logo import user_input
from utils.review_url import url_maker
import pickle
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ua = UserAgent()
reviews = {'title': [], 'rating': [], 'content': []}

def request_wrapper(url, ua, proxies):
  proxy = choice(proxies)
  print(f'\nRandom Chosen Proxy:\n{proxy}')
  response = requests.get(url, verify=False,headers={'User-Agent': ua},proxies = proxy)
  # checking response
  if (response.status_code != 200):
    raise Exception(response.raise_for_status())

  print("Response fetched successfully \n")
  return response

def page_scrape(url, proxies, cnt):
    global reviews  # Declare reviews as global to modify it
    pg_reviews = {'title': [], 'rating': [], 'content': []}

    print(f'Page URL: {url}')
    user_ag = ua.random
    print(f'User Agent : \n{user_ag}')
    response = request_wrapper(url, user_ag, proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup.prettify(), "=="*600)

    try:
        rvw2 = soup.find_all("div", {"class": ["a-section", "celwidget"], "id": re.compile("^customer_review-")})
    except:
        print ("Not able to scrape page {} (CAPTCHA is not bypassed)".format(url), flush=True)

    if rvw2 != []:
        for i in range(min(10, len(rvw2))):  # Ensure not to exceed the available reviews
            # Title
            title = rvw2[i].find_all("span")[3].get_text()
            reviews['title'].append(title)
            pg_reviews['title'].append(title)

            # Rating
            rating = rvw2[i].find("i", {"data-hook": "review-star-rating"}).string[0]
            reviews['rating'].append(rating)
            pg_reviews['rating'].append(rating)

            # Content
            content = rvw2[i].find("span", {"data-hook": "review-body"}).get_text("\n").strip()
            reviews['content'].append(content)
            pg_reviews['content'].append(content)

        print(pg_reviews, "**"*200)
    
    else:
        cnt += 1
        print("No reviews found for this page.")

    return cnt
    

def get_total_pages(url, proxies):
        
        user_ag = ua.random
        print(f'User Agent : \n{user_ag}')
        response = request_wrapper(url, user_ag, proxies)
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(soup.prettify())
        # Find the div with the specific data-hook
        content = soup.find_all("div", {"data-hook": "cr-filter-info-review-rating-count"})
        if not content:
            print("No review count information found.")
            return 0

        # Extract the text from the div
        text = content[0].get_text(strip=True).split()
        # The first number is total ratings, and the second is reviews with text
        total_reviews = int(text[3].replace(',',''))

        print("Total reviews (all pages): \n{}".format(total_reviews))

        # Assuming 10 reviews per page
        total_pages = math.ceil(total_reviews / 10)

        print(f"total pages: \n{total_pages}")

        return total_pages

def scrape(url):

    print('url :' , url)

    with open("Proxies/gen_proxy", "rb") as fp:
        proxies = pickle.load(fp)
    print(f"Proxies loaded successfully: \n{proxies}")

    total_pages = get_total_pages(url, proxies)

    print(f'Total Pages: \n{total_pages}')
    no_revw_cnt = 0

    for i in range(1, total_pages + 1):
        time.sleep(1)
        if i == 1:
            current_url = url
        else:
            # current_url = url.replace('btm', f'btm_next_{i}') + f'&pageNumber={i}'
            current_url = url + f'?pageNumber={i}'

        no_revw_cnt = page_scrape(current_url, proxies, no_revw_cnt)
        if no_revw_cnt >= 2:
            break

    reviews_df = pd.DataFrame(reviews)
    print(f"Scraped Reviews : \n{reviews_df}")
    addr = 'ScrapedReviews/Review_Data.csv'
    reviews_df.to_csv(addr)
    print(f'Data saved Succesfully to \n{addr}')
    return reviews_df


if __name__ == "__main__":
    url = user_input()
    rev = url_maker(url)
    scrape(rev)


# scrape("https://www.amazon.in/Samsung-Thunder-Storage-Corning-Gorilla/product-reviews/B0D7Z8CJP8/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")