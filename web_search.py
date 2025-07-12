import requests
import time

from bs4 import BeautifulSoup
from scholarly import scholarly


def search(query, num_results: int = 5):
    """
    Function to search Google Scholar using a simple keyword query.

    Parameters:
    query (str): The search query (e.g., paper title or author).
    num_results (int): The number of results to retrieve.

    Returns:
    list: A list of dictionaries containing search results.
    """
    search_url = f"https://scholar.google.com/scholar?q={query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    count = 0

    for item in soup.find_all("div", class_="gs_ri"):
        if count >= num_results:
            break

        title_tag = item.find("h3", class_="gs_rt")
        title = title_tag.get_text() if title_tag else "No title available"

        link = (
            title_tag.find("a")["href"]
            if title_tag and title_tag.find("a")
            else "No Link available"
        )

        authors_tags = item.find("div", class_="gs_a")
        authors = authors_tags.get_text() if authors_tags else "No authors available"

        abstract_tag = item.find("div", class_="gs_rs")
        abstract = abstract_tag.get_text() if abstract_tag else "No abstract available"

        result_data = {
            "Title": title,
            "Authors": authors,
            "Abstract": abstract,
            "URL": link,
        }

        results.append(result_data)
        count += 1
    return results


def advanced_search(query, author: None, year_range=None, num_results=5):
    """
    Function to search Google Scholar using advanced search filters (e.g., author, year range).

    Parameters:
        query (str): The search query (e.g., paper title or topic).
        author (str): The author's name to filter the results (default is None).
        year_range (tuple): A tuple (start_year, end_year) to filter the results by publication year (default is None).
        num_results (int): The number of results to retrieve.

    Returns:
        list: A list of dictionaries containing search results.
    """
    search_url = "https://scholar.google.com/scholar?"

    search_params = {"q": query.replace(" ", "+")}
    if author:
        search_params["as_auth"] = author
    if year_range:
        start_year, end_year = year_range
        search_params["as_ylo"] = start_year  # start year
        search_params["as_yhi"] = end_year  # End year

    search_url += "&".join([f"{key}={value}" for key, value in search_params.items()])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    count = 0

    for item in soup.find_all("div", class_="gs_ri"):
        if count >= num_results:
            break

        title_tag = item.find("h3", class_="gs_rt")
        title = title_tag.get_text() if title_tag else "No title available"

        link = (
            title_tag.find("a")["href"]
            if title_tag and title_tag.find("a")
            else "No Link available"
        )

        authors_tags = item.find("div", class_="gs_a")
        authors = authors_tags.get_text() if authors_tags else "No authors available"

        abstract_tag = item.find("div", class_="gs_rs")
        abstract = abstract_tag.get_text() if abstract_tag else "No abstract available"

        result_data = {
            "Title": title,
            "Authors": authors,
            "Abstract": abstract,
            "URL": link,
        }

        results.append(result_data)
        count += 1
    return results




# example usage
if __name__ == '__main__':
    query = 'machine learning'
    results = search(query, num_results=5)
    print(results)
    print('Result for key word search:')
    for result in results:
        print(f"\nTitle: {result['Title']}")
        print(f"Authors: {result['Authors']}")
        print(f"Abstract: {result['Abstract']}")
        print(f"URL: {result['URL']}")
        print("-" * 80)

    advanced_query = 'machine learning'
    advanced_results = advanced_search(advanced_query, author="Ian Goodfellow", year_range=(2010, 2021), num_results=5)
    print("\nResults for advanced search:")
    for result in advanced_results:
        print(f"\nTitle: {result['Title']}")
        print(f"Authors: {result['Authors']}")
        print(f"Abstract: {result['Abstract']}")
        print(f"URL: {result['URL']}")
        print("-" * 80)



    # Retrieve the author's data, fill-in, and print
    search_query = scholarly.search_author('Steven')
    # 4.Retrieve the first result from the iterator
    print(list(search_query))
    first_author_result = list(search_query)
    scholarly.pprint(first_author_result)

    author = scholarly.fill(first_author_result)
    scholarly.pprint(author)