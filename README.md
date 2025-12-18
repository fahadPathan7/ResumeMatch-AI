# ResumeMatch AI

An intelligent CV (Resume) matching system that automatically evaluates and scores CVs against job descriptions using Natural Language Processing (NLP) techniques. Built with Streamlit and Hugging Face models.

## Features

- **Multi-format Support**: Upload CVs in PDF, DOCX, or TXT format
- **AI-Powered Matching**: Uses Sentence-BERT models for semantic similarity
- **Detailed Analysis**: Get comprehensive score breakdowns and insights
- **Skills Analysis**: Identify matched and missing skills
- **Recommendations**: Receive actionable suggestions for CV improvement
- **Easy to Use**: Simple, intuitive web interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy language model (optional, for advanced NLP):
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically `http://localhost:8501`)

3. Upload your CV and enter/paste a job description

4. Click "Match CV" to get your results

### Using the Application

1. **Upload CV**: Use the file uploader to upload your CV (PDF, DOCX, or TXT)

2. **Enter Job Description**: 
   - Option 1: Paste the job description directly in the text area
   - Option 2: Upload a job description file

3. **Get Results**: Click the "Match CV" button to analyze your CV

4. **Review Results**:
   - Overall match score (0-100%)
   - Score breakdown by category
   - Skills analysis (matched and missing)
   - Personalized recommendations

## How It Works

1. **Document Parsing**: Extracts text from uploaded CV files
2. **Text Processing**: Cleans and structures the text, identifies sections
3. **Feature Extraction**: Extracts skills, experience, education, and keywords
4. **Embedding Generation**: Uses Sentence-BERT to create semantic embeddings
5. **Similarity Calculation**: Computes cosine similarity between CV and job description
6. **Scoring**: Calculates weighted match score based on multiple factors
7. **Analysis**: Provides detailed breakdown and recommendations

## Scoring Components

The final match score is calculated using weighted components:

- **Overall Similarity (40%)**: Semantic similarity between full texts
- **Skills Match (30%)**: Percentage of required skills found in CV
- **Experience Match (20%)**: Alignment of work experience
- **Education Match (10%)**: Education requirements alignment

## Model Information

This application uses the `sentence-transformers/all-MiniLM-L6-v2` model, which:
- Provides fast inference (~50ms per document)
- Offers good accuracy for semantic similarity
- Has a small model size (~80MB)
- Is free and open-source

## Project Structure

```
cv-reviewer/
├── PLAN/
│   └── initial-plan.md
├── src/
│   ├── parsers/          # Document parsers (PDF, DOCX, TXT)
│   ├── processors/       # Text processing and feature extraction
│   ├── models/           # Embedding and similarity models
│   ├── scoring/          # Scoring engine
│   └── utils/            # Helper functions
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore          # Git ignore file
```

## Future Enhancements

- Batch CV processing
- Custom scoring weights
- Export results to PDF/CSV
- History of previous matches
- Multi-language support
- ATS compatibility check