import streamlit as st
import openai
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from datetime import datetime, date
from decimal import Decimal
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Configuration
st.set_page_config(page_title="Social Media Analytics Assistant", layout="wide")

# Get API keys from .env
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASTRA_DB_TOKEN = os.getenv('ASTRA_DB_TOKEN')
SECURE_CONNECT_BUNDLE_PATH = os.getenv('ASTRA_SECURE_CONNECT_BUNDLE_PATH')
ASTRA_DB_KEYSPACE = os.getenv('ASTRA_DB_KEYSPACE', 'default_keyspace')

# Check if environment variables are set
if not all([OPENAI_API_KEY, ASTRA_DB_TOKEN, SECURE_CONNECT_BUNDLE_PATH]):
    st.error("Please set all required environment variables in your .env file")
    st.stop()

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# AstraDB Connection Setup
def init_astra_db():
    try:
        cloud_config = {
            'secure_connect_bundle': SECURE_CONNECT_BUNDLE_PATH
        }
        auth_provider = PlainTextAuthProvider('token', ASTRA_DB_TOKEN)
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect()
        session.set_keyspace(ASTRA_DB_KEYSPACE)
        return session
    except Exception as e:
        st.error(f"Failed to connect to database: {str(e)}")
        return None

# Initialize database connection
session = init_astra_db()
if not session:
    st.error("Could not establish database connection. Please check your credentials and secure connect bundle path.")
    st.stop()

def create_prompt(user_question):
    return f"""You are a social media analytics expert. You have access to a database of social media engagement metrics with the following data structure:

Post Data Fields:
post_id: Unique identifier for each post
type: Type of post (carousel, reel, static)
created_at: Post creation date
likes: Number of likes
shares: Number of shares
comments: Number of comments
views: Number of views
engagement_rate: Overall engagement rate (%)

{user_question}"""

# Query Database
def query_social_media_data():
    try:
        # First, let's get the column names
        query = f"SELECT * FROM {ASTRA_DB_KEYSPACE}.social_media_engagment LIMIT 5"
        rows = session.execute(query)
        
        # Convert rows to list of dictionaries with proper handling
        result = []
        if rows:
            # Get column names from the first row
            columns = rows.column_names
            
            # Convert each row to a dictionary
            for row in rows:
                row_dict = {}
                for i, column in enumerate(columns):
                    # Handle different data types appropriately
                    value = row[i]
                    if isinstance(value, (datetime, date)):
                        value = value.isoformat()
                    elif isinstance(value, (Decimal, float)):
                        value = float(value)
                    elif isinstance(value, (int, bool)):
                        value = value
                    else:
                        value = str(value) if value is not None else None
                    row_dict[column] = value
                result.append(row_dict)
                
        return result
    except Exception as e:
        st.error(f"Database query failed: {str(e)}")
        return []

# Process with GPT-4
def process_with_gpt(prompt, data):
    try:
        # Convert the data to a more readable format for GPT
        formatted_data = json.dumps(data, indent=2)
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes social media data."},
                {"role": "user", "content": f"{prompt}\n\nData: {formatted_data}"}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing with GPT: {str(e)}"

# Streamlit UI
st.title("Social Media Analytics Assistant")

# Chat interface
st.subheader("Ask about social media strategy")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new question
if prompt := st.chat_input("What would you like to know about social media strategy?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get data and process response
    with st.spinner("Analyzing social media data..."):
        # Query database
        data = query_social_media_data()
        
        # Create full prompt
        full_prompt = create_prompt(prompt)
        
        # Get AI response
        response = process_with_gpt(full_prompt, data)
        
        # Add AI response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# Sidebar with additional options
with st.sidebar:
    st.header("Settings")
    debug_mode = st.checkbox("Debug Mode", value=False)
    if debug_mode:
        if 'last_query_result' in locals():
            st.write("Debug - Query Results:", last_query_result)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
    
    st.subheader("About")
    st.markdown("""
    This application helps content creators make data-driven decisions about their social media strategy.
    It analyzes engagement metrics across different content types to provide personalized recommendations.
    """)