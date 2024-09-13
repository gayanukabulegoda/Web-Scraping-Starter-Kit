from bs4 import BeautifulSoup
import requests
import os


def main():
    url = "https://www.geeksforgeeks.org/fundamentals-of-algorithms/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Create a directory to store images
        if not os.path.exists('images'):
            os.makedirs('images')

            # Find all images and download them
            img = soup.find('img', {'alt': "What is Algorithm?"})
            img_url = img['src']
            img_name = img_url.split('/')[-1]
            # This splits the image URL (img_url) into a list of strings at each /.
            # [-1]: This accesses the last element of the list, which is the actual image file name.

            with open(f'images/{img_name}',
                      'wb') as file:  # f-string (formatted string literal), used to create a file path
                img_response = requests.get(img_url)
                file.write(img_response.content)

        print("Image downloaded successfully")


if __name__ == "__main__":
    main()
