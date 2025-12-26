"""
Web scraper module for extracting content from documentation websites.
This module handles crawling, content extraction, and text processing.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import logging
from typing import List, Dict, Set, Optional
import re

class WebScraper:
    def __init__(self, delay: float = 1.0, max_depth: int = 3, max_pages: int = 50):
        """
        Initialize the web scraper.
        
        Args:
            delay: Delay between requests in seconds
            max_depth: Maximum crawling depth
            max_pages: Maximum number of pages to scrape
        """
        self.delay = delay
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible."""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False
    
    def is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs belong to the same domain."""
        return urlparse(url1).netloc == urlparse(url2).netloc
    
    def clean_url(self, url: str) -> str:
        """Clean and normalize URL."""
        parsed = urlparse(url)
        # Remove fragment
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, 
                          parsed.params, parsed.query, ''))
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a single page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Check if it's HTML content
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type.lower():
                self.logger.warning(f"Non-HTML content detected: {url}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error processing {url}: {e}")
            return None
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract relevant internal links from a page.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            List of cleaned URLs
        """
        links = []
        
        # Find all anchor tags with href
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip empty links, fragments, and javascript
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Resolve relative URLs
            absolute_url = urljoin(base_url, href)
            
            # Only include links from the same domain
            if self.is_same_domain(absolute_url, base_url):
                cleaned_url = self.clean_url(absolute_url)
                if cleaned_url not in links:
                    links.append(cleaned_url)
        
        return links
    
    def extract_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract meaningful content from a page.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dictionary with title and content
        """
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                           'aside', 'advertisement', 'cookie', 'banner']):
            element.decompose()
        
        # Extract title
        title = ""
        if soup.title:
            title = soup.title.get_text().strip()
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        
        # Extract main content
        content_selectors = [
            'main', 'article', '[role="main"]', 
            '.content', '#content', '.documentation',
            '.help-content', '.article-content'
        ]
        
        content = ""
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                content = main_content.get_text(separator=' ', strip=True)
                break
        
        # If no main content found, extract from body
        if not content and soup.body:
            content = soup.body.get_text(separator=' ', strip=True)
        
        # Clean content
        content = re.sub(r'\s+', ' ', content).strip()
        
        return {
            'title': title,
            'content': content
        }
    
    def crawl_website(self, start_urls: List[str]) -> List[Dict[str, str]]:
        """
        Crawl website starting from given URLs.
        
        Args:
            start_urls: List of starting URLs
            
        Returns:
            List of dictionaries containing page data
        """
        if not start_urls:
            self.logger.error("No start URLs provided")
            return []
        
        visited = set()
        to_visit = [(url, 0) for url in start_urls]  # (url, depth)
        results = []
        
        while to_visit and len(results) < self.max_pages:
            current_url, depth = to_visit.pop(0)
            
            # Skip if already visited or max depth exceeded
            if current_url in visited or depth > self.max_depth:
                continue
            
            visited.add(current_url)
            
            # Get page content
            soup = self.get_page_content(current_url)
            if not soup:
                continue
            
            # Extract content
            page_data = self.extract_content(soup)
            if page_data['content']:  # Only add pages with meaningful content
                page_data['url'] = current_url
                page_data['depth'] = depth
                results.append(page_data)
            
            # Extract links for next level crawling
            if depth < self.max_depth:
                links = self.extract_links(soup, current_url)
                for link in links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))
            
            # Rate limiting
            time.sleep(self.delay)
        
        self.logger.info(f"Crawling completed. Found {len(results)} pages.")
        return results
    
    def scrape_single_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a single URL without crawling.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with page data or None
        """
        if not self.is_valid_url(url):
            self.logger.error(f"Invalid URL: {url}")
            return None
        
        soup = self.get_page_content(url)
        if not soup:
            return None
        
        page_data = self.extract_content(soup)
        page_data['url'] = url
        page_data['depth'] = 0
        
        return page_data if page_data['content'] else None