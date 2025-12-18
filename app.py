"""
ResumeMatch AI - Streamlit Application
Main application file for CV matching against job descriptions
"""

import streamlit as st
import sys
import os

# Get the directory where app.py is located (works on both local and Streamlit Cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Remove BASE_DIR from path if it exists, then add it at the beginning
# This ensures it has highest priority for imports
if BASE_DIR in sys.path:
    sys.path.remove(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# Verify src directory structure
src_path = os.path.join(BASE_DIR, 'src')
if not os.path.exists(src_path):
    st.error(f"Error: 'src' directory not found at {src_path}")
    st.error(f"Base directory: {BASE_DIR}")
    st.error(f"Files in base directory: {os.listdir(BASE_DIR) if os.path.exists(BASE_DIR) else 'N/A'}")
    st.stop()

# Check for required subdirectories and provide helpful error if missing
required_dirs = ['models', 'utils', 'processors', 'scoring', 'parsers']
missing_dirs = []
for dir_name in required_dirs:
    dir_path = os.path.join(src_path, dir_name)
    if not os.path.exists(dir_path):
        missing_dirs.append(dir_name)

if missing_dirs:
    st.error("### Missing Required Directories")
    st.error(f"The following directories are missing from the deployment: {', '.join(missing_dirs)}")
    st.error("**This usually means these files weren't committed to git.**")
    st.error("**Files in src directory:**")
    try:
        src_files = os.listdir(src_path)
        st.code('\n'.join(src_files))
    except:
        st.error("Cannot list files")
    st.error("**Solution:**")
    st.markdown("""
    1. Ensure all files are committed to git:
       ```bash
       git add src/models/
       git commit -m "Add models directory"
       git push
       ```
    2. Verify `.gitignore` is not excluding these files
    3. Re-deploy on Streamlit Cloud
    """)
    st.stop()

# Import modules with detailed error handling
try:
    # Verify Python can find the module
    import importlib.util
    
    # Check if src can be found as a package
    src_spec = importlib.util.find_spec("src")
    if src_spec is None or src_spec.origin is None:
        st.error("Python cannot find 'src' package")
        st.error(f"BASE_DIR: {BASE_DIR}")
        st.error(f"Python path: {sys.path[:5]}")
        st.error(f"src directory exists: {os.path.exists(src_path)}")
        if os.path.exists(src_path):
            st.error(f"src/__init__.py exists: {os.path.exists(os.path.join(src_path, '__init__.py'))}")
        st.stop()
    
    # Now try the actual imports
    from src.utils.helpers import parse_document, get_file_type
    from src.processors.text_processor import TextProcessor
    from src.models.embedding_model import EmbeddingModel
    from src.models.similarity_calculator import SimilarityCalculator
    from src.scoring.score_engine import ScoreEngine
except ImportError as e:
    import traceback
    st.error("### Import Error")
    st.error(f"**Error**: {str(e)}")
    
    # Debug information
    debug_info = {
        "Base Directory": BASE_DIR,
        "Current Working Directory": os.getcwd(),
        "File Location": os.path.abspath(__file__),
        "Src Directory Exists": os.path.exists(os.path.join(BASE_DIR, 'src')),
        "Python Path (first 5)": sys.path[:5]
    }
    
    if os.path.exists(BASE_DIR):
        try:
            debug_info["Files in BASE_DIR"] = [f for f in os.listdir(BASE_DIR) if not f.startswith('.')]
        except:
            debug_info["Files in BASE_DIR"] = "Cannot list"
    
    st.error("**Debug Information:**")
    for key, value in debug_info.items():
        st.text(f"{key}: {value}")
    
    st.error("**Full Traceback:**")
    st.code(traceback.format_exc())
    st.error("**Troubleshooting:**")
    st.markdown("""
    1. Ensure `src/` directory exists in the project root
    2. Check that all `__init__.py` files are present
    3. Verify `requirements.txt` includes all dependencies
    4. On Streamlit Cloud, ensure the repository structure matches local structure
    """)
    st.stop()

# Page configuration
st.set_page_config(
    page_title="ResumeMatch AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'embedding_model' not in st.session_state:
    st.session_state.embedding_model = None
if 'similarity_calculator' not in st.session_state:
    st.session_state.similarity_calculator = None
if 'score_engine' not in st.session_state:
    st.session_state.score_engine = None


@st.cache_resource
def load_models():
    """Load and cache embedding model"""
    try:
        embedding_model = EmbeddingModel('sentence-transformers/all-MiniLM-L6-v2')
        similarity_calculator = SimilarityCalculator(embedding_model)
        score_engine = ScoreEngine(similarity_calculator)
        return embedding_model, similarity_calculator, score_engine
    except Exception as e:
        st.error(f"Failed to load models: {str(e)}")
        return None, None, None


def main():
    """Main application function"""
    st.title("ResumeMatch AI")
    st.markdown("### Match your CV against job descriptions using AI")
    st.markdown("---")
    
    # Load models
    with st.spinner("Loading AI models..."):
        if not st.session_state.model_loaded:
            embedding_model, similarity_calculator, score_engine = load_models()
            if embedding_model:
                st.session_state.embedding_model = embedding_model
                st.session_state.similarity_calculator = similarity_calculator
                st.session_state.score_engine = score_engine
                st.session_state.model_loaded = True
                st.success("Models loaded successfully!")
            else:
                st.error("Failed to load models. Please check your internet connection and try again.")
                return
    
    # Sidebar
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. **Upload your CV** (PDF, DOCX, or TXT)
        2. **Enter or upload job description**
        3. Click **Match CV** to get results
        4. Review your match score and recommendations
        """)
        
        st.markdown("---")
        st.markdown("### Supported Formats")
        st.markdown("- PDF (.pdf)")
        st.markdown("- Word Document (.docx)")
        st.markdown("- Text File (.txt)")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("Developed by Fahad Pathan")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload CV")
        cv_file = st.file_uploader(
            "Choose your CV file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your CV in PDF, DOCX, or TXT format"
        )
        
        if cv_file:
            st.success(f"{cv_file.name} uploaded")
            with st.expander("Preview CV"):
                try:
                    cv_text, _ = parse_document(cv_file.read(), cv_file.name)
                    st.text_area("CV Content", cv_text[:500] + "..." if len(cv_text) > 500 else cv_text, height=200)
                except Exception as e:
                    st.error(f"Error reading CV: {str(e)}")
    
    with col2:
        st.subheader("Job Description")
        job_input_method = st.radio(
            "Input method",
            ["Text Input", "File Upload"],
            horizontal=True
        )
        
        job_text = ""
        if job_input_method == "Text Input":
            job_text = st.text_area(
                "Enter job description",
                height=300,
                placeholder="Paste the job description here..."
            )
        else:
            job_file = st.file_uploader(
                "Upload job description",
                type=['pdf', 'docx', 'txt'],
                help="Upload job description file"
            )
            if job_file:
                try:
                    job_text, _ = parse_document(job_file.read(), job_file.name)
                    st.success(f"{job_file.name} uploaded")
                except Exception as e:
                    st.error(f"Error reading job description: {str(e)}")
    
    # Process button
    st.markdown("---")
    process_button = st.button("Match CV", type="primary", use_container_width=True)
    
    if process_button:
        if not cv_file:
            st.error("Please upload a CV file")
            return
        
        if not job_text.strip():
            st.error("Please provide a job description")
            return
        
        # Process the matching
        with st.spinner("Processing... This may take a few seconds"):
            try:
                # Parse CV
                cv_file.seek(0)  # Reset file pointer
                cv_text, _ = parse_document(cv_file.read(), cv_file.name)
                
                if not cv_text.strip():
                    st.error("Could not extract text from CV. Please check the file format.")
                    return
                
                # Process texts
                text_processor = TextProcessor()
                cv_cleaned = text_processor.clean_text(cv_text)
                job_cleaned = text_processor.clean_text(job_text)
                
                # Identify sections
                cv_sections = text_processor.identify_sections(cv_cleaned)
                job_sections = text_processor.identify_sections(job_cleaned)
                
                # Calculate scores
                score_engine = st.session_state.score_engine
                results = score_engine.calculate_match_score(
                    cv_cleaned, job_cleaned, cv_sections, job_sections
                )
                
                # Display results
                st.markdown("---")
                st.header("Match Results")
                
                # Overall score
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    score = results['final_score']
                    interpretation = score_engine.get_score_interpretation(score)
                    
                    st.metric(
                        "Overall Match Score",
                        f"{score:.1f}%",
                        delta=interpretation
                    )
                    st.markdown(f"### {interpretation}")
                
                # Score breakdown
                st.subheader("Score Breakdown")
                breakdown_cols = st.columns(4)
                
                with breakdown_cols[0]:
                    st.metric("Overall Similarity", f"{results['overall_similarity']:.1f}%")
                with breakdown_cols[1]:
                    st.metric("Skills Match", f"{results['skills_match']:.1f}%")
                with breakdown_cols[2]:
                    st.metric("Experience Match", f"{results['experience_match']:.1f}%")
                with breakdown_cols[3]:
                    st.metric("Education Match", f"{results['education_match']:.1f}%")
                
                # Visual progress bars
                st.progress(results['overall_similarity'] / 100, text="Overall Similarity")
                st.progress(results['skills_match'] / 100, text="Skills Match")
                st.progress(results['experience_match'] / 100, text="Experience Match")
                st.progress(results['education_match'] / 100, text="Education Match")
                
                # Skills analysis
                st.subheader("Skills Analysis")
                skills_col1, skills_col2 = st.columns(2)
                
                with skills_col1:
                    st.markdown("**Matched Skills**")
                    if results['matched_skills']:
                        for skill in results['matched_skills'][:20]:  # Show first 20
                            st.markdown(f"- {skill}")
                    else:
                        st.info("No skills matched")
                
                with skills_col2:
                    st.markdown("**Missing Skills**")
                    if results['missing_skills']:
                        for skill in results['missing_skills'][:20]:  # Show first 20
                            st.markdown(f"- {skill}")
                    else:
                        st.success("All required skills found!")
                
                # Recommendations
                st.subheader("Recommendations")
                recommendations = []
                
                if results['skills_match'] < 50:
                    recommendations.append("**Improve Skills Match**: Consider highlighting more relevant skills from the job description in your CV.")
                
                if results['experience_match'] < 50:
                    recommendations.append("**Experience Gap**: Ensure your experience section clearly demonstrates relevant work history.")
                
                if results['missing_skills']:
                    recommendations.append(f"**Add Missing Skills**: Consider adding or highlighting these skills: {', '.join(results['missing_skills'][:5])}")
                
                if results['overall_similarity'] < 60:
                    recommendations.append("**Improve Overall Match**: Review the job description keywords and ensure they appear in your CV.")
                
                if not recommendations:
                    recommendations.append("**Great Job!** Your CV is well-matched to this position.")
                
                for rec in recommendations:
                    st.markdown(rec)
                
                # Section similarities
                if results['section_similarities']:
                    st.subheader("Section-wise Similarities")
                    for section, similarity in results['section_similarities'].items():
                        st.markdown(f"**{section.title()}**: {similarity:.1f}%")
                        st.progress(similarity / 100)
                
            except Exception as e:
                st.error(f"Error processing: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()

