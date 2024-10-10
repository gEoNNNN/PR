import requests
from bs4 import BeautifulSoup
import re

def extract_and_convert_to_int(text):
    # Use regex to find the part before "lei"
    match = re.search(r'(\d+[\s\d]*)\s*lei', text)
    if match:
        # Remove both regular spaces and non-breaking spaces, then convert to an integer
        cleaned_number = match.group(1).replace(" ", "").replace("\xa0", "")
        return int(cleaned_number)
    return None

def add_space_before_uppercase(text):
    # Use regex to add a space before each uppercase letter only if it's not preceded or followed by another uppercase letter.
    return re.sub(r'(?<![A-Z])([A-Z])(?![A-Z])', r' \1', text).strip()

# URL of the website you want to scrape
url = "https://bomba.md/ro/category/telefoane-mobile-686094/apple/"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# Send a GET request to the website with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product items within the 'rht__products' div
    products = soup.find_all('div', class_='product__item')

    # Loop through each product item to extract the name, price, and link
    for product in products:
        # Extract the product name
        name_tag = product.find('div', class_='product__name')
        name = name_tag.get_text(strip=True) if name_tag else "No name found"

        # Extract the product price
        price_tag = product.find('div', class_='product__price')
        price = price_tag.get_text(strip=True) if price_tag else "No price found"
        price_int = extract_and_convert_to_int(price)

        # Extract the product link (assuming it's in an 'a' tag inside the product item)
        link_tag = product.find('a', href=True)
        link = link_tag['href'] if link_tag else "No link found"
        # Construct the full link if it's a relative path
        full_link = f"https://bomba.md{link}" if link.startswith('/') else link

        print(f"Product Name: {name}")
        print(f"Price: {price_int}")
        print(f"Link: {full_link}")

        # Make a request to the product's detail page to scrape the 'product-bottom' section
        if link != "No link found":
            product_response = requests.get(full_link, headers=headers)
            if product_response.status_code == 200:
                product_soup = BeautifulSoup(product_response.content, 'html.parser')
                # Find the 'product-bottom' section and print its content
                product_bottom = product_soup.find('section', class_='product-bottom')
                if product_bottom:
                    # Extract the text from product_bottom
                    product_bottom_text = product_bottom.get_text(strip=True)
                    # Add space before uppercase letters
                    spaced_product_bottom = add_space_before_uppercase(product_bottom_text)
                    print("Product-Bottom Section:")
                    print(spaced_product_bottom)
                else:
                    print("No 'product-bottom' section found.")
            else:
                print(f"Failed to retrieve the product page. Status code: {product_response.status_code}")

        print("-" * 40)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")