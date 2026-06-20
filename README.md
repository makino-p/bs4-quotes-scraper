# bs4-quotes-scraper

> BeautifulSoup — Advanced Quotes Scraper

`BeautifulSoup4` `Web Scraping` `Requests` `Pagination`

---

## Overview

Create a professional web scraper using requests and BeautifulSoup4.

Target: http://quotes.toscrape.com (all 10 pages)

Requirements:
- Scrape ALL pages automatically by following pagination links
- Extract per quote: text, author, tags, author_bio_url
- Fetch each author's bio page and extract: born_date, born_location, description
- Use a requests.Session() with proper headers
- Add 0.5 second delay between requests (polite crawling)
- Show progress: "Scraping page 2/10... (15 quotes collected)"
- Save to quotes_full.csv with all fields
- Save to authors.csv with unique author details
- Pri

## Features

- Scrape ALL pages automatically by following pagination links
- Extract per quote: text, author, tags, author_bio_url
- Fetch each author's bio page and extract: born_date, born_location, description
- Use a requests.Session() with proper headers
- Add 0.5 second delay between requests (polite crawling)
- Show progress: "Scraping page 2/10... (15 quotes collected)"
- Save to quotes_full.csv with all fields
- Save to authors.csv with unique author details
- Print summary: total quotes, unique authors, top 10 tags by frequency
- Functions: scrape_quotes_page(), scrape_author_bio(), save_results(), print_summary()

---

## Tech Stack

| Library | Purpose |
|---|---|
| `bs4` | Data processing |
| `pandas` | Data processing |
| `requests` | Data processing |

---

## Quick Start

```bash
git clone https://github.com/makino-p/bs4-quotes-scraper.git
cd bs4-quotes-scraper
pip install bs4 pandas requests
python solution.py
```

## Dependencies

```bash
pip install bs4 pandas requests
```

## Key Functions

- `scrape_quotes_page()`
- `scrape_author_bio()`
- `save_results()`
- `print_summary()`
- `main()`

## Output Files

| File | Description |
|---|---|
| `.git` | Generated output |
| `authors.csv` | Generated output |
| `quotes_full.csv` | Generated output |

---

## Project Stats

- **Lines of code**: 167
- **Functions**: 5
- **Output files**: 3

---

## Skills Demonstrated

`BeautifulSoup4` `Web Scraping` `Requests` `Pagination`

---

## License

MIT
