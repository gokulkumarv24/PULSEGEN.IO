#!/usr/bin/env python3
"""
Module Extraction AI Agent - Command Line Interface

This script extracts structured information from documentation websites,
identifying key modules and submodules with detailed descriptions.

Creator: Gokul Kumar V
GitHub: https://github.com/gokulkumarv24
LinkedIn: https://www.linkedin.com/in/gokul-kumar-v-236a24217

Usage:
    python module_extractor.py --urls https://help.example.com
    python module_extractor.py --urls https://help.site1.com https://help.site2.com
    python module_extractor.py --file urls.txt --output results.json
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import List
import logging

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from web_scraper import WebScraper
    from content_processor import ContentProcessor
    from ai_extractor import AIModuleExtractor
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required packages are installed: pip install -r requirements.txt")
    sys.exit(1)

class ModuleExtractorCLI:
    def __init__(self):
        """Initialize the CLI application."""
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def setup_logging(self, verbose: bool = False):
        """Setup logging configuration."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Extract structured modules from documentation websites",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --urls https://help.instagram.com
  %(prog)s --urls https://support.neo.space/hc/en-us https://help.zluri.com/
  %(prog)s --file urls.txt --output results.json
  %(prog)s --urls https://wordpress.org/documentation/ --openai-key YOUR_KEY
            """
        )
        
        # URL input options (mutually exclusive)
        url_group = parser.add_mutually_exclusive_group(required=True)
        url_group.add_argument(
            '--urls',
            nargs='+',
            help='One or more documentation URLs to process'
        )
        url_group.add_argument(
            '--file',
            help='Text file containing URLs (one per line)'
        )
        
        # Output options
        parser.add_argument(
            '--output', '-o',
            default='output/modules_{timestamp}.json',
            help='Output JSON file path (default: output/modules_TIMESTAMP.json)'
        )
        
        # Scraping configuration
        parser.add_argument(
            '--delay',
            type=float,
            default=1.0,
            help='Delay between HTTP requests in seconds (default: 1.0)'
        )
        parser.add_argument(
            '--max-pages',
            type=int,
            default=30,
            help='Maximum number of pages to scrape (default: 30)'
        )
        parser.add_argument(
            '--max-depth',
            type=int,
            default=2,
            help='Maximum crawling depth (default: 2)'
        )
        
        # AI configuration
        parser.add_argument(
            '--openai-key',
            help='OpenAI API key for enhanced module extraction'
        )
        parser.add_argument(
            '--no-ai',
            action='store_true',
            help='Use only rule-based extraction (no AI)'
        )
        
        # Display options
        parser.add_argument(
            '--pretty',
            action='store_true',
            help='Pretty print JSON output to console'
        )
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose logging'
        )
        parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Suppress all output except errors'
        )
        
        return parser.parse_args()
    
    def read_urls_from_file(self, file_path: str) -> List[str]:
        """
        Read URLs from a text file.
        
        Args:
            file_path: Path to the file containing URLs
            
        Returns:
            List of URLs
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            return urls
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return []
    
    def validate_urls(self, urls: List[str]) -> List[str]:
        """
        Validate URLs and return only valid ones.
        
        Args:
            urls: List of URLs to validate
            
        Returns:
            List of valid URLs
        """
        valid_urls = []
        
        for url in urls:
            # Basic URL validation
            if url.startswith(('http://', 'https://')) and '.' in url:
                valid_urls.append(url)
            else:
                self.logger.warning(f"Invalid URL skipped: {url}")
        
        return valid_urls
    
    def create_output_path(self, output_template: str) -> str:
        """
        Create output file path with timestamp replacement.
        
        Args:
            output_template: Output path template
            
        Returns:
            Actual output file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_template.replace('{timestamp}', timestamp)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        return output_path
    
    def extract_modules(self, urls: List[str], args: argparse.Namespace) -> List[dict]:
        """
        Main extraction logic.
        
        Args:
            urls: List of URLs to process
            args: Parsed command line arguments
            
        Returns:
            List of extracted modules
        """
        if not args.quiet:
            print(f"🚀 Starting module extraction for {len(urls)} URL(s)")
        
        try:
            # Initialize components
            scraper = WebScraper(
                delay=args.delay,
                max_depth=args.max_depth,
                max_pages=args.max_pages
            )
            
            processor = ContentProcessor()
            
            # Configure AI extractor
            openai_key = args.openai_key or os.getenv('OPENAI_API_KEY')
            if args.no_ai:
                openai_key = None
            
            extractor = AIModuleExtractor(api_key=openai_key)
            
            # Step 1: Scrape websites
            if not args.quiet:
                print("🔍 Scraping websites...")
            
            scraped_pages = scraper.crawl_website(urls)
            
            if not scraped_pages:
                self.logger.error("No content could be extracted from the provided URLs")
                return []
            
            if not args.quiet:
                print(f"📄 Successfully scraped {len(scraped_pages)} pages")
            
            # Step 2: Process content
            if not args.quiet:
                print("⚙️ Processing content and identifying structure...")
            
            processed_content = processor.process_pages(scraped_pages)
            
            if not args.quiet:
                print(f"🗂️ Identified {len(processed_content)} potential modules")
            
            # Step 3: Extract modules with AI
            if not args.quiet:
                ai_status = "AI-powered" if openai_key else "rule-based"
                print(f"🤖 Extracting modules using {ai_status} analysis...")
            
            extracted_modules = extractor.extract_modules(processed_content)
            validated_modules = extractor.validate_output_format(extracted_modules)
            
            if not args.quiet:
                total_submodules = sum(len(module.get('Submodules', {})) for module in validated_modules)
                print(f"✅ Extraction completed!")
                print(f"📊 Results: {len(validated_modules)} modules, {total_submodules} submodules")
            
            return validated_modules
            
        except Exception as e:
            self.logger.error(f"Error during extraction: {e}")
            if args.verbose:
                import traceback
                self.logger.error(traceback.format_exc())
            return []
    
    def save_results(self, results: List[dict], output_path: str, pretty: bool = False) -> bool:
        """
        Save results to JSON file.
        
        Args:
            results: Extracted modules
            output_path: Output file path
            pretty: Whether to format JSON nicely
            
        Returns:
            True if saved successfully
        """
        try:
            indent = 2 if pretty else None
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=indent, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving results to {output_path}: {e}")
            return False
    
    def print_results_summary(self, results: List[dict]):
        """Print a summary of the extraction results."""
        if not results:
            print("No modules extracted.")
            return
        
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        
        for i, module in enumerate(results, 1):
            print(f"\n{i}. Module: {module['module']}")
            print(f"   Description: {module['Description'][:100]}...")
            
            submodules = module.get('Submodules', {})
            if submodules:
                print(f"   Submodules ({len(submodules)}):")
                for sub_name in list(submodules.keys())[:3]:  # Show first 3
                    print(f"     • {sub_name}")
                if len(submodules) > 3:
                    print(f"     ... and {len(submodules) - 3} more")
        
        print("\n" + "="*60)
    
    def run(self):
        """Main CLI runner."""
        # Parse arguments
        args = self.parse_arguments()
        
        # Configure logging based on verbosity
        if args.verbose:
            self.setup_logging(verbose=True)
        elif args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        
        # Get URLs
        if args.urls:
            urls = args.urls
        else:
            urls = self.read_urls_from_file(args.file)
        
        if not urls:
            self.logger.error("No URLs provided or file is empty")
            sys.exit(1)
        
        # Validate URLs
        valid_urls = self.validate_urls(urls)
        
        if not valid_urls:
            self.logger.error("No valid URLs found")
            sys.exit(1)
        
        if len(valid_urls) < len(urls):
            self.logger.warning(f"Only {len(valid_urls)} of {len(urls)} URLs are valid")
        
        # Extract modules
        results = self.extract_modules(valid_urls, args)
        
        if not results:
            self.logger.error("No modules could be extracted")
            sys.exit(1)
        
        # Save results
        output_path = self.create_output_path(args.output)
        
        if self.save_results(results, output_path, args.pretty):
            if not args.quiet:
                print(f"💾 Results saved to: {output_path}")
        else:
            self.logger.error("Failed to save results")
            sys.exit(1)
        
        # Print results if requested
        if args.pretty and not args.quiet:
            self.print_results_summary(results)
        
        # Print JSON to console if no output file specified and pretty is True
        if args.pretty:
            print("\nJSON Output:")
            print(json.dumps(results, indent=2, ensure_ascii=False))

def main():
    """Main entry point."""
    cli = ModuleExtractorCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()