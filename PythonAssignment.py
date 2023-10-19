import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product details from an individual product page
def scrape_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_details = []

    # Extract additional product information (description, ASIN, product description, manufacturer)
    product_description = soup.find('div', {'id': 'productDescription'})
    asin = soup.find('th', text='ASIN')
    manufacturer = soup.find('th', text='Manufacturer')

    product_details.extend([
        product_description.get_text() if product_description else '',
        asin.find_next('td').get_text() if asin else '',
        manufacturer.find_next('td').get_text() if manufacturer else ''
    ])

    return product_details

# Main function to scrape both product listings and details
def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C6104MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=se_pg_"
    
    num_pages_to_scrape = 20
    product_data = []

    for page in range(1, num_pages_to_scrape + 1):
        page_url = base_url + str(page)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product URLs
        product_urls = [a['href'] for a in soup.select('div.s-result-item a.a-link-normal')]
        
        for product_url in product_urls:
            product_data.append(scrape_product_details(product_url))
        
    # Write data to a CSV file
    with open('amazon_product_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Description', 'ASIN', 'Product Description', 'Manufacturer'])
        csv_writer.writerows(product_data)

if __name__ == '__main__':
    main()
