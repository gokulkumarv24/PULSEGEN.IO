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
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Add custom CSS for enhanced styling and animations
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        /* Global Styles */
        .main {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        /* Custom Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102,126,234,0.4);
        }
        
        /* Progress Bar Styling */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Expander Styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            border: 1px solid #dee2e6;
        }
        
        /* Metric Cards Enhancement */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid #e9ecef;
        }
        
        /* Code Block Styling */
        .stCodeBlock {
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }
        
        /* Text Input Styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e9ecef;
            font-family: 'Poppins', sans-serif;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.25);
        }
        
        /* Text Area Styling */
        .stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 2px solid #e9ecef;
            font-family: 'Poppins', sans-serif;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.25);
        }
        
        /* File Uploader Styling */
        .stFileUploader {
            border-radius: 10px;
        }
        
        /* Radio Button Styling */
        .stRadio > div {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        /* Success/Error Message Styling */
        .stAlert {
            border-radius: 10px;
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
        # Create an attractive header with gradient background effect
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <h1 style="
                color: white;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">🤖 PULSEGEN.IO</h1>
            <h2 style="
                color: #f0f0f0;
                font-size: 1.5rem;
                margin-bottom: 1rem;
                font-weight: 300;
            ">Module Extraction AI Agent</h2>
            <p style="
                color: #e0e0e0;
                font-size: 1.1rem;
                margin: 0;
                max-width: 800px;
                margin: 0 auto;
                line-height: 1.6;
            ">
                🚀 Extract structured information from documentation websites using advanced AI
                <br>
                ✨ Analyze help documentation and identify key modules with intelligent descriptions
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add feature highlights
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 0.5rem 0;">
                <h3 style="color: #667eea; margin: 0;">🔍</h3>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600;">Smart Crawling</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 0.5rem 0;">
                <h3 style="color: #667eea; margin: 0;">🤖</h3>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600;">AI Analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 0.5rem 0;">
                <h3 style="color: #667eea; margin: 0;">📊</h3>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600;">Structured Output</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin: 0.5rem 0;">
                <h3 style="color: #667eea; margin: 0;">⚡</h3>
                <p style="margin: 0.5rem 0 0 0; font-weight: 600;">Real-time Results</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            # Attractive sidebar header
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 1.5rem;
                text-align: center;
            ">
                <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚙️ Configuration</h2>
                <p style="color: #e0e0e0; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Customize your extraction</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Scraping settings with enhanced styling
            st.markdown("""
            <div style="
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0 0 1rem 0; color: #333; font-size: 1.1rem;">🔍 Scraping Settings</h3>
            </div>
            """, unsafe_allow_html=True)
            
            delay = st.slider("⏱️ Delay between requests", 0.5, 5.0, 1.0, 0.5, 
                            help="Respectful crawling delay in seconds")
            max_pages = st.slider("📄 Maximum pages to scrape", 10, 100, 30, 5,
                               help="Limit the number of pages to process")
            max_depth = st.slider("🌊 Maximum crawling depth", 1, 5, 2, 1,
                                help="How deep to follow links from the starting URL")
            
            # AI settings with enhanced styling
            st.markdown("""
            <div style="
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #764ba2;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0 0 1rem 0; color: #333; font-size: 1.1rem;">🤖 AI Settings</h3>
            </div>
            """, unsafe_allow_html=True)
            
            use_openai = st.checkbox("✨ Use OpenAI API (Enhanced Results)", value=False,
                                   help="Enable AI-powered analysis with OpenAI GPT")
            openai_key = ""
            if use_openai:
                openai_key = st.text_input("🔑 OpenAI API Key", type="password", 
                                         help="Enter your OpenAI API key for enhanced analysis")
                st.info("💡 **Tip**: The system works great even without an API key using intelligent fallback methods!")
            else:
                st.success("🎯 **Fallback Mode**: Uses advanced rule-based extraction - no API key needed!")
            
            # Performance info
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
            ">
                <h4 style="margin: 0 0 0.5rem 0; color: #8b4513;">📊 Performance Tips</h4>
                <ul style="margin: 0; padding-left: 1.2rem; color: #8b4513; font-size: 0.9rem;">
                    <li>Lower delay = faster crawling</li>
                    <li>Higher depth = more comprehensive</li>
                    <li>OpenAI API = better descriptions</li>
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
        # Attractive section header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        ">
            <h2 style="margin: 0 0 0.5rem 0; color: #2c3e50; font-size: 1.8rem;">📝 Input URLs</h2>
            <p style="margin: 0; color: #34495e; font-size: 1rem;">Add documentation websites to analyze</p>
        </div>
        """, unsafe_allow_html=True)
        
        # URL input methods with enhanced styling
        st.markdown("### 🎯 Choose Input Method")
        input_method = st.radio(
            "Choose how you want to provide URLs for analysis",
            ("🔗 Single URL", "📚 Multiple URLs", "📁 Upload URL list"),
            horizontal=True,
            help="Select how you want to provide URLs for analysis",
            label_visibility="collapsed"
        )
        
        urls = []
        
        if input_method == "🔗 Single URL":
            st.markdown("#### Enter Documentation URL")
            url = st.text_input(
                "Enter documentation URL",
                placeholder="https://help.example.com or https://docs.example.com",
                help="Enter a single documentation website URL",
                label_visibility="collapsed"
            )
            if url:
                urls = [url]
                
        elif input_method == "📚 Multiple URLs":
            st.markdown("#### Enter Multiple URLs")
            url_text = st.text_area(
                "Enter multiple URLs",
                placeholder="https://help.example.com\nhttps://docs.example.com\nhttps://support.example.com",
                height=150,
                help="Enter URLs one per line",
                label_visibility="collapsed"
            )
            if url_text:
                urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        else:  # Upload URL list
            st.markdown("#### Upload URL List File")
            uploaded_file = st.file_uploader(
                "Upload URL list file",
                type=['txt'],
                help="Upload a text file with URLs, one per line",
                label_visibility="collapsed"
            )
            if uploaded_file:
                urls = [url.strip() for url in uploaded_file.read().decode().split('\n') if url.strip()]
        
        # Enhanced URL validation with better visual feedback
        if urls:
            valid_urls = []
            invalid_urls = []
            
            for url in urls:
                if validators.url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            
            # Show validation results with attractive styling
            col1, col2 = st.columns(2)
            
            with col1:
                if valid_urls:
                    st.markdown(f"""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        border-radius: 8px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="color: #155724; margin: 0 0 0.5rem 0;">✅ Valid URLs ({len(valid_urls)})</h4>
                        <p style="color: #155724; margin: 0; font-size: 0.9rem;">Ready for processing!</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if invalid_urls:
                    st.markdown(f"""
                    <div style="
                        background: #f8d7da;
                        border: 1px solid #f5c6cb;
                        border-radius: 8px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="color: #721c24; margin: 0 0 0.5rem 0;">❌ Invalid URLs ({len(invalid_urls)})</h4>
                        <p style="color: #721c24; margin: 0; font-size: 0.9rem;">Please check format</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show URL list in an attractive format
            if valid_urls:
                with st.expander(f"👀 View URLs ({len(valid_urls)} valid)", expanded=False):
                    for i, url in enumerate(valid_urls, 1):
                        st.markdown(f"""
                        <div style="
                            background: #f8f9fa;
                            border-left: 3px solid #667eea;
                            padding: 0.5rem 1rem;
                            margin: 0.2rem 0;
                            border-radius: 0 5px 5px 0;
                        ">
                            <strong>{i}.</strong> <a href="{url}" target="_blank" style="color: #667eea; text-decoration: none;">{url}</a>
                        </div>
                        """, unsafe_allow_html=True)
        
        return valid_urls if 'valid_urls' in locals() else []
    
    def render_processing_section(self, urls, config):
        """Render the processing section with start button."""
        # Attractive processing section header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
            <h2 style="margin: 0 0 0.5rem 0; color: white; font-size: 1.8rem;">🚀 Processing Center</h2>
            <p style="margin: 0; color: #e0e0e0; font-size: 1rem;">Start extraction or manage results</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # Custom styled start button
            if urls:
                start_processing = st.button(
                    "🚀 Start Extraction",
                    type="primary",
                    width='stretch',
                    help="Begin analyzing the provided URLs"
                )
            else:
                st.markdown("""
                <div style="
                    background: #e9ecef;
                    color: #6c757d;
                    padding: 0.75rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px dashed #ced4da;
                ">
                    <strong>🚀 Start Extraction</strong><br>
                    <small>Add URLs first</small>
                </div>
                """, unsafe_allow_html=True)
                start_processing = False
        
        with col2:
            if st.session_state.extraction_results:
                # Enhanced download button
                download_data = json.dumps(st.session_state.extraction_results, indent=2)
                filename = f"pulsegen_modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button(
                    "💾 Download JSON",
                    data=download_data,
                    file_name=filename,
                    mime="application/json",
                    width='stretch',
                    help="Download extraction results as JSON file"
                )
            else:
                st.markdown("""
                <div style="
                    background: #e9ecef;
                    color: #6c757d;
                    padding: 0.75rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px dashed #ced4da;
                ">
                    <strong>💾 Download JSON</strong><br>
                    <small>No results yet</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if st.session_state.extraction_results or st.session_state.scraped_pages:
                clear_results = st.button(
                    "🗑️ Clear Results", 
                    width='stretch',
                    help="Clear all results and start fresh"
                )
                if clear_results:
                    st.session_state.extraction_results = None
                    st.session_state.processing_status = None
                    st.session_state.scraped_pages = []
                    st.success("✅ Results cleared!")
                    st.rerun()
            else:
                st.markdown("""
                <div style="
                    background: #e9ecef;
                    color: #6c757d;
                    padding: 0.75rem;
                    border-radius: 8px;
                    text-align: center;
                    border: 2px dashed #ced4da;
                ">
                    <strong>🗑️ Clear Results</strong><br>
                    <small>Nothing to clear</small>
                </div>
                """, unsafe_allow_html=True)
        
        if start_processing and urls:
            self.process_urls(urls, config)
    
    def process_urls(self, urls, config):
        """Process URLs and extract modules."""
        try:
            st.session_state.processing_status = "Starting..."
            
            # Enhanced processing display with animations
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                text-align: center;
                animation: pulse 2s infinite;
            ">
                <h3 style="color: white; margin: 0;">🔄 Processing in Progress</h3>
                <p style="color: #f0f0f0; margin: 0.5rem 0 0 0;">AI agents are analyzing your URLs...</p>
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
                        border-left: 4px solid #2196f3;
                        padding: 1rem;
                        border-radius: 0 8px 8px 0;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0; color: #1976d2;">🔍 Step 1: Web Scraping</h4>
                        <p style="margin: 0.5rem 0 0 0; color: #1976d2;">Crawling documentation websites...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                progress_bar.progress(10)
                
                scraped_pages = scraper.crawl_website(urls)
                st.session_state.scraped_pages = scraped_pages
                
                if not scraped_pages:
                    st.error("❌ No content could be extracted from the provided URLs.")
                    return
                
                progress_bar.progress(40)
                
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="
                        background: #f3e5f5;
                        border-left: 4px solid #9c27b0;
                        padding: 1rem;
                        border-radius: 0 8px 8px 0;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0; color: #7b1fa2;">📄 Step 2: Content Analysis</h4>
                        <p style="margin: 0.5rem 0 0 0; color: #7b1fa2;">Found {len(scraped_pages)} pages, analyzing content structure...</p>
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
                        border-left: 4px solid #4caf50;
                        padding: 1rem;
                        border-radius: 0 8px 8px 0;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0; color: #388e3c;">🤖 Step 3: AI Module Extraction</h4>
                        <p style="margin: 0.5rem 0 0 0; color: #388e3c;">Using {ai_mode} analysis to extract modules...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Step 3: AI extraction
                extracted_modules = extractor.extract_modules(processed_content)
                validated_modules = extractor.validate_output_format(extracted_modules)
                
                progress_bar.progress(100)
                
                # Success message with animation
                status_placeholder.markdown("""
                <div style="
                    background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(76,175,80,0.3);
                    animation: fadeIn 0.5s ease-in;
                ">
                    <h3 style="margin: 0 0 0.5rem 0;">✅ Extraction Completed Successfully!</h3>
                    <p style="margin: 0; opacity: 0.9;">Your modules have been extracted and are ready for review</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Store results
            st.session_state.extraction_results = validated_modules
            st.session_state.processing_status = "completed"
            
            # Auto-refresh to show results
            st.balloons()  # Celebratory animation!
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
                <h4 style="color: #d32f2f; margin: 0 0 0.5rem 0;">❌ Processing Error</h4>
                <p style="color: #d32f2f; margin: 0;">An error occurred during processing. Please check the details below and try again.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 Error Details", expanded=True):
                st.error(f"Error: {str(e)}")
                st.code(traceback.format_exc(), language='python')
            
            st.session_state.processing_status = "error"
    
    def render_results_section(self):
        """Render the results section."""
        if st.session_state.extraction_results:
            # Attractive results header
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                padding: 2rem;
                border-radius: 20px;
                margin: 2rem 0;
                text-align: center;
                box-shadow: 0 8px 25px rgba(255,154,158,0.3);
            ">
                <h2 style="margin: 0 0 0.5rem 0; color: #2c3e50; font-size: 2rem;">📊 Extraction Results</h2>
                <p style="margin: 0; color: #34495e; font-size: 1.1rem;">AI-powered analysis complete! Review your structured modules below</p>
            </div>
            """, unsafe_allow_html=True)
            
            results = st.session_state.extraction_results
            
            # Enhanced summary metrics with attractive cards
            col1, col2, col3, col4 = st.columns(4)
            
            total_submodules = sum(len(module.get('Submodules', {})) for module in results)
            avg_submodules = total_submodules / len(results) if results else 0
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(102,126,234,0.3);
                ">
                    <h1 style="margin: 0; font-size: 2.5rem;">{len(results)}</h1>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Total Modules</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(240,147,251,0.3);
                ">
                    <h1 style="margin: 0; font-size: 2.5rem;">{total_submodules}</h1>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Total Submodules</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(79,172,254,0.3);
                ">
                    <h1 style="margin: 0; font-size: 2.5rem;">{len(st.session_state.scraped_pages)}</h1>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Pages Analyzed</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(67,233,123,0.3);
                ">
                    <h1 style="margin: 0; font-size: 2.5rem;">{avg_submodules:.1f}</h1>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Avg Sub/Module</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Enhanced display options
            st.markdown("### 🎨 Choose Display Format")
            display_format = st.radio(
                "Select display format for results",
                ("🎯 Structured View", "💻 JSON View", "📋 Table View"),
                horizontal=True,
                help="Select how you want to view the extracted modules",
                label_visibility="collapsed"
            )
            
            if display_format == "🎯 Structured View":
                self.render_structured_results(results)
            elif display_format == "💻 JSON View":
                st.markdown("#### 📄 Raw JSON Output")
                st.code(json.dumps(results, indent=2), language='json')
            else:
                st.markdown("#### 📊 Tabular Data View")
                self.render_table_results(results)
    
    def render_structured_results(self, results):
        """Render results in a structured, user-friendly format."""
        st.markdown("#### 🎯 Module Structure Analysis")
        
        for i, module in enumerate(results):
            # Create attractive module cards
            module_color = ["#667eea", "#f093fb", "#4facfe", "#43e97b", "#ff9a9e"][i % 5]
            
            with st.expander(f"📁 {module['module']}", expanded=i < 2):
                # Module header with custom styling
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {module_color}20 0%, {module_color}10 100%);
                    border-left: 4px solid {module_color};
                    padding: 1rem;
                    border-radius: 0 10px 10px 0;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">📋 Module Description</h4>
                    <p style="margin: 0; color: #34495e; font-size: 1rem; line-height: 1.6;">{module['Description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                submodules = module.get('Submodules', {})
                if submodules:
                    st.markdown(f"""
                    <div style="
                        background: #f8f9fa;
                        border-radius: 10px;
                        padding: 1rem;
                        margin-top: 1rem;
                    ">
                        <h4 style="margin: 0 0 1rem 0; color: #495057;">🔗 Submodules ({len(submodules)})</h4>
                    """, unsafe_allow_html=True)
                    
                    # Display submodules in a grid
                    sub_cols = st.columns(2)
                    for idx, (sub_name, sub_desc) in enumerate(submodules.items()):
                        with sub_cols[idx % 2]:
                            st.markdown(f"""
                            <div style="
                                background: white;
                                border: 1px solid #dee2e6;
                                border-radius: 8px;
                                padding: 1rem;
                                margin-bottom: 0.5rem;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            ">
                                <h5 style="margin: 0 0 0.5rem 0; color: {module_color};">🔹 {sub_name}</h5>
                                <p style="margin: 0; color: #6c757d; font-size: 0.9rem; line-height: 1.5;">{sub_desc}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 8px;
                        padding: 1rem;
                        margin-top: 1rem;
                        text-align: center;
                    ">
                        <p style="margin: 0; color: #856404;">📝 <em>No submodules identified for this module</em></p>
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
        
        # Enhanced Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin-top: 3rem;
            box-shadow: 0 8px 25px rgba(44,62,80,0.3);
        ">
            <h3 style="margin: 0 0 1rem 0; font-size: 1.5rem;">🤖 PULSEGEN.IO - Module Extraction AI Agent</h3>
            <p style="margin: 0 0 1rem 0; opacity: 0.9; font-size: 1rem;">
                Advanced AI-driven system for intelligent documentation analysis and structured data extraction
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
                <div style="text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #3498db;">🔍</h4>
                    <p style="margin: 0; font-size: 0.9rem;">Smart Web Crawling</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #e74c3c;">🤖</h4>
                    <p style="margin: 0; font-size: 0.9rem;">AI-Powered Analysis</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #f39c12;">📊</h4>
                    <p style="margin: 0; font-size: 0.9rem;">Structured Results</p>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #27ae60;">⚡</h4>
                    <p style="margin: 0; font-size: 0.9rem;">Real-time Processing</p>
                </div>
            </div>
            <hr style="border: none; height: 1px; background: rgba(255,255,255,0.2); margin: 1.5rem 0;">
            <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">
                Built with Python, OpenAI GPT, Streamlit • Powered by advanced NLP and ML techniques
            </p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()