"""
Web Scraper for quotes.toscrape.com

This script scrapes quotes and author information from quotes.toscrape.com,
following pagination links automatically. It extracts quote text, author,
tags, and author bio URLs from the quotes pages, then follows each author's
bio link to collect additional details. Results are saved to CSV files and
a summary is printed with key statistics.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = 'http://quotes.toscrape.com'

def scrape_quotes_page(url: str, session: requests.Session, base_url: str) -> tuple[list[dict], str | None]:
    """Scrape quotes from a single page and return next page URL."""
    try:
        with session.get(url) as res:
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')
            quotes = []
            quote_divs = soup.find_all('div', class_='quote')
            for quote_div in quote_divs:
                try:
                    text = quote_div.find('span', class_='text').text
                    author = quote_div.find('small', class_='author').text
                    bio_tag = quote_div.find('a')  # this should be the author link
                    bio_url_full = f"{base_url}{bio_tag['href']}" if bio_tag else ''
                    tags = [a.text for a in quote_div.find_all('a', class_='tag')]
                    quotes.append({
                        'text': text,
                        'author': author,
                        'tags': tags,
                        'bio_url': bio_url_full
                    })
                except Exception as e:
                    print(f"Error parsing quote: {e}")
                    continue
            # get next page URL
            next_page = soup.find('li', class_='next')
            next_page_url = None
            if next_page:
                href = next_page.find('a')['href']
                next_page_url = f"{base_url}{href}"
            return quotes, next_page_url
    except Exception as e:
        print(f"Error scraping page {url}: {e}")
        return [], None

def scrape_author_bio(url: str, session: requests.Session) -> dict:
    """Scrape author details from their bio page."""
    try:
        with session.get(url) as res:
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'lxml')
            details = soup.find('div', class_='author-details')
            if not details:
                return {}
            born_date_tag = details.find('p', class_='author-born-date')
            born_location_tag = details.find('p', class_='author-born-location')
            description_tag = details.find('p', class_='author-description')
            name_tag = details.find('h3', class_='author-title')
            return {
                'name': name_tag.text.strip() if name_tag else '',
                'born_date': born_date_tag.text.strip() if born_date_tag else '',
                'born_location': born_location_tag.text.strip() if born_location_tag else '',
                'description': description_tag.text.strip() if description_tag else ''
            }
    except Exception as e:
        print(f"Error scraping author bio from {url}: {e}")
        return {}

def save_results(quotes: list[dict], authors: list[dict]) -> None:
    """Save scraped data to CSV files."""
    try:
        # Process quotes
        quotes_df = pd.DataFrame(quotes)
        # Convert tags list to comma-separated string
        quotes_df['tags'] = quotes_df['tags'].apply(lambda tags: ','.join(tags))
        # Save quotes to CSV
        quotes_df[['text', 'author', 'tags', 'bio_url']].to_csv('quotes_full.csv', index=False)
        
        # Process authors
        authors_df = pd.DataFrame(authors)
        # Save authors to CSV
        authors_df[['name', 'born_date', 'born_location', 'description']].to_csv('authors.csv', index=False)
    except Exception as e:
        print(f"Error saving results: {e}")

def print_summary(quotes: list[dict], authors: list[dict]) -> None:
    """Print summary statistics about the scraped data."""
    try:
        total_quotes = len(quotes)
        unique_authors_count = len(set(quote['author'] for quote in quotes))
        
        # Count tags
        tag_counts = {}
        for quote in quotes:
            for tag in quote['tags'].split(','):
                if tag:  # avoid empty strings if any
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        # Sort tags by count descending
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        top_tags = sorted_tags[:10]
        
        print("── SUMMARY ──")
        print(f"Total quotes scraped: {total_quotes}")
        print(f"Unique authors: {unique_authors_count}")
        print("Top 10 tags by frequency:")
        for tag, count in top_tags:
            print(f"  {tag}: {count}")
    except Exception as e:
        print(f"Error printing summary: {e}")

def main() -> None:
    """Main function to orchestrate the scraping process."""
    headers = {
        'User-Agent': 'QuotesScraper/1.0'
    }
    quotes = []
    authors = []
    seen_authors = set()  # track bio URLs to avoid duplicates
    
    with requests.Session() as session:
        session.headers.update(headers)
        current_url = f"{base_url}/page/1/"
        page_number = 1
        
        while True:
            # Extract current page number from URL
            if '/page/' in current_url:
                try:
                    page_number_str = current_url.split('/page/')[-1].strip('/')
                    page_number = int(page_number_str) if page_number_str else 1
                except ValueError:
                    page_number = 1
            else:
                page_number = 1
            
            print(f"Scraping page {page_number}/10... ({len(quotes)} quotes collected)")
            
            page_quotes, next_page_url = scrape_quotes_page(current_url, session, base_url)
            quotes.extend(page_quotes)
            
            # Process new authors from current page quotes
            for quote in page_quotes:
                bio_url = quote['bio_url']
                if bio_url not in seen_authors:
                    author_data = scrape_author_bio(bio_url, session)
                    if author_data:
                        authors.append(author_data)
                        seen_authors.add(bio_url)
            
            if not next_page_url:
                break
            
            current_url = next_page_url
            time.sleep(0.5)
        
    save_results(quotes, authors)
    print_summary(quotes, authors)

if __name__ == '__main__':
    main()