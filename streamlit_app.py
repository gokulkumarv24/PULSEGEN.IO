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
            page_title="PULSEGEN.IO - Module Extraction AI",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Add custom CSS for professional, classic styling
        st.markdown("""
        <style>
        /* Import Professional Typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');
        /* Import Font Awesome for professional icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Global Styles - Clean & Professional */
        .main {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #fdfdfd;
            color: #1a1a1a;
        }
        
        /* Professional Button Styles */
        .stButton > button {
            background: #2c3e50;
            border: 1px solid #34495e;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 0.6rem 1.5rem;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(44,62,80,0.12);
        }
        
        .stButton > button:hover {
            background: #34495e;
            border-color: #2c3e50;
            box-shadow: 0 2px 6px rgba(44,62,80,0.16);
        }
        
        .stButton > button:active {
            background: #1a252f;
            box-shadow: 0 1px 2px rgba(44,62,80,0.2);
        }
        
        /* Progress Bar - Minimal & Clean */
        .stProgress > div > div > div {
            background: #2c3e50;
            border-radius: 2px;
        }
        
        /* Sidebar - Professional Styling */
        .css-1d391kg {
            background: #f8f9fa;
            border-right: 1px solid #e9ecef;
        }
        
        /* Expander - Clean Design */
        .streamlit-expanderHeader {
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .streamlit-expanderHeader:hover {
            background: #f8f9fa;
            border-color: #dee2e6;
        }
        
        /* Cards - Subtle & Professional */
        [data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Code Blocks - Editor-style */
        .stCodeBlock {
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            background: #f6f8fa;
        }
        
        /* Form Elements - Professional */
        .stTextInput > div > div > input {
            border: 1px solid #d0d7de;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 0.5rem 0.75rem;
            background: #ffffff;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #2c3e50;
            box-shadow: 0 0 0 2px rgba(44,62,80,0.08);
            outline: none;
        }
        
        .stTextArea > div > div > textarea {
            border: 1px solid #d0d7de;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 0.75rem;
            background: #ffffff;
            line-height: 1.5;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #2c3e50;
            box-shadow: 0 0 0 2px rgba(44,62,80,0.08);
            outline: none;
        }
        
        /* Select Boxes */
        .stSelectbox > div > div {
            border: 1px solid #d0d7de;
            border-radius: 4px;
            background: #ffffff;
        }
        
        /* Radio Buttons - Clean */
        .stRadio > div {
            background: transparent;
            border: none;
            padding: 0;
        }
        
        /* File Uploader */
        .stFileUploader {
            border: 1px dashed #d0d7de;
            border-radius: 4px;
            background: #f6f8fa;
        }
        
        /* Alert Messages - Professional */
        .stAlert {
            border-radius: 4px;
            border: 1px solid;
            font-family: 'Inter', sans-serif;
        }
        
        .stAlert[data-baseweb="notification"] {
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Professional Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f3f4;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
        
        /* Typography Improvements */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Crimson Text', Georgia, serif;
            color: #1a1a1a;
            font-weight: 600;
        }
        
        /* Clean spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Professional Tables */
        .dataframe {
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 4px 4px 0 0;
            color: #586069;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: #ffffff;
            border-bottom-color: #ffffff;
            color: #1a1a1a;
        }
        </style>
        """, unsafe_allow_html=True)
    
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
        # Professional, clean header design
        st.markdown("""
        <div style="
            background: #ffffff;
            border-bottom: 2px solid #2c3e50;
            padding: 3rem 2rem 2rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <h1 style="
                color: #2c3e50;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 2.8rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
            ">PULSEGEN.IO</h1>
            <h2 style="
                color: #34495e;
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                font-weight: 400;
                margin-bottom: 1.5rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">Module Extraction AI Agent</h2>
            <p style="
                color: #7f8c8d;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                margin: 0 auto;
                max-width: 600px;
                line-height: 1.6;
            ">
                Extract structured information from documentation websites using advanced artificial intelligence.
                <br>Analyze help documentation and identify key modules with intelligent descriptions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean feature highlights
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 1.5rem 1rem; 
                background: #ffffff; 
                border: 1px solid #e9ecef; 
                border-radius: 4px;
                margin: 0.5rem 0;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.75rem; color: #2c3e50;">
                    <i class="fas fa-search"></i>
                </div>
                <h4 style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #2c3e50;">SMART CRAWLING</h4>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #7f8c8d;">Intelligent web scraping</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 1.5rem 1rem; 
                background: #ffffff; 
                border: 1px solid #e9ecef; 
                border-radius: 4px;
                margin: 0.5rem 0;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.75rem; color: #2c3e50;">
                    <i class="fas fa-brain"></i>
                </div>
                <h4 style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #2c3e50;">AI ANALYSIS</h4>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #7f8c8d;">Advanced language models</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 1.5rem 1rem; 
                background: #ffffff; 
                border: 1px solid #e9ecef; 
                border-radius: 4px;
                margin: 0.5rem 0;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.75rem; color: #2c3e50;">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <h4 style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #2c3e50;">STRUCTURED OUTPUT</h4>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #7f8c8d;">JSON format results</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 1.5rem 1rem; 
                background: #ffffff; 
                border: 1px solid #e9ecef; 
                border-radius: 4px;
                margin: 0.5rem 0;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.75rem; color: #2c3e50;">
                    <i class="fas fa-bolt"></i>
                </div>
                <h4 style="margin: 0; font-size: 0.9rem; font-weight: 600; color: #2c3e50;">REAL-TIME</h4>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #7f8c8d;">Instant processing</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            # Professional sidebar header
            st.markdown("""
            <div style="
                background: #2c3e50;
                color: #ffffff;
                padding: 1.5rem;
                margin: -1rem -1rem 2rem -1rem;
                text-align: center;
            ">
                <h3 style="
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.1rem;
                    font-weight: 600;
                    letter-spacing: 0.05em;
                ">CONFIGURATION</h3>
                <p style="
                    margin: 0.5rem 0 0 0;
                    font-size: 0.8rem;
                    opacity: 0.8;
                    font-weight: 400;
                ">Customize extraction settings</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Scraping settings section
            st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h4 style="
                    margin: 0 0 1rem 0;
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.9rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    border-bottom: 1px solid #e9ecef;
                    padding-bottom: 0.5rem;
                ">Web Scraping</h4>
            </div>
            """, unsafe_allow_html=True)
            
            delay = st.slider(
                "Request delay (seconds)", 
                0.5, 5.0, 1.0, 0.5, 
                help="Delay between HTTP requests for respectful crawling"
            )
            max_pages = st.slider(
                "Maximum pages", 
                10, 100, 30, 5,
                help="Limit the number of pages to process"
            )
            max_depth = st.slider(
                "Crawling depth", 
                1, 5, 2, 1,
                help="Maximum depth to follow links from starting URL"
            )
            
            # AI settings section
            st.markdown("""
            <div style="margin: 2rem 0 1.5rem 0;">
                <h4 style="
                    margin: 0 0 1rem 0;
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.9rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    border-bottom: 1px solid #e9ecef;
                    padding-bottom: 0.5rem;
                ">AI Processing</h4>
            </div>
            """, unsafe_allow_html=True)
            
            use_openai = st.checkbox(
                "Enable OpenAI API", 
                value=False,
                help="Use OpenAI GPT for enhanced analysis (optional)"
            )
            openai_key = ""
            if use_openai:
                openai_key = st.text_input(
                    "OpenAI API Key", 
                    type="password", 
                    help="Enter your OpenAI API key"
                )
                st.info("**Note**: Enhanced AI analysis with GPT models")
            else:
                st.success("**Default**: Advanced rule-based extraction (no API required)")
            
            # Performance information
            st.markdown("""
            <div style="
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 1rem;
                margin-top: 2rem;
            ">
                <h5 style="
                    margin: 0 0 0.75rem 0;
                    color: #495057;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">Performance Guidelines</h5>
                <ul style="
                    margin: 0;
                    padding-left: 1.2rem;
                    color: #6c757d;
                    font-size: 0.8rem;
                    line-height: 1.5;
                ">
                    <li>Lower delay = faster processing</li>
                    <li>Higher depth = more comprehensive analysis</li>
                    <li>OpenAI API = enhanced descriptions</li>
                    <li>Rule-based mode = consistent performance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            return {
                'delay': delay,
                'max_pages': max_pages,
                'max_depth': max_depth,
                'use_openai': use_openai,
                'openai_key': openai_key
            }
    
    def render_input_section(self):
        """Render the URL input section."""
        # Clean, professional section header
        st.markdown("""
        <div style="
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-left: 4px solid #2c3e50;
            padding: 2rem;
            margin: 2rem 0;
        ">
            <h2 style="
                margin: 0 0 0.5rem 0;
                color: #2c3e50;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.8rem;
                font-weight: 600;
            ">Input Documentation URLs</h2>
            <p style="
                margin: 0;
                color: #7f8c8d;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                line-height: 1.5;
            ">Provide documentation websites for intelligent module extraction and analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # URL input methods with clean styling
        st.markdown("### Input Method Selection")
        input_method = st.radio(
            "Choose how you want to provide URLs for analysis",
            ("Single URL", "Multiple URLs", "Upload URL List"),
            horizontal=True,
            help="Select the input method for providing documentation URLs"
        )
        
        urls = []
        
        if input_method == "Single URL":
            st.markdown("#### Documentation URL")
            url = st.text_input(
                "Enter documentation URL",
                placeholder="https://help.example.com or https://docs.example.com",
                help="Enter a single documentation website URL",
                label_visibility="collapsed"
            )
            if url:
                urls = [url]
                
        elif input_method == "Multiple URLs":
            st.markdown("#### Multiple Documentation URLs")
            url_text = st.text_area(
                "Enter multiple URLs",
                placeholder="https://help.example.com\nhttps://docs.example.com\nhttps://support.example.com",
                height=120,
                help="Enter URLs, one per line",
                label_visibility="collapsed"
            )
            if url_text:
                urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        else:  # Upload URL list
            st.markdown("#### Upload URL List")
            uploaded_file = st.file_uploader(
                "Upload URL list file",
                type=['txt'],
                help="Upload a text file containing URLs, one per line",
                label_visibility="collapsed"
            )
            if uploaded_file:
                urls = [url.strip() for url in uploaded_file.read().decode().split('\n') if url.strip()]
        
        # URL validation with clean presentation
        if urls:
            valid_urls = []
            invalid_urls = []
            
            for url in urls:
                if validators.url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            
            # Show validation results
            col1, col2 = st.columns(2)
            
            with col1:
                if valid_urls:
                    st.markdown(f"""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        border-radius: 4px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="color: #155724; margin: 0 0 0.25rem 0; font-size: 1rem;">
                            <i class="fas fa-check-circle"></i> Valid URLs ({len(valid_urls)})
                        </h4>
                        <p style="color: #155724; margin: 0; font-size: 0.9rem;">Ready for processing</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if invalid_urls:
                    st.markdown(f"""
                    <div style="
                        background: #f8d7da;
                        border: 1px solid #f5c6cb;
                        border-radius: 4px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="color: #721c24; margin: 0 0 0.25rem 0; font-size: 1rem;">
                            <i class="fas fa-exclamation-circle"></i> Invalid URLs ({len(invalid_urls)})
                        </h4>
                        <p style="color: #721c24; margin: 0; font-size: 0.9rem;">Please verify format</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show URL list in clean format
            if valid_urls:
                with st.expander(f"Review URLs ({len(valid_urls)} valid)", expanded=False):
                    for i, url in enumerate(valid_urls, 1):
                        st.markdown(f"""
                        <div style="
                            background: #ffffff;
                            border: 1px solid #e9ecef;
                            border-left: 3px solid #2c3e50;
                            padding: 0.75rem 1rem;
                            margin: 0.25rem 0;
                            font-family: 'Inter', sans-serif;
                        ">
                            <strong style="color: #2c3e50;">{i}.</strong> 
                            <a href="{url}" target="_blank" style="color: #2c3e50; text-decoration: none;">
                                {url}
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
        
        return valid_urls if 'valid_urls' in locals() else []
    
    def render_processing_section(self, urls, config):
        """Render the processing section with start button."""
        # Clean processing section header
        st.markdown("""
        <div style="
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-left: 4px solid #2c3e50;
            padding: 2rem;
            margin: 2rem 0;
        ">
            <h2 style="
                margin: 0 0 0.5rem 0;
                color: #2c3e50;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.8rem;
                font-weight: 600;
            ">Processing Center</h2>
            <p style="
                margin: 0;
                color: #7f8c8d;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
            ">Execute extraction or manage results</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if urls:
                start_processing = st.button(
                    "Start Extraction",
                    type="primary",
                    width='stretch',
                    help="Begin analyzing the provided URLs"
                )
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Start Extraction</strong><br>
                    <small>Add URLs first</small>
                </div>
                """, unsafe_allow_html=True)
                start_processing = False
        
        with col2:
            if st.session_state.extraction_results:
                download_data = json.dumps(st.session_state.extraction_results, indent=2)
                filename = f"pulsegen_modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button(
                    "Download JSON",
                    data=download_data,
                    file_name=filename,
                    mime="application/json",
                    width='stretch',
                    help="Download extraction results as JSON file"
                )
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Download JSON</strong><br>
                    <small>No results available</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if st.session_state.extraction_results or st.session_state.scraped_pages:
                clear_results = st.button(
                    "Clear Results", 
                    width='stretch',
                    help="Clear all results and start fresh"
                )
                if clear_results:
                    st.session_state.extraction_results = None
                    st.session_state.processing_status = None
                    st.session_state.scraped_pages = []
                    st.success("Results cleared successfully")
                    st.rerun()
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Clear Results</strong><br>
                    <small>Nothing to clear</small>
                </div>
                """, unsafe_allow_html=True)
        
        if start_processing and urls:
            self.process_urls(urls, config)
    
    def process_urls(self, urls, config):
        """Process URLs and extract modules."""
        try:
            st.session_state.processing_status = "Starting..."
            
            # Professional processing display
            st.markdown("""
            <div style="
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-left: 4px solid #2c3e50;
                padding: 1.5rem;
                margin: 1rem 0;
                text-align: center;
            ">
                <h3 style="color: #2c3e50; margin: 0 0 0.5rem 0; font-family: 'Inter', sans-serif;">
                    Processing in Progress
                </h3>
                <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">
                    Analyzing documentation URLs with AI agents...
                </p>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            # Enhanced progress tracking
            progress_container = st.container()
            
            with progress_container:
                # Custom progress bar
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                # Step 1: Web scraping
                with status_placeholder.container():
                    st.markdown("""
                    <div style="
                        background: #e3f2fd;
                        border: 1px solid #2196f3;
                        border-left: 4px solid #2196f3;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #1976d2; font-family: 'Inter', sans-serif;">
                            Step 1: Web Scraping
                        </h4>
                        <p style="margin: 0; color: #1976d2; font-size: 0.9rem;">
                            Crawling documentation websites...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                progress_bar.progress(10)
                
                scraped_pages = scraper.crawl_website(urls)
                st.session_state.scraped_pages = scraped_pages
                
                if not scraped_pages:
                    st.error("No content could be extracted from the provided URLs.")
                    return
                
                progress_bar.progress(40)
                
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="
                        background: #f3e5f5;
                        border: 1px solid #9c27b0;
                        border-left: 4px solid #9c27b0;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #7b1fa2; font-family: 'Inter', sans-serif;">
                            Step 2: Content Analysis
                        </h4>
                        <p style="margin: 0; color: #7b1fa2; font-size: 0.9rem;">
                            Found {len(scraped_pages)} pages, analyzing content structure...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Step 2: Content processing
                progress_bar.progress(60)
                processed_content = processor.process_pages(scraped_pages)
                
                progress_bar.progress(80)
                
                with status_placeholder.container():
                    ai_mode = "OpenAI GPT" if config['use_openai'] and config['openai_key'] else "Advanced Rule-based"
                    st.markdown(f"""
                    <div style="
                        background: #e8f5e8;
                        border: 1px solid #4caf50;
                        border-left: 4px solid #4caf50;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #388e3c; font-family: 'Inter', sans-serif;">
                            Step 3: AI Module Extraction
                        </h4>
                        <p style="margin: 0; color: #388e3c; font-size: 0.9rem;">
                            Using {ai_mode} analysis to extract modules...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Step 3: AI extraction
                extracted_modules = extractor.extract_modules(processed_content)
                validated_modules = extractor.validate_output_format(extracted_modules)
                
                progress_bar.progress(100)
                
                # Success message
                status_placeholder.markdown("""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-left: 4px solid #28a745;
                    padding: 1.5rem;
                    text-align: center;
                    color: #155724;
                    margin: 1rem 0;
                ">
                    <h3 style="margin: 0 0 0.5rem 0; font-family: 'Inter', sans-serif;">
                        Extraction Completed Successfully
                    </h3>
                    <p style="margin: 0; font-size: 0.9rem;">
                        Your modules have been extracted and are ready for review
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Store results
            st.session_state.extraction_results = validated_modules
            st.session_state.processing_status = "completed"
            
            # Auto-refresh to show results
            st.rerun()
            
        except Exception as e:
            st.markdown("""
            <div style="
                background: #ffebee;
                border: 1px solid #f44336;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            ">
                <h4 style="color: #d32f2f; margin: 0 0 0.5rem 0;">
                    <i class="fas fa-exclamation-triangle"></i> Processing Error
                </h4>
                <p style="color: #d32f2f; margin: 0;">An error occurred during processing. Please check the details below and try again.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Error Details", expanded=True):
                st.error(f"Error: {str(e)}")
                st.code(traceback.format_exc(), language='python')
            
            st.session_state.processing_status = "error"
    
    def render_results_section(self):
        """Render the results section."""
        if st.session_state.extraction_results:
            # Professional results header
            st.markdown("""
            <div style="
                background: #ffffff;
                border: 1px solid #e9ecef;
                border-left: 4px solid #2c3e50;
                padding: 2rem;
                margin: 2rem 0;
            ">
                <h2 style="
                    margin: 0 0 0.5rem 0;
                    color: #2c3e50;
                    font-family: 'Crimson Text', Georgia, serif;
                    font-size: 1.8rem;
                    font-weight: 600;
                ">Extraction Results</h2>
                <p style="
                    margin: 0;
                    color: #7f8c8d;
                    font-family: 'Inter', sans-serif;
                    font-size: 1rem;
                ">AI-powered analysis complete. Review your structured modules below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            results = st.session_state.extraction_results
            
            # Professional summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_submodules = sum(len(module.get('Submodules', {})) for module in results)
            avg_submodules = total_submodules / len(results) if results else 0
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {len(results)}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Total Modules
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {total_submodules}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Total Submodules
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {len(st.session_state.scraped_pages)}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Pages Analyzed
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {avg_submodules:.1f}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Avg Sub/Module
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display format selection
            st.markdown("### Display Format")
            display_format = st.radio(
                "Select display format for results",
                ("Structured View", "JSON View", "Table View"),
                horizontal=True,
                help="Choose how you want to view the extracted modules"
            )
            
            if display_format == "Structured View":
                self.render_structured_results(results)
            elif display_format == "JSON View":
                st.markdown("#### Raw JSON Output")
                st.code(json.dumps(results, indent=2), language='json')
            else:
                st.markdown("#### Tabular Data View")
                self.render_table_results(results)
    
    def render_structured_results(self, results):
        """Render results in a structured, user-friendly format."""
        st.markdown("#### Module Structure Analysis")
        
        for i, module in enumerate(results):
            # Professional module cards
            with st.expander(f"{module['module']}", expanded=i < 2):
                # Module description
                st.markdown(f"""
                <div style="
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-left: 4px solid #2c3e50;
                    padding: 1rem;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.75rem 0; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        Module Description
                    </h4>
                    <p style="
                        margin: 0;
                        color: #495057;
                        font-size: 1rem;
                        line-height: 1.6;
                        font-family: 'Inter', sans-serif;
                    ">{module['Description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                submodules = module.get('Submodules', {})
                if submodules:
                    st.markdown(f"""
                    <div style="
                        background: #ffffff;
                        border: 1px solid #e9ecef;
                        padding: 1rem;
                        margin-top: 1rem;
                    ">
                        <h4 style="
                            margin: 0 0 1rem 0;
                            color: #495057;
                            font-family: 'Inter', sans-serif;
                        ">Submodules ({len(submodules)})</h4>
                    """, unsafe_allow_html=True)
                    
                    # Display submodules in a clean grid
                    sub_cols = st.columns(2)
                    for idx, (sub_name, sub_desc) in enumerate(submodules.items()):
                        with sub_cols[idx % 2]:
                            st.markdown(f"""
                            <div style="
                                background: #ffffff;
                                border: 1px solid #dee2e6;
                                padding: 1rem;
                                margin-bottom: 0.75rem;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                            ">
                                <h5 style="
                                    margin: 0 0 0.5rem 0;
                                    color: #2c3e50;
                                    font-family: 'Inter', sans-serif;
                                    font-size: 0.95rem;
                                    font-weight: 600;
                                ">{sub_name}</h5>
                                <p style="
                                    margin: 0;
                                    color: #6c757d;
                                    font-size: 0.9rem;
                                    line-height: 1.5;
                                    font-family: 'Inter', sans-serif;
                                ">{sub_desc}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        padding: 1rem;
                        margin-top: 1rem;
                        text-align: center;
                    ">
                        <p style="
                            margin: 0;
                            color: #856404;
                            font-family: 'Inter', sans-serif;
                            font-style: italic;
                        ">No submodules identified for this module</p>
                    </div>
                    """, unsafe_allow_html=True)
    
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
            st.dataframe(df, width='stretch')
    
    def render_debug_section(self):
        """Render debug information section."""
        if st.session_state.scraped_pages:
            with st.expander("Debug Information"):
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
        
        # Enhanced Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: #2c3e50;
            color: #ffffff;
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 3rem;
            border-top: 1px solid #34495e;
        ">
            <h3 style="
                margin: 0 0 1rem 0;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.8rem;
                font-weight: 600;
                letter-spacing: -0.01em;
            ">PULSEGEN.IO</h3>
            <p style="
                margin: 0 0 2rem 0;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                opacity: 0.8;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            ">
                Advanced AI-driven system for intelligent documentation analysis and structured data extraction.
                Built with modern technologies for enterprise-grade performance.
            </p>
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 2rem;
                max-width: 800px;
                margin: 0 auto;
            ">
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-search"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Smart Crawling</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Intelligent web scraping</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">AI Analysis</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Advanced NLP processing</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-chart-bar"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Structured Data</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">JSON format output</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Real-time</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Instant processing</p>
                </div>
            </div>
            <hr style="
                border: none;
                height: 1px;
                background: #34495e;
                margin: 2rem auto;
                max-width: 600px;
            ">
            <p style="
                margin: 0;
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                opacity: 0.6;
                line-height: 1.5;
            ">
                Built with Python, OpenAI GPT, and Streamlit<br>
                Powered by advanced natural language processing and machine learning
            </p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()