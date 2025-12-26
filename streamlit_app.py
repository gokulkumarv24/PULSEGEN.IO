"""
Streamlit web interface for the Module Extraction AI Agent.
Provides a user-friendly interface for URL input and JSON output display.
"""

import streamlit as st
import json
import sys
import os
from datetime import datetime
import validators
import traceback

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from web_scraper import WebScraper
    from content_processor import ContentProcessor
    from ai_extractor import AIModuleExtractor
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

class StreamlitApp:
    def __init__(self):
        """Initialize the Streamlit application."""
        self.setup_page_config()
        self.setup_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Module Extraction AI Agent",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def setup_session_state(self):
        """Initialize session state variables."""
        if 'extraction_results' not in st.session_state:
            st.session_state.extraction_results = None
        if 'processing_status' not in st.session_state:
            st.session_state.processing_status = None
        if 'scraped_pages' not in st.session_state:
            st.session_state.scraped_pages = []
    
    def render_header(self):
        """Render the application header."""
        st.title("🤖 Module Extraction AI Agent")
        st.markdown("""
        **Extract structured information from documentation websites**
        
        This tool analyzes help documentation websites and identifies key modules and submodules 
        with detailed descriptions based on the content structure.
        """)
        st.divider()
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Scraping settings
            st.subheader("Scraping Settings")
            delay = st.slider("Delay between requests (seconds)", 0.5, 5.0, 1.0, 0.5)
            max_pages = st.slider("Maximum pages to scrape", 10, 100, 30, 5)
            max_depth = st.slider("Maximum crawling depth", 1, 5, 2, 1)
            
            # AI settings
            st.subheader("AI Settings")
            use_openai = st.checkbox("Use OpenAI API (requires API key)", value=False)
            openai_key = ""
            if use_openai:
                openai_key = st.text_input("OpenAI API Key", type="password", 
                                         help="Enter your OpenAI API key")
            
            return {
                'delay': delay,
                'max_pages': max_pages,
                'max_depth': max_depth,
                'use_openai': use_openai,
                'openai_key': openai_key
            }
    
    def render_input_section(self):
        """Render the URL input section."""
        st.header("📝 Input URLs")
        
        # URL input methods
        input_method = st.radio(
            "Choose input method:",
            ("Single URL", "Multiple URLs", "Upload URL list"),
            horizontal=True
        )
        
        urls = []
        
        if input_method == "Single URL":
            url = st.text_input(
                "Enter documentation URL:",
                placeholder="https://help.example.com",
                help="Enter a single documentation website URL"
            )
            if url:
                urls = [url]
        
        elif input_method == "Multiple URLs":
            url_text = st.text_area(
                "Enter URLs (one per line):",
                placeholder="https://help.example.com\nhttps://docs.example.com",
                height=150
            )
            if url_text:
                urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        else:  # Upload URL list
            uploaded_file = st.file_uploader(
                "Upload URL list (.txt file)",
                type=['txt'],
                help="Upload a text file with URLs, one per line"
            )
            if uploaded_file:
                urls = [url.strip() for url in uploaded_file.read().decode().split('\n') if url.strip()]
        
        # Validate URLs
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if validators.url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if invalid_urls:
            st.warning(f"Invalid URLs detected: {', '.join(invalid_urls)}")
        
        if valid_urls:
            st.success(f"Valid URLs: {len(valid_urls)}")
            with st.expander("View URLs"):
                for url in valid_urls:
                    st.write(f"• {url}")
        
        return valid_urls
    
    def render_processing_section(self, urls, config):
        """Render the processing section with start button."""
        st.header("🚀 Processing")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            start_processing = st.button(
                "Start Extraction",
                disabled=not urls,
                type="primary",
                use_container_width=True
            )
        
        with col2:
            if st.session_state.extraction_results:
                st.download_button(
                    "Download JSON",
                    data=json.dumps(st.session_state.extraction_results, indent=2),
                    file_name=f"modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col3:
            if st.button("Clear Results", use_container_width=True):
                st.session_state.extraction_results = None
                st.session_state.processing_status = None
                st.session_state.scraped_pages = []
                st.rerun()
        
        if start_processing and urls:
            self.process_urls(urls, config)
    
    def process_urls(self, urls, config):
        """Process URLs and extract modules."""
        try:
            st.session_state.processing_status = "Starting..."
            
            # Initialize components
            scraper = WebScraper(
                delay=config['delay'],
                max_depth=config['max_depth'],
                max_pages=config['max_pages']
            )
            
            processor = ContentProcessor()
            
            extractor = AIModuleExtractor(
                api_key=config['openai_key'] if config['use_openai'] else None
            )
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Web scraping
            status_text.text("🔍 Scraping websites...")
            progress_bar.progress(10)
            
            scraped_pages = scraper.crawl_website(urls)
            st.session_state.scraped_pages = scraped_pages
            
            if not scraped_pages:
                st.error("No content could be extracted from the provided URLs.")
                return
            
            progress_bar.progress(40)
            status_text.text(f"📄 Found {len(scraped_pages)} pages")
            
            # Step 2: Content processing
            status_text.text("⚙️ Processing content...")
            progress_bar.progress(60)
            
            processed_content = processor.process_pages(scraped_pages)
            
            progress_bar.progress(80)
            status_text.text("🤖 Extracting modules with AI...")
            
            # Step 3: AI extraction
            extracted_modules = extractor.extract_modules(processed_content)
            validated_modules = extractor.validate_output_format(extracted_modules)
            
            progress_bar.progress(100)
            status_text.text("✅ Extraction completed!")
            
            # Store results
            st.session_state.extraction_results = validated_modules
            st.session_state.processing_status = "completed"
            
            # Auto-refresh to show results
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
            st.error("Full error traceback:")
            st.code(traceback.format_exc())
            st.session_state.processing_status = "error"
    
    def render_results_section(self):
        """Render the results section."""
        if st.session_state.extraction_results:
            st.header("📊 Extraction Results")
            
            results = st.session_state.extraction_results
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Modules", len(results))
            
            with col2:
                total_submodules = sum(len(module.get('Submodules', {})) for module in results)
                st.metric("Total Submodules", total_submodules)
            
            with col3:
                st.metric("Pages Processed", len(st.session_state.scraped_pages))
            
            with col4:
                avg_submodules = total_submodules / len(results) if results else 0
                st.metric("Avg Submodules/Module", f"{avg_submodules:.1f}")
            
            # Display options
            display_format = st.radio(
                "Display format:",
                ("Structured View", "JSON View", "Table View"),
                horizontal=True
            )
            
            if display_format == "Structured View":
                self.render_structured_results(results)
            elif display_format == "JSON View":
                st.code(json.dumps(results, indent=2), language='json')
            else:
                self.render_table_results(results)
    
    def render_structured_results(self, results):
        """Render results in a structured, user-friendly format."""
        for i, module in enumerate(results):
            with st.expander(f"📁 {module['module']}", expanded=i < 3):
                st.write(f"**Description:** {module['Description']}")
                
                submodules = module.get('Submodules', {})
                if submodules:
                    st.write(f"**Submodules ({len(submodules)}):**")
                    for sub_name, sub_desc in submodules.items():
                        st.write(f"• **{sub_name}:** {sub_desc}")
                else:
                    st.write("*No submodules identified*")
    
    def render_table_results(self, results):
        """Render results in table format."""
        import pandas as pd
        
        # Create table data
        table_data = []
        for module in results:
            submodules = module.get('Submodules', {})
            if submodules:
                for sub_name, sub_desc in submodules.items():
                    table_data.append({
                        'Module': module['module'],
                        'Module Description': module['Description'],
                        'Submodule': sub_name,
                        'Submodule Description': sub_desc
                    })
            else:
                table_data.append({
                    'Module': module['module'],
                    'Module Description': module['Description'],
                    'Submodule': 'N/A',
                    'Submodule Description': 'N/A'
                })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)
    
    def render_debug_section(self):
        """Render debug information section."""
        if st.session_state.scraped_pages:
            with st.expander("🔧 Debug Information"):
                st.subheader("Scraped Pages")
                for i, page in enumerate(st.session_state.scraped_pages[:5]):  # Show first 5
                    st.write(f"**Page {i+1}:** {page.get('title', 'No title')}")
                    st.write(f"URL: {page.get('url', 'No URL')}")
                    st.write(f"Content length: {len(page.get('content', ''))} characters")
                    if page.get('content'):
                        st.text_area(
                            f"Content preview {i+1}",
                            page['content'][:300] + "..." if len(page['content']) > 300 else page['content'],
                            height=100,
                            key=f"content_{i}"
                        )
                    st.divider()
    
    def run(self):
        """Main application runner."""
        self.render_header()
        
        # Get configuration from sidebar
        config = self.render_sidebar()
        
        # Main content
        urls = self.render_input_section()
        
        self.render_processing_section(urls, config)
        
        self.render_results_section()
        
        self.render_debug_section()
        
        # Footer
        st.divider()
        st.markdown("""
        **Module Extraction AI Agent** - Built for analyzing documentation websites
        and extracting structured module information using AI and NLP techniques.
        """)

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()