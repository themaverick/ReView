from utils.url_parser import extract_product_info

def url_maker(url):
    product_name , asin = extract_product_info(url)
    review_url  = f'https://www.amazon.in/{product_name}/product-reviews/{asin}/'
    return review_url