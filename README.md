# AI-Powered Misinformation Filter & Verifier

An AI-powered tool that verifies news claims against reliable sources and helps combat misinformation.

## Features

- **AI Analysis**: Analyzes claims and detects potential misinformation patterns
- **Fact-Checking Integration**: Automatically searches for related fact-checks from reliable sources
- **Confidence Scoring**: Provides a confidence score for how likely a claim is to be true or false
- **Topic-Specific Verification**: Tailored verification approach based on claim topic (health, politics, etc.)
- **User-Friendly Interface**: Simple interface for submitting claims and reviewing results

## How It Works

1. **Submit a Claim**: Enter a claim or paste an article for verification
2. **AI Analysis**: Our system analyzes language patterns and content to detect potential misinformation
3. **Fact-Check Search**: The system searches for related fact-checks from trusted sources
4. **Verification Results**: Review the AI analysis and fact-checking sources in an easy-to-understand format

## Technologies Used

- **Backend**: Python, Flask
- **Database**: SQLAlchemy, SQLite
- **AI/ML**: Pattern matching, NLP techniques
- **Web Scraping**: Trafilatura for content extraction
- **Frontend**: HTML, CSS (Bootstrap), JavaScript

## Getting Started

### Prerequisites

- Python 3.10+
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/misinformation-filter.git
   cd misinformation-filter
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the application
   ```
   python main.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Future Development

- Blockchain record of verification
- Multilingual support
- Browser extension
- User feedback mechanism
- Enhanced AI capabilities

## License

MIT License