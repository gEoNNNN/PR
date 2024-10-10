import requests
from bs4 import BeautifulSoup

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

        # Extract the product link (assuming it's in an 'a' tag inside the product item)
        link_tag = product.find('a', href=True)
        link = link_tag['href'] if link_tag else "No link found"
        # Construct the full link if it's a relative path
        full_link = f"https://bomba.md{link}" if link.startswith('/') else link

        print(f"Product Name: {name}")
        print(f"Price: {price}")
        print(f"Link: {full_link}")
        print("-" * 40)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
