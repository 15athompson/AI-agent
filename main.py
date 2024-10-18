import requests
import feedparser
from Bio import Entrez
import urllib.parse  # Import the urllib.parse module
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to generate a summary (Dummy for now, replace with real summarization later)
def generate_summary(text):
    return f"Summary of: {text[:200]}..."  # Just return a truncated version for now

# Function to generate a BibTeX citation (for arXiv papers)
#def generate_bibtex(paper):
 #   return f"@article{{{paper['id']}},\n  title={{ {paper['title']} }},\n  author={{ {', '.join(paper['authors'])} }},\n  journal={{arXiv}},\n  year={{ {paper['published'][:4]} }}\n}}"


# Search arXiv for papers
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

# Search PubMed for papers
def search_pubmed(query, max_results=5):
    Entrez.email = "your.email@example.com"  # Use your email here
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    id_list = record["IdList"]
    
    papers = []
    if id_list:
        handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        for article in records['PubmedArticle']:
            title = article['MedlineCitation']['Article']['ArticleTitle']
            authors_list = article['MedlineCitation']['Article']['AuthorList']
            authors = ', '.join([f"{author['ForeName']} {author['LastName']}" for author in authors_list])
            abstract = article['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', [""])[0]
            link = f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']}/"
            
            papers.append({
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'link': link
            })
    return papers

# Search Semantic Scholar for papers
def search_semantic_scholar(query, max_results=5):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={max_results}"
    response = requests.get(url)
    data = response.json()

    papers = []
    if 'data' in data:
        for paper in data['data']:
            title = paper['title']
            authors = ', '.join([author['name'] for author in paper['authors']])
            link = paper['url']
            abstract = paper.get('abstract', 'No abstract available')

            papers.append({
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'link': link
            })
    return papers

# Analyze the sentiment of a given text (abstract or summary)
def analyze_sentiment(text):
    sentiment_scores = analyzer.polarity_scores(text)
    return sentiment_scores['compound']  # The compound score represents overall sentiment

# Core function to search and summarize research papers from multiple sources
def research_papers(query, max_results=5):
    # Retrieve papers from multiple sources
    arxiv_papers = search_arxiv(query, max_results)
    pubmed_papers = search_pubmed(query, max_results)
    semantic_scholar_papers = search_semantic_scholar(query, max_results)

    # Combine results
    combined_results = []
    
    # Process arXiv papers
    for paper in arxiv_papers:
        generated_summary = generate_summary(paper['summary'])
        bibtex = generate_bibtex(paper)
        sentiment = analyze_sentiment(paper['summary'])
        
        combined_results.append({
            'title': paper['title'],
            'authors': ', '.join(paper['authors']),
            'published': paper['published'],
            'link': paper['link'],
            'generated_summary': generated_summary,
            'bibtex': bibtex,
            'sentiment': sentiment
        })

    # Process PubMed papers
    for paper in pubmed_papers:
        generated_summary = generate_summary(paper['abstract'])
        sentiment = analyze_sentiment(paper['abstract'])
        
        combined_results.append({
            'title': paper['title'],
            'authors': paper['authors'],
            'link': paper['link'],
            'generated_summary': generated_summary,
            'bibtex': "",  # PubMed doesn't provide BibTeX data natively
            'sentiment': sentiment
        })

    # Process Semantic Scholar papers
    for paper in semantic_scholar_papers:
        generated_summary = generate_summary(paper['abstract'])
        sentiment = analyze_sentiment(paper['abstract'])
        
        combined_results.append({
            'title': paper['title'],
            'authors': paper['authors'],
            'link': paper['link'],
            'generated_summary': generated_summary,
            'bibtex': "",  # Semantic Scholar doesn't provide BibTeX data natively
            'sentiment': sentiment
        })

    return combined_results

