from urllib.parse import urlparse, parse_qs

def extract_product_info(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Split the path to get the product name and ASIN
    path_parts = parsed_url.path.split('/')
    
    # Extract the product name and ASIN
    product_name = path_parts[1]
    asin = path_parts[3]
    
    return product_name, asin

# print(extract_product_info('https://www.amazon.in/VAS-COLLECTIONS%C2%AE-Woolen-Blanket-Blankets/dp/B08R68MDBR/ref=cm_cr_arp_d_product_top?ie=UTF8'))


