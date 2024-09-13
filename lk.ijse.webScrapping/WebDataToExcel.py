import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    # Define the URL
    url = "https://www.geeksforgeeks.org/fundamentals-of-algorithms/"

    # Get the response from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Lists to store headings and their related content
        headings = []
        content = []

        # Find all headings (h2) and paragraphs (p) and store them
        for heading in soup.find_all('h2'):
            heading_text = heading.text.strip()
            # Get the next paragraph after each heading
            next_paragraph = heading.find_next('p')

            # Store heading and content
            headings.append(heading_text)
            if next_paragraph:
                content.append(next_paragraph.text.strip())
            else:
                content.append("")  # In case there's no paragraph after the heading

        # Create a DataFrame from the lists
        df = pd.DataFrame({'Heading': headings, 'Content': content})

        # Write the DataFrame to an Excel file
        df.to_excel("web_data_to_excel.xlsx", sheet_name="Headings and Content", index=False)

        print("Data successfully written to 'web_data_to_excel.xlsx'")

    else:
        print('Error Occurred')


if __name__ == "__main__":
    main()
