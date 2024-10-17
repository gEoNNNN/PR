import requests
from bs4 import BeautifulSoup
import re

def menu():
    print("1 :Use an HTML parser to extract the name and price of the products.")
    print("2 :Extract the product link. Scrape the link further and extract one additional piece of data from it")
    print("3 :Before storing the product information in your data models/structures, add two validations to the data.")
    print("4 :Process the list of products using Map/Filter/Reduce functions.Filter the products within a range of prices.")
    option = int(input("Chose an option: "))
    return option
def extract_phone_details(text):
    # Define patterns to match the required details
    phone_pattern = r'iPhone \d{1,2}'
    ram_pattern = r'\d+ GB'
    storage_pattern = r'\d+GB'
    color_pattern = r'Negru|Alb|Albastru|Verde|Roșu|Aur|Argint|Mov|Roz|Gri|Sur|Starlight|Midnight'  # Add more colors as needed

    # Find all occurrences of the patterns
    phone_match = re.search(phone_pattern, text, re.IGNORECASE)
    ram_match = re.search(ram_pattern, text)
    storage_match = re.search(storage_pattern, text)
    color_match = re.search(color_pattern, text, re.IGNORECASE)

    # Extract matched details or set default values
    phone = phone_match.group() if phone_match else 'Unknown Model'
    ram = ram_match.group() if ram_match else 'Unknown RAM'
    storage = storage_match.group() if storage_match else 'Unknown Storage'
    color = color_match.group() if color_match else 'Unknown Color'

    # Return the details as a list
    return [phone, ram, storage, color]
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

def option_one():
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

            print(f"Product Name: {name}")
            print(f"Price: {price}")
            print("-" * 100)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def option_two():
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
            print("-" * 100)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
def option_three():
# URL of the website you want to scrape
    url = "https://bomba.md/ro/category/telefoane-mobile-686094/apple/"
    product_dict = {}
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
        id = 0
        for product in products:
            # Extract the product name
            name_tag = product.find('div', class_='product__name')
            name = name_tag.get_text(strip=True) if name_tag else "No name found"
            livrare = name
            livrare = 'Prin' + livrare.split('Prin', 1)[1]
            name = name.split('Prin')[0]

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
            print(f"Order time: {livrare}")
            print(f"Link: {full_link}")
            id += 1
            product_dict[id] = {
                'Name': name,
                'Price': price_int,
                'Order time': livrare,
                'Link': full_link
            }
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
                        product_dict[id]['Specifications'] = spaced_product_bottom
                        print("Product-Bottom Section:")
                        print(spaced_product_bottom)
                    else:
                        print("No 'product-bottom' section found.")
                else:
                    print(f"Failed to retrieve the product page. Status code: {product_response.status_code}")

            print("-" * 40)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def option_four():
    # URL of the website you want to scrape
    url = "https://bomba.md/ro/category/telefoane-mobile-686094/apple/"
    product_dict = {}
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
        id = 0
        for product in products:
            # Extract the product name
            name_tag = product.find('div', class_='product__name')
            name = name_tag.get_text(strip=True) if name_tag else "No name found"
            livrare = name
            livrare = 'Prin' + livrare.split('Prin', 1)[1]
            name = name.split('Prin')[0]

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
            print(f"Order time: {livrare}")
            print(f"Link: {full_link}")
            product_dict[id] = {
                'Name': name,
                'Price': price_int,
                'Order time': livrare,
                'Link': full_link
            }
            id += 1
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
                        product_dict[id]['Specifications'] = spaced_product_bottom
                        print("Product-Bottom Section:")
                        print(spaced_product_bottom)
                    else:
                        print("No 'product-bottom' section found.")
                else:
                    print(f"Failed to retrieve the product page. Status code: {product_response.status_code}")

            print("-" * 40)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

while True:
    option = menu()
    if option == 1:
        option_one()
    elif option == 2:
        option_two()
    elif option == 3:
        option_three()
