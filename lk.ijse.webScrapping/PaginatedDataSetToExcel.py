from bs4 import BeautifulSoup
import requests
import pandas as pd

# Base URL to scrape (with page number placeholder)
base_url = "https://www.patpat.lk/property/filter/land?page={}"

# Lists to hold the scraped data
landTitles = []
landSizes = []
locations = []
createDates = []
totalPrices = []
monthlyPayments = []
imageUrls = []


# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the div elements containing land listings
        land_items = soup.find_all('div', class_='result-item')

        # Check if the page contains only two default items (likely no real listings)
        if len(land_items) == 2:
            print(f"Stopping: only two default divs found on page {url}")
            return False

        # Iterate over each listing
        for item in land_items:
            # Extracting the land title
            land_title = item.find("h4", class_="result-title")
            land_title = land_title.text.strip() if land_title else "N/A"

            # Extracting the land size
            land_size = item.find('span', class_='d-block w-50 float-left')
            # Splits the text into a list. Remove extra whitespace and join text with a single space.
            land_size_text = ' '.join(land_size.text.split()).strip() if land_size else "N/A"

            # Extracting location
            location = item.select_one('p.result-agent > span.d-block')
            if location:
                # Filters out only text nodes (excluding nested tags) and joins them into a single string.
                location_text = ''.join(node for node in location.contents if isinstance(node, str)).strip()
            else:
                location_text = "N/A"

            # Extracting create date
            create_date = item.select_one('.course-info p.result-agent + p span.d-block')
            create_date = create_date.text.strip() if create_date else "N/A"

            # Extracting total price
            total_price = item.select_one('.result-payments.price span.money')
            total_price = total_price.text.strip() if total_price else "N/A"

            # Extracting monthly payment
            monthly_payment = item.select_one('.result-payments.price.border-top-0 span.money')
            monthly_payment = monthly_payment.text.strip() if monthly_payment else "N/A"

            # Extracting image URL
            image = item.find('img')
            image_url = image['src'] if image else "N/A"

            # Append data to respective lists
            landTitles.append(land_title)
            landSizes.append(land_size_text)
            locations.append(location_text)
            createDates.append(create_date)
            totalPrices.append(total_price)
            monthlyPayments.append(monthly_payment)
            imageUrls.append(image_url)

        return True
    else:
        print(f"Failed to retrieve page: {url}")
        return False


# Main function to start scraping
def main():
    # Loop through all the available pages
    page_no = 1
    while True:
        page_url = base_url.format(page_no)
        print(f"Scraping page: {page_no}")

        if not scrape_page(page_url):
            break  # Stop the loop if the scrape_page function returns False (only two default divs)

        page_no += 1

    # Create a DataFrame from the scraped data
    df = pd.DataFrame({
        'Title': landTitles,
        'Land Size': landSizes,
        'Location': locations,
        'Create Date': createDates,
        'Total Price': totalPrices,
        'Monthly Payment': monthlyPayments,
        'Image URL': imageUrls
    })

    # Export the DataFrame to an Excel file
    df.to_excel('land_properties.xlsx', index=False)
    print("Data successfully written to land_properties.xlsx")


# Entry point of the script
if __name__ == "__main__":
    main()
