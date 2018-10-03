import json
from urllib.parse import urlparse

# import the requests library to help use query a website
import requests

# import the BeautifulSoup library to help us parse the websites
from bs4 import BeautifulSoup


# The function to query a website
def scrap_website(url):

    # query the web page
    page = requests.get(url)

    # parse the fetched html content using a html parser
    # since our page content is going to be in html format
    soup = BeautifulSoup(page.content, 'html.parser')

    # You can also view the source on the terminal by uncommenting the following line
    # print(soup.prettify)

    # find the repositories container div
    main_content = soup.find('div', {'id': 'user-repositories-list'})

    # Extract the list of repositories
    list_of_repos = main_content.findAll('li')

    # put the results of the scraping in a list of dictionaries
    results = []

    # Extract the details for each repo
    for repo in list_of_repos:
        # create a new repository details dictionary
        repository = {}

        # add the repository name, note that we strip a leading newline and
        # leading and trailing whitespaces
        repository["name"] = repo.a.string.strip()

        # Extract the base url for the url passed into the function
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
        # generate the repository link
        repository["link"] = "{0}{1}".format(base_url, repo.a.get('href'))

        # Check if there is a repo description and add it to our dictionary
        if repo.p and repo.p.string:
            repository["description"] = repo.p.string.strip()

        # if no description is found
        else:
            repository["description"] = "No description available for this repository."

        # add the programming language of the repository
        programming_language = soup.find(attrs={"itemprop": "programmingLanguage"}).string.strip()
        repository["programming_language"] = programming_language
        
        # Add the repository to our results
        results.append(repository)

    # return our list of repositories as the output of our function
    return results


print(json.dumps(scrap_website("https://github.com/gvanrossum?tab=repositories"), indent=4))

parsed_uri = urlparse("https://github.com/gvanrossum?tab=repositories")
result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
print(result)
