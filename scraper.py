from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import time
import math
import pandas as pd
from fake_useragent import UserAgent # fake user agent library
from random import choice
from logo import user_input
from utils.review_url import url_maker

ua = UserAgent()
reviews = {'title': [], 'rating': [], 'content': []}
broken = []


def proxy_generator():
            # URL of the website to scrape
      proxies = []

      url = 'https://sslproxies.org/'  # Replace with the actual URL

      # Make a request to fetch the HTML content
      response = requests.get(url,headers={'User-Agent': ua.random},verify = False)

      print({"Proxies Table fetched Successfully"})

      # Check if the request was successful
      if response.status_code == 200:
          # Parse the HTML content using BeautifulSoup
          soup = BeautifulSoup(response.text, 'html.parser')

          # Find the div containing the table (based on class or other attributes)
          table_div = soup.find('div', class_='table-responsive fpl-list')

          if table_div:
              # Find all rows in the table body
              rows = table_div.find_all('tr')[1:]  # Skipping the header row

              # Extract IP addresses and ports
              ip_port_list = []
              for row in rows:
                  cells = row.find_all('td')
                  ip_address = cells[0].get_text(strip=True)
                  port = cells[1].get_text(strip=True)
                  ip_port_list.append((ip_address, port))

              # Print the results
              for ip, port in ip_port_list:
                proxies.append({'http':'http://'+ip+':'+port})

              return proxies

          else:
              print("Could not find the table div.")
      else:
          print(f"Failed to fetch the webpage. Status code: {response.status_code}")

def request_wrapper(url, ua, proxies):
  proxy = choice(proxies)
  print(f'\nRandom Chosen Proxy:\n{proxy}')
  response = requests.get(url, verify=False,headers={'User-Agent': ua},proxies = proxy)
  # checking response
  if (response.status_code != 200):
    raise Exception(response.raise_for_status())

  print("Response fetched successfully")
  return response

def page_scrape(url, proxies):
    global reviews  # Declare reviews as global to modify it
    global broken

    print(f'Page URL: {url}')
    user_ag = ua.random
    print(f'User Agent : \n{user_ag}')
    response = request_wrapper(url, user_ag, proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        rvw2 = soup.find_all("div", {"class": ["a-section", "celwidget"], "id": re.compile("^customer_review-")})
    except:
        broken.append(url)
        print ("Not able to scrape page {} (CAPTCHA is not bypassed)".format(url), flush=True)

    for i in range(min(10, len(rvw2))):  # Ensure not to exceed the available reviews
        # Title
        title = rvw2[i].find_all("span")[3].get_text()
        reviews['title'].append(title)

        # Rating
        rating = rvw2[i].find("i", {"data-hook": "review-star-rating"}).string[0]
        reviews['rating'].append(rating)

        # Content
        content = rvw2[i].find("span", {"data-hook": "review-body"}).get_text("\n").strip()
        reviews['content'].append(content)

    print(reviews)
    

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

        print("Total reviews (all pages): {}".format(total_reviews))

        # Assuming 10 reviews per page
        total_pages = math.ceil(total_reviews / 10)

        print(f"total pages: {total_pages}")

        return total_pages

def scrape(url):

    print('url :' , url)
    proxies = proxy_generator()
    print(f"Proxies generated successfully:\n{proxies}")

    total_pages = get_total_pages(url, proxies)

    print(f'Total Pages: {total_pages}')

    for i in range(1, total_pages + 1):
        time.sleep(1)
        if i == 1:
            current_url = url
        else:
            # current_url = url.replace('btm', f'btm_next_{i}') + f'&pageNumber={i}'
            current_url = url + f'?pageNumber={i}'

        page_scrape(current_url, proxies)

    # Convert the reviews dictionary to a pandas DataFrame
    print(f'Broken links : {broken}')
    reviews_df = pd.DataFrame(reviews)
    print(reviews_df)
    addr = 'Review_Data_1.csv'
    reviews_df.to_csv(addr)
    print(f'Data saved Succesfully to \n{addr}')


if __name__ == "__main__":
    url = user_input()
    rev = url_maker(url)
    scrape(rev)


# scrape("https://www.amazon.in/Samsung-Thunder-Storage-Corning-Gorilla/product-reviews/B0D7Z8CJP8/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")