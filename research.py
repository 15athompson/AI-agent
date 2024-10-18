import feedparser
import requests
import urllib.parse  # Import the urllib.parse module

def search_arxiv(query, max_results=5):
    # Encode the query string to be URL-safe
    encoded_query = urllib.parse.quote(query)
    
    # Construct the base URL with the encoded query
    base_url = f'http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results={max_results}'
    
    # Fetch the data from the API
    response = feedparser.parse(base_url)

    papers = []
    for entry in response.entries:
        papers.append({
            'title': entry.title,
            'summary': entry.summary,
            'link': entry.link,
            'published': entry.published,
        })
    
    return papers

def research_papers(query, max_results=5):
    arxiv_papers = search_arxiv(query, max_results)
    # You can add more sources here in the future
    return arxiv_papers
