import pickle
import requests
from bs4 import BeautifulSoup


def getProxies(file_addr):
    # URL of the website to scrape
    
    proxies = []
    url = 'https://sslproxies.org/'  # Replace with the actual URL

    # Make a request to fetch the HTML content
    response = requests.get(url)
    print(response)

    # Check if the request was successful
    if response.status_code == 200:
        print("akshat")
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

            with open(file_addr, "wb") as fp:   #Pickling
                pickle.dump(proxies, fp)

            #with open(file_addr, "rb") as fp:   # Unpickling
            #   proxies = pickle.load(fp)
            #return proxies

        else:
            print("Could not find the table div.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")


if __name__ == "__main__":
    filename = input("Enter file name to save proxies: ")
    getProxies(filename)


 

