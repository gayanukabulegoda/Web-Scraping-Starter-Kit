# import required libs
import requests
from bs4 import BeautifulSoup


def main():
    # url of the page to scrap
    url = 'https://example.com/'

    # send a get request to the server
    response = requests.get(url)

    # print scrap data
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup.prettify()) # prints the whole html content
        # print(soup.title) prints # only the title tag
        # print(soup.title.string) # prints the title tag content
        # print(soup.h1.string) # prints the h1 tag content
        # print(soup.a.string) #prints the a tag content
        # print(soup.p) # prints the first paragraph tag
        # print(soup.p.text) # prints the text inside the first paragraph tag
        # for paragraph in soup.find_all('p'): # prints all the paragraph tags
        #     print(paragraph.text)

        tags = soup.find_all(['h1', "p"])
        for tag in tags:
            print(tag.text.strip())

    else:
        print('Error Occurred')


# Entry point of the script
if __name__ == "__main__":
    main()
