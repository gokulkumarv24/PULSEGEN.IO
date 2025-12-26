# PULSEGEN.IO - Module Extraction AI Agent 🤖

[![Created by Gokul Kumar V](https://img.shields.io/badge/Created%20by-Gokul%20Kumar%20V-blue?style=for-the-badge&logo=github)](https://github.com/gokulkumarv24)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/gokul-kumar-v-236a24217)
[![AI Powered](https://img.shields.io/badge/AI%20Powered-OpenAI%20GPT-00A67E?style=for-the-badge&logo=openai)](https://openai.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python)](https://python.org)

A sophisticated AI-powered tool that extracts structured information from documentation websites. This tool automatically identifies key modules and submodules from help documentation and generates detailed descriptions based on the actual content.

**🚀 PULSEGEN.IO Project**: Advanced AI-driven module extraction system designed for intelligent documentation analysis and structured data extraction.

## � Video Demonstration

Watch the complete project demonstration and walkthrough:

[![Module Extraction AI Agent Demo](https://img.shields.io/badge/▶️_Watch_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](YOUR_GOOGLE_DRIVE_VIDEO_LINK_HERE)

> **📹 Video Overview**: This demonstration covers the complete functionality, technical architecture, live CLI and web interface demos, and real-world results. Perfect for understanding the project's capabilities and implementation details.

**🔗 Quick Access Options**:

- **Direct Link**: [Click here to watch the video demonstration](YOUR_GOOGLE_DRIVE_VIDEO_LINK_HERE)
- **Download**: Right-click the video link and select "Save link as" to download for offline viewing
- **Mobile Friendly**: The video is optimized for both desktop and mobile viewing

---

## �🌟 Features

- **Intelligent Web Scraping**: Automatically crawls documentation websites with respect for rate limits
- **AI-Powered Analysis**: Uses OpenAI GPT models for intelligent module identification and description generation
- **Fallback Rule-Based Extraction**: Works even without OpenAI API key using advanced pattern matching
- **Multiple Interfaces**: Both command-line and web-based Streamlit interface
- **Structured Output**: Clean JSON format matching the specified requirements
- **Flexible Input**: Support for single URLs, multiple URLs, or URL lists from files
- **Comprehensive Validation**: URL validation, content filtering, and output format validation

## 🎯 Use Cases

- **Product Documentation Analysis**: Extract feature modules from software documentation
- **Competitive Analysis**: Understand product structure from public documentation
- **Documentation Organization**: Restructure existing documentation based on identified modules
- **Feature Discovery**: Identify all features and capabilities of a product from its help docs

## 📁 Project Structure

```
module_extraction_ai/
├── src/
│   ├── web_scraper.py          # Web scraping and content extraction
│   ├── content_processor.py     # Content analysis and preprocessing
│   └── ai_extractor.py         # AI-powered module extraction
├── output/                     # Generated results
├── tests/                      # Test files
├── module_extractor.py         # Command-line interface
├── streamlit_app.py           # Web interface
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection for web scraping
- OpenAI API key (optional, for enhanced results)
- **Note**: Compatible with OpenAI API v1.0+ (uses latest Python client)

### Installation

1. **Clone or download this project**:

   ```bash
   cd module_extraction_ai
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key (optional)**:
   ```bash
   # Create a .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

### Basic Usage

#### Command Line Interface

Extract modules from a single URL:

```bash
python module_extractor.py --urls https://help.instagram.com
```

Extract from multiple URLs:

```bash
python module_extractor.py --urls https://support.neo.space/hc/en-us https://help.zluri.com/
```

Use a URL list file:

```bash
# Create a file with URLs (one per line)
echo "https://wordpress.org/documentation/" > urls.txt
echo "https://www.chargebee.com/docs/2.0/" >> urls.txt

python module_extractor.py --file urls.txt --output my_results.json
```

#### Web Interface

Launch the Streamlit web app:

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501` and use the user-friendly interface.

## 📚 Detailed Usage

### Command Line Options

```bash
python module_extractor.py --help
```

**URL Input Options** (choose one):

- `--urls URL1 URL2 ...` - Specify URLs directly
- `--file FILE` - Read URLs from a text file

**Output Options**:

- `--output PATH` - Output file path (default: output/modules_TIMESTAMP.json)
- `--pretty` - Pretty print JSON and show summary

**Scraping Configuration**:

- `--delay SECONDS` - Delay between requests (default: 1.0)
- `--max-pages NUM` - Maximum pages to scrape (default: 30)
- `--max-depth NUM` - Maximum crawling depth (default: 2)

**AI Configuration**:

- `--openai-key KEY` - OpenAI API key for enhanced extraction
- `--no-ai` - Use only rule-based extraction

**Logging**:

- `--verbose, -v` - Enable verbose logging
- `--quiet, -q` - Suppress output except errors

### Examples

**Basic extraction with pretty output**:

```bash
python module_extractor.py --urls https://help.instagram.com --pretty
```

**Fast extraction with minimal crawling**:

```bash
python module_extractor.py --urls https://help.example.com --max-depth 1 --max-pages 10
```

**Use OpenAI for better results**:

```bash
python module_extractor.py --urls https://help.example.com --openai-key sk-your-key-here
```

**Process multiple documentation sites**:

```bash
python module_extractor.py --urls \
  https://support.neo.space/hc/en-us \
  https://wordpress.org/documentation/ \
  https://help.zluri.com/ \
  https://www.chargebee.com/docs/2.0/ \
  --output comprehensive_analysis.json
```

## 📋 Output Format

The tool generates JSON output in the following format:

```json
[
  {
    "module": "Account Settings",
    "Description": "Features and tools for managing Instagram account preferences, privacy, and credentials.",
    "Submodules": {
      "Change Username": "Explains how to update your Instagram handle and display name via account settings.",
      "Privacy Controls": "Manage who can see your posts, stories, and personal information.",
      "Account Security": "Two-factor authentication, login alerts, and security settings."
    }
  },
  {
    "module": "Content Sharing",
    "Description": "Tools and workflows for creating, editing, and publishing content on Instagram.",
    "Submodules": {
      "Creating Reels": "Instructions for recording, editing, and sharing short-form video content.",
      "Tagging Users": "How to tag individuals or businesses in posts and stories.",
      "Story Features": "Advanced story features like polls, questions, and interactive elements."
    }
  }
]
```

## 🔧 Configuration

### Web Scraper Settings

- **Delay**: Time between HTTP requests (respect rate limits)
- **Max Pages**: Limit total pages scraped to avoid overwhelming servers
- **Max Depth**: How deep to crawl from the starting URLs
- **User Agent**: Identifies the scraper to web servers

### AI Extractor Settings

- **OpenAI Model**: Uses GPT-3.5-turbo for analysis (configurable)
- **Temperature**: Controls creativity in responses (set to 0.3 for consistency)
- **Max Tokens**: Limits response length to manage costs
- **Retry Logic**: Handles rate limits and API errors gracefully

### Content Processing

- **Content Filtering**: Removes navigation, ads, and non-content elements
- **Text Cleaning**: Normalizes whitespace and removes special characters
- **Hierarchy Detection**: Identifies headings and document structure
- **Module Grouping**: Groups related content under appropriate modules

## 🧪 Testing

Test the application with the provided B2B documentation URLs:

```bash
# Test with Neo
python module_extractor.py --urls https://support.neo.space/hc/en-us --pretty

# Test with WordPress
python module_extractor.py --urls https://wordpress.org/documentation/ --pretty

# Test with Zluri
python module_extractor.py --urls https://help.zluri.com/ --pretty

# Test with Chargebee
python module_extractor.py --urls https://www.chargebee.com/docs/2.0/ --pretty
```

### Creating Test Scripts

Create a test script to run multiple tests:

```bash
# Create test_urls.txt
echo "https://support.neo.space/hc/en-us" > test_urls.txt
echo "https://wordpress.org/documentation/" >> test_urls.txt
echo "https://help.zluri.com/" >> test_urls.txt
echo "https://www.chargebee.com/docs/2.0/" >> test_urls.txt

# Run comprehensive test
python module_extractor.py --file test_urls.txt --output test_results.json --verbose
```

## 🎨 Web Interface Features

Launch with: `streamlit run streamlit_app.py`

### Features:

- **URL Input Methods**: Single URL, multiple URLs, or file upload
- **Real-time Progress**: Progress bars and status updates
- **Multiple Views**: Structured view, JSON view, or table view
- **Configuration Panel**: Adjust scraping and AI settings
- **Download Results**: Export results as JSON
- **Debug Information**: View scraped pages and processing details

### Interface Sections:

1. **Configuration Sidebar**: Scraping settings and AI options
2. **Input Section**: URL input with validation
3. **Processing Section**: Start extraction with progress tracking
4. **Results Section**: Multiple viewing formats for results
5. **Debug Section**: Detailed information about the scraping process

## 🔍 How It Works

### 1. Web Scraping Phase

- Validates input URLs
- Crawls documentation sites following internal links
- Respects robots.txt and implements rate limiting
- Extracts meaningful content while filtering navigation/ads

### 2. Content Processing Phase

- Cleans and normalizes extracted text
- Identifies document structure and hierarchy
- Detects potential modules from headings and sections
- Groups related content logically

### 3. AI Analysis Phase (Optional)

- Uses OpenAI GPT models to analyze content structure
- Identifies semantically related topics
- Generates detailed, accurate descriptions
- Consolidates similar topics to avoid duplication

### 4. Fallback Rule-Based Phase

- Pattern matching for common documentation structures
- Keyword extraction and categorization
- Template-based description generation
- Ensures functionality without AI dependencies

## 🚨 Limitations & Considerations

### Technical Limitations

- **Rate Limiting**: Respects website rate limits (may be slow for large sites)
- **JavaScript Content**: Cannot process dynamically loaded content
- **Authentication**: Cannot access login-protected documentation
- **PDF/Non-HTML**: Only processes HTML content

### AI Dependencies

- **OpenAI Costs**: API calls incur costs (approximately $0.01-0.10 per site)
- **Rate Limits**: OpenAI has usage limits that may affect large batch processing
- **Fallback Quality**: Rule-based extraction is less accurate than AI-powered

### Content Quality

- **Site Structure**: Results quality depends on documentation organization
- **Content Volume**: Very sparse documentation may yield limited results
- **Language**: Optimized for English documentation

## 🔒 Security & Privacy

- **No Data Storage**: Scraped content is not permanently stored
- **API Key Security**: OpenAI keys should be kept confidential
- **Respectful Scraping**: Implements delays and respects robots.txt
- **Local Processing**: All processing happens locally except AI API calls

## 🐛 Troubleshooting

### Common Issues

**Import Errors**:

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Network Issues**:

```bash
# Test with a simple URL first
python module_extractor.py --urls https://help.instagram.com --verbose
```

**OpenAI API Issues**:

```bash
# Test without AI first
python module_extractor.py --urls https://help.example.com --no-ai
```

**Empty Results**:

- Check if the URL is accessible
- Try increasing max-pages and max-depth
- Enable verbose logging to see what's happening

### Debug Mode

Enable detailed logging:

```bash
python module_extractor.py --urls https://help.example.com --verbose
```

This will show:

- URLs being scraped
- Content extraction progress
- AI API interactions
- Error messages and stack traces

## 🤝 Contributing

This project follows best practices for code organization and documentation:

### Code Structure

- **Modular Design**: Separate modules for different functionalities
- **Error Handling**: Comprehensive error handling and logging
- **Type Hints**: Type annotations for better code clarity
- **Documentation**: Detailed docstrings and comments

### Areas for Enhancement

- Support for additional content formats (PDF, XML)
- Integration with other AI providers
- Enhanced content similarity detection
- Performance optimizations for large sites
- Multi-language documentation support

## 📄 License

This project is created for educational and evaluation purposes. Please ensure compliance with website terms of service when scraping documentation.

## �‍💻 Creator

**Created by: Gokul Kumar V**

- **GitHub**: [gokulkumarv24](https://github.com/gokulkumarv24)
- **LinkedIn**: [Gokul Kumar V](https://www.linkedin.com/in/gokul-kumar-v-236a24217)

> _Passionate about AI, Machine Learning, and Building Intelligent Solutions_

### About the Developer

Gokul Kumar V is the creator and lead developer of this Module Extraction AI Agent. With expertise in artificial intelligence, web development, and data processing, he's dedicated to building innovative solutions that bridge the gap between AI capabilities and real-world applications.

**Core Expertise**:

- AI & Machine Learning Integration
- Modern Web Application Development
- Natural Language Processing
- Intelligent Data Extraction Systems

For collaboration opportunities, technical discussions, or project inquiries, feel free to connect through the links above!

## �🙋‍♂️ Support

For issues or questions:

1. Check the troubleshooting section above
2. Enable verbose logging to diagnose issues
3. Test with the provided sample URLs first
4. Ensure all dependencies are properly installed
5. Reach out to the creator through GitHub or LinkedIn

---

**Module Extraction AI Agent** - Turning unstructured documentation into structured insights with the power of AI! 🚀

_Built with ❤️ by [Gokul Kumar V](https://github.com/gokulkumarv24)_
