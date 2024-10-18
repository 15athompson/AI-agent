import requests
import json

# Function to search arXiv for papers
def search_arxiv(query, max_results=5):
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{query}&start=0&max_results={max_results}"
    url = base_url + query
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve data from arXiv")
        return None

# Extracting data from arXiv XML response (example)
from bs4 import BeautifulSoup

def parse_arxiv_response(response):
    soup = BeautifulSoup(response, "lxml")
    entries = soup.find_all("entry")
    
    papers = []
    for entry in entries:
        title = entry.title.text.strip()
        summary = entry.summary.text.strip()
        authors = [author.text for author in entry.find_all("author")]
        link = entry.id.text
        published = entry.published.text
        
        papers.append({
            "title": title,
            "summary": summary,
            "authors": authors,
            "link": link,
            "published": published
        })
    return papers

# Example of querying and extracting data
query = "machine learning"
response = search_arxiv(query)
if response:
    papers = parse_arxiv_response(response)
    for paper in papers:
        print(json.dumps(paper, indent=2))



import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# Load spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

# Preprocessing function for cleaning text
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
    return tokens

# Topic modeling using LDA
def topic_modeling(documents, num_topics=3):
    processed_docs = [preprocess_text(doc) for doc in documents]
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    topics = lda_model.print_topics(num_words=5)
    
    return topics

# Example usage for summaries from arXiv papers
summaries = [paper['summary'] for paper in papers]
topics = topic_modeling(summaries)
print("Identified Topics:")
for topic in topics:
    print(topic)


from transformers import pipeline

# Summarization pipeline using Hugging Face's transformers
summarizer = pipeline("summarization")

def generate_summary(text, max_length=150):
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Example usage
for paper in papers:
    summary = generate_summary(paper['summary'])
    print(f"Original Summary: {paper['summary']}")
    print(f"Generated Summary: {summary}")
    print("-" * 80)



from pybtex.database import BibliographyData, Entry

def generate_bibtex(paper):
    bib_data = BibliographyData({
        'citation_key': Entry(
            'article',
            fields={
                'title': paper['title'],
                'author': ' and '.join(paper['authors']),
                'journal': 'arXiv',
                'year': paper['published'][:4],
                'url': paper['link']
            }
        )
    })
    return bib_data.to_string('bibtex')

# Example usage
for paper in papers:
    print(generate_bibtex(paper))



def research_papers(query, max_results=5):
    # Step 1: Retrieve Papers
    response = search_arxiv(query, max_results)
    if not response:
        return
    
    papers = parse_arxiv_response(response)
    
    # Step 2: Analyze Papers (Topic Modeling)
    summaries = [paper['summary'] for paper in papers]
    topics = topic_modeling(summaries)
    
    # Print Topics
    print("Identified Topics:")
    for topic in topics:
        print(topic)
    
    # Step 3: Summarize and Output Results
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Link: {paper['link']}")
        print(f"Published: {paper['published']}")
        
        # Generate summary
        generated_summary = generate_summary(paper['summary'])
        print(f"Summary: {generated_summary}")
        
        # Citation in BibTeX format
        bibtex = generate_bibtex(paper)
        print(f"BibTeX Citation:\n{bibtex}")
        print("-" * 80)

# Run the full pipeline
research_papers("neural networks in medical imaging")
