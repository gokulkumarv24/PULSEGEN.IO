"""
AI Module Extractor using OpenAI API to intelligently identify and describe modules and submodules.
This module uses advanced NLP to understand documentation structure and generate accurate descriptions.
"""

from openai import OpenAI
import json
import logging
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import time
import re

# Load environment variables
load_dotenv()

class AIModuleExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Module Extractor.
        
        Args:
            api_key: OpenAI API key (if not provided, will look for OPENAI_API_KEY env var)
        """
        self.logger = logging.getLogger(__name__)
        
        # Set up OpenAI API
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            # For demo purposes, we'll use a fallback method
            self.use_openai = False
            self.client = None
            self.logger.warning("OpenAI API key not found. Using fallback extraction method.")
        else:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_openai = True
                self.logger.info("OpenAI client initialized successfully.")
            except Exception as e:
                self.logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.logger.warning("Falling back to rule-based extraction method.")
                self.use_openai = False
                self.client = None
    
    def create_analysis_prompt(self, content_data: Dict[str, Dict]) -> str:
        """
        Create a detailed prompt for AI analysis.
        
        Args:
            content_data: Processed content data from ContentProcessor
            
        Returns:
            Formatted prompt for AI analysis
        """
        prompt = """
You are an expert at analyzing software documentation and extracting structured information about product modules and features.

Your task is to analyze the following documentation content and identify:
1. Main modules (high-level feature categories)
2. Submodules (specific features/functions within each module)
3. Detailed descriptions for both modules and submodules

Guidelines:
- Focus on user-facing features and functionality
- Group related features logically
- Create clear, concise descriptions based on the content
- Avoid duplicate or overly similar modules
- Prioritize modules that appear most frequently or prominently

Here is the documentation content to analyze:

"""
        
        # Add content data
        for module_name, module_data in content_data.items():
            prompt += f"\n--- Module: {module_name} ---\n"
            
            # Add main content
            if module_data.get('main_content'):
                prompt += "Main Content:\n"
                for content in module_data['main_content'][:3]:  # Limit content
                    prompt += f"- {content[:200]}...\n"
            
            # Add submodule information
            if module_data.get('submodules'):
                prompt += "Potential Submodules:\n"
                for sub_name, sub_content in module_data['submodules'].items():
                    prompt += f"- {sub_name}: {sub_content[0][:100] if sub_content else ''}...\n"
        
        prompt += """

Please return a JSON response in the following format:
[
  {
    "module": "Module Name",
    "Description": "Detailed description of the module based on the content",
    "Submodules": {
      "submodule_1": "Detailed description of submodule 1",
      "submodule_2": "Detailed description of submodule 2"
    }
  }
]

Ensure descriptions are informative and based on the actual content provided.
"""
        
        return prompt
    
    def query_openai(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Query OpenAI API with retry logic.
        
        Args:
            prompt: The prompt to send
            max_retries: Maximum number of retries
            
        Returns:
            AI response or None if failed
        """
        # Check if client is available
        if not self.client:
            self.logger.warning("OpenAI client not available, cannot query API")
            return None
            
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert at analyzing software documentation and extracting structured module information."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.3
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                error_str = str(e).lower()
                if "rate limit" in error_str:
                    wait_time = (2 ** attempt) * 60  # Exponential backoff
                    self.logger.warning(f"Rate limit hit. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                elif "api" in error_str:
                    self.logger.error(f"OpenAI API error: {e}")
                    time.sleep(5)
                else:
                    self.logger.error(f"Unexpected error querying OpenAI: {e}")
                    break
        
        return None
    
    def fallback_extraction(self, content_data: Dict[str, Dict]) -> List[Dict]:
        """
        Fallback method when OpenAI API is not available.
        Uses rule-based extraction and predefined patterns.
        
        Args:
            content_data: Processed content data
            
        Returns:
            List of modules in the required format
        """
        self.logger.info("Using fallback extraction method")
        
        modules = []
        
        # Common module patterns and descriptions
        module_templates = {
            'account': 'Account Management - Features for managing user accounts, profiles, and personal settings',
            'billing': 'Billing and Payments - Payment processing, subscription management, and billing features',
            'security': 'Security and Privacy - Security settings, privacy controls, and account protection features',
            'api': 'API and Integration - API documentation, integration guides, and developer resources',
            'setup': 'Setup and Configuration - Initial setup, configuration options, and getting started guides',
            'support': 'Support and Help - Help resources, troubleshooting, and customer support features',
            'dashboard': 'Dashboard and Analytics - Main dashboard features and analytics tools',
            'user': 'User Management - User account features and management capabilities',
            'settings': 'Settings and Preferences - Application settings and user preferences',
            'admin': 'Administration - Administrative tools and management features'
        }
        
        for module_name, module_data in content_data.items():
            # Clean module name
            clean_name = self.clean_module_name(module_name)
            
            # Generate description based on content and templates
            description = self.generate_description(clean_name, module_data, module_templates)
            
            # Extract submodules
            submodules = self.extract_submodules_fallback(module_data)
            
            modules.append({
                'module': clean_name,
                'Description': description,
                'Submodules': submodules
            })
        
        return modules
    
    def clean_module_name(self, name: str) -> str:
        """Clean and format module names."""
        # Remove special characters and normalize
        clean_name = re.sub(r'[^\w\s]', '', name)
        # Convert to title case
        return ' '.join(word.capitalize() for word in clean_name.split())
    
    def generate_description(self, module_name: str, module_data: Dict, templates: Dict) -> str:
        """
        Generate module description using templates and content analysis.
        
        Args:
            module_name: Name of the module
            module_data: Module content data
            templates: Template descriptions
            
        Returns:
            Generated description
        """
        # Check if module name matches any template
        name_lower = module_name.lower()
        for template_key, template_desc in templates.items():
            if template_key in name_lower:
                return template_desc
        
        # Generate description from content
        all_content = ""
        if module_data.get('main_content'):
            all_content += ' '.join(module_data['main_content'][:2])
        
        # Extract key features from content
        features = self.extract_key_features(all_content)
        
        if features:
            return f"{module_name} - {features}"
        else:
            return f"{module_name} - Documentation and features related to {module_name.lower()}"
    
    def extract_key_features(self, content: str) -> str:
        """Extract key features from content text."""
        if not content:
            return ""
        
        # Look for action words and features
        feature_patterns = [
            r'(?i)(manage|create|delete|configure|setup|add|remove|update|edit|view)\s+([^.]{5,30})',
            r'(?i)(features?|capabilities?|options?)\s+(?:include|for)\s+([^.]{10,50})',
            r'(?i)(allows?|enables?)\s+(?:you\s+to\s+)?([^.]{10,50})'
        ]
        
        features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, content[:500])  # First 500 chars
            for match in matches:
                if len(match) == 2:
                    features.append(f"{match[0]} {match[1]}")
        
        if features:
            return f"Features for {', '.join(features[:3])}"
        else:
            # Fallback: use first meaningful sentence
            sentences = content.split('.')[:2]
            return sentences[0][:100] + "..." if sentences else "Related features and functionality"
    
    def extract_submodules_fallback(self, module_data: Dict) -> Dict[str, str]:
        """
        Extract submodules using fallback method.
        
        Args:
            module_data: Module content data
            
        Returns:
            Dictionary of submodules and descriptions
        """
        submodules = {}
        
        # Get submodules from processed data
        if module_data.get('submodules'):
            for sub_name, sub_content in module_data['submodules'].items():
                description = self.generate_submodule_description(sub_name, sub_content)
                submodules[sub_name] = description
        
        # If no submodules found, try to extract from main content
        if not submodules and module_data.get('main_content'):
            content = ' '.join(module_data['main_content'])
            extracted_subs = self.extract_submodules_from_text(content)
            for sub_name in extracted_subs:
                submodules[sub_name] = f"Features and functionality related to {sub_name.lower()}"
        
        return submodules
    
    def generate_submodule_description(self, sub_name: str, sub_content: List[str]) -> str:
        """Generate description for a submodule."""
        if not sub_content:
            return f"Features related to {sub_name.lower()}"
        
        # Use first content item for description
        content = sub_content[0][:200] if sub_content[0] else ""
        
        # Clean and format
        sentences = content.split('.')
        if sentences and len(sentences[0]) > 20:
            return sentences[0].strip() + "."
        else:
            return f"Functionality for {sub_name.lower()} operations and management"
    
    def extract_submodules_from_text(self, text: str) -> List[str]:
        """Extract potential submodules from text content."""
        # Look for common submodule patterns
        patterns = [
            r'(?i)(create|add|delete|remove|manage|configure|setup|update|edit)\s+([a-zA-Z\s]{3,25})',
            r'(?i)(how\s+to)\s+([a-zA-Z\s]{5,30})'
        ]
        
        submodules = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 2:
                    sub_name = f"{match[0].title()} {match[1].title()}"
                    submodules.append(sub_name.strip())
        
        return list(set(submodules))[:5]  # Limit to 5 submodules
    
    def parse_ai_response(self, response: str) -> List[Dict]:
        """
        Parse AI response and convert to required format.
        
        Args:
            response: Raw AI response
            
        Returns:
            Parsed module list
        """
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Try to parse the entire response as JSON
                return json.loads(response)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response as JSON: {e}")
            return []
    
    def extract_modules(self, content_data: Dict[str, Dict]) -> List[Dict]:
        """
        Main method to extract modules using AI or fallback method.
        
        Args:
            content_data: Processed content data from ContentProcessor
            
        Returns:
            List of modules in the required format
        """
        self.logger.info("Starting AI module extraction")
        
        if self.use_openai and len(content_data) > 0:
            # Use OpenAI API
            prompt = self.create_analysis_prompt(content_data)
            ai_response = self.query_openai(prompt)
            
            if ai_response:
                parsed_modules = self.parse_ai_response(ai_response)
                if parsed_modules:
                    self.logger.info(f"Successfully extracted {len(parsed_modules)} modules using AI")
                    return parsed_modules
        
        # Use fallback method
        return self.fallback_extraction(content_data)
    
    def validate_output_format(self, modules: List[Dict]) -> List[Dict]:
        """
        Validate and clean the output format.
        
        Args:
            modules: List of modules
            
        Returns:
            Validated and cleaned modules
        """
        validated = []
        
        for module in modules:
            if not isinstance(module, dict):
                continue
            
            # Ensure required fields exist
            if 'module' not in module or 'Description' not in module:
                continue
            
            clean_module = {
                'module': str(module['module']).strip(),
                'Description': str(module['Description']).strip(),
                'Submodules': {}
            }
            
            # Clean submodules
            if 'Submodules' in module and isinstance(module['Submodules'], dict):
                for sub_name, sub_desc in module['Submodules'].items():
                    if sub_name and sub_desc:
                        clean_module['Submodules'][str(sub_name).strip()] = str(sub_desc).strip()
            
            validated.append(clean_module)
        
        return validated