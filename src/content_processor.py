"""
Content processor module for analyzing and structuring extracted documentation content.
This module handles content analysis, hierarchy detection, and text processing.
"""

import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import logging

class ContentProcessor:
    def __init__(self):
        """Initialize the content processor."""
        self.logger = logging.getLogger(__name__)
        
        # Common section indicators
        self.section_indicators = [
            r'(?i)getting\s+started',
            r'(?i)quick\s+start',
            r'(?i)installation',
            r'(?i)setup',
            r'(?i)configuration',
            r'(?i)api\s+reference',
            r'(?i)user\s+guide',
            r'(?i)tutorial',
            r'(?i)how\s+to',
            r'(?i)faq',
            r'(?i)troubleshooting',
            r'(?i)account\s+management',
            r'(?i)billing',
            r'(?i)security',
            r'(?i)integration',
            r'(?i)features',
            r'(?i)settings',
            r'(?i)admin',
            r'(?i)dashboard'
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', '', text)
        
        # Remove very short lines (likely navigation or footer text)
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return ' '.join(cleaned_lines).strip()
    
    def extract_headings(self, content: str) -> List[Tuple[str, int]]:
        """
        Extract heading-like structures from content.
        
        Args:
            content: Text content
            
        Returns:
            List of tuples (heading_text, estimated_level)
        """
        headings = []
        
        # Split content into sentences/paragraphs
        sentences = re.split(r'[.!?]\s+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if sentence looks like a heading
            # Characteristics: Short, title case, ends with certain patterns
            if (len(sentence) < 100 and 
                len(sentence) > 5 and
                sentence[0].isupper() and
                not sentence.endswith(',') and
                not sentence.startswith('The ') and
                not sentence.startswith('This ') and
                not sentence.startswith('You can')):
                
                # Estimate heading level based on length and characteristics
                level = 1
                if len(sentence) > 50:
                    level = 2
                elif any(indicator in sentence.lower() for indicator in ['how to', 'step', 'guide']):
                    level = 2
                
                headings.append((sentence, level))
        
        return headings
    
    def detect_modules_from_structure(self, pages: List[Dict[str, str]]) -> Dict[str, List[str]]:
        """
        Detect potential modules based on page structure and content.
        
        Args:
            pages: List of page data dictionaries
            
        Returns:
            Dictionary mapping module names to related content
        """
        modules = defaultdict(list)
        
        for page in pages:
            title = page.get('title', '')
            content = page.get('content', '')
            url = page.get('url', '')
            
            # Extract potential module from URL path
            url_parts = [part for part in url.split('/') if part and len(part) > 2]
            
            # Extract potential modules from title
            title_modules = self.extract_modules_from_text(title)
            
            # Extract potential modules from content headings
            headings = self.extract_headings(content)
            content_modules = []
            for heading, level in headings:
                if level == 1:  # Top level headings are likely modules
                    content_modules.extend(self.extract_modules_from_text(heading))
            
            # Combine all potential modules
            all_modules = title_modules + content_modules
            
            # If no modules found, try to infer from URL or content patterns
            if not all_modules:
                if url_parts:
                    all_modules = [self.clean_module_name(part) for part in url_parts[-2:]]
                else:
                    # Try to extract from first few sentences
                    sentences = content.split('.')[:3]
                    for sentence in sentences:
                        all_modules.extend(self.extract_modules_from_text(sentence))
            
            # Add content to modules
            for module in all_modules:
                if module and len(module) > 2:
                    modules[module].append({
                        'title': title,
                        'content': content[:500],  # First 500 chars
                        'url': url
                    })
        
        return dict(modules)
    
    def extract_modules_from_text(self, text: str) -> List[str]:
        """
        Extract potential module names from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of potential module names
        """
        modules = []
        
        if not text:
            return modules
        
        # Look for section indicators
        for pattern in self.section_indicators:
            matches = re.findall(pattern, text)
            for match in matches:
                modules.append(self.clean_module_name(match))
        
        # Extract title case phrases (potential module names)
        title_case_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        matches = re.findall(title_case_pattern, text)
        for match in matches:
            if len(match) > 3 and len(match) < 50:
                modules.append(self.clean_module_name(match))
        
        return list(set(modules))  # Remove duplicates
    
    def clean_module_name(self, name: str) -> str:
        """
        Clean and normalize module names.
        
        Args:
            name: Raw module name
            
        Returns:
            Cleaned module name
        """
        if not name:
            return ""
        
        # Remove special characters
        name = re.sub(r'[^\w\s]', '', name)
        
        # Convert to title case
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Remove common words that shouldn't be in module names
        stop_words = ['The', 'And', 'Or', 'But', 'In', 'On', 'At', 'To', 'For', 'Of', 'With', 'By']
        words = name.split()
        cleaned_words = [word for word in words if word not in stop_words or words.index(word) == 0]
        
        return ' '.join(cleaned_words).strip()
    
    def group_related_content(self, modules: Dict[str, List[str]]) -> Dict[str, Dict[str, List[str]]]:
        """
        Group related content and identify submodules.
        
        Args:
            modules: Dictionary of modules and their content
            
        Returns:
            Dictionary with modules and their submodules
        """
        grouped = {}
        
        for module_name, content_list in modules.items():
            grouped[module_name] = {
                'main_content': [],
                'submodules': {}
            }
            
            for content_item in content_list:
                title = content_item.get('title', '')
                content = content_item.get('content', '')
                
                # Extract potential submodules from title and content
                submodules = self.extract_submodules(title + ' ' + content, module_name)
                
                if submodules:
                    for submodule in submodules:
                        if submodule not in grouped[module_name]['submodules']:
                            grouped[module_name]['submodules'][submodule] = []
                        grouped[module_name]['submodules'][submodule].append(content)
                else:
                    grouped[module_name]['main_content'].append(content)
        
        return grouped
    
    def extract_submodules(self, content: str, parent_module: str) -> List[str]:
        """
        Extract potential submodules from content.
        
        Args:
            content: Content to analyze
            parent_module: Parent module name
            
        Returns:
            List of submodule names
        """
        submodules = []
        
        # Look for action-oriented phrases (common in submodules)
        action_patterns = [
            r'(?i)how\s+to\s+([^.!?]{5,50})',
            r'(?i)create\s+([^.!?]{5,30})',
            r'(?i)delete\s+([^.!?]{5,30})',
            r'(?i)manage\s+([^.!?]{5,30})',
            r'(?i)configure\s+([^.!?]{5,30})',
            r'(?i)setup\s+([^.!?]{5,30})',
            r'(?i)add\s+([^.!?]{5,30})',
            r'(?i)remove\s+([^.!?]{5,30})',
            r'(?i)update\s+([^.!?]{5,30})',
            r'(?i)edit\s+([^.!?]{5,30})'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                clean_match = self.clean_module_name(match)
                if clean_match and clean_match.lower() not in parent_module.lower():
                    submodules.append(clean_match)
        
        # Look for numbered or bulleted lists (often contain submodules)
        list_pattern = r'(?:^\d+\.|^\*\s+|^-\s+)([^.!?\n]{10,60})'
        matches = re.findall(list_pattern, content, re.MULTILINE)
        for match in matches:
            clean_match = self.clean_module_name(match)
            if clean_match and len(clean_match) > 5:
                submodules.append(clean_match)
        
        return list(set(submodules))[:5]  # Limit to 5 submodules per module
    
    def process_pages(self, pages: List[Dict[str, str]]) -> Dict[str, Dict]:
        """
        Main processing function to extract modules and submodules from pages.
        
        Args:
            pages: List of scraped page data
            
        Returns:
            Processed structure with modules and submodules
        """
        self.logger.info(f"Processing {len(pages)} pages for module extraction")
        
        # Clean content from all pages
        cleaned_pages = []
        for page in pages:
            cleaned_page = page.copy()
            cleaned_page['content'] = self.clean_text(page.get('content', ''))
            cleaned_page['title'] = self.clean_text(page.get('title', ''))
            if cleaned_page['content']:  # Only keep pages with content
                cleaned_pages.append(cleaned_page)
        
        # Detect modules from structure
        modules = self.detect_modules_from_structure(cleaned_pages)
        
        # Group related content and identify submodules
        grouped_content = self.group_related_content(modules)
        
        self.logger.info(f"Extracted {len(grouped_content)} modules")
        return grouped_content