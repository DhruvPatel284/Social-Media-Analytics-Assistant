
# Social Media Analytics Assistant

Welcome to **Social Media Analytics Assistant**, a web application designed to analyze engagement data from simulated social media accounts. This tool helps content creators make data-driven decisions by providing insights into post performance based on engagement metrics.

## 📚 Table of Contents
- [Project Overview](#-project-overview)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Features in Detail](#-features-in-detail)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## 🚀 Project Overview

**Social Media Analytics Assistant** is a web application that simulates social media engagement data and provides insights into post performance. It utilizes DataStax Astra DB for data storage and OpenAI's GPT for generating insights based on the analyzed data.

### Key Features:
- **Data Generation**: Simulates engagement data for different post types (carousel, reels, static images).
- **Post Performance Analysis**: Analyzes engagement metrics to evaluate the performance of various post types.
- **Insights Generation**: Provides recommendations and insights using GPT based on the analyzed data.

## 🛠️ Technologies Used

### Backend:
- **Python**: The programming language used for backend development.
- **Streamlit**: A framework for building interactive web applications.
- **OpenAI API**: For generating insights from social media engagement data.
- **DataStax Astra DB**: A cloud-based database for storing and querying engagement metrics.

## 🏗️ Project Structure

Here's a breakdown of the core structure:

- **App**: `app.py`
  - Contains the main application logic and user interface built with Streamlit.
  
- **Data Generation**: `data.py`
  - Generates mock social media engagement data and saves it in JSON format.

- **Requirements**: `requirements.txt`
  - Lists all required Python packages for the project.

## 🚀 Getting Started

### Prerequisites:
- **Python 3.11+**
- **DataStax Astra DB account**
- **OpenAI API key**

### Step-by-Step Setup:

1. **Clone the repository**:
   ```
   git clone https://github.com/DhruvPatel284/Social-Media-Analytics-Assistant.git
   cd Social-Media-Analytics-Assistant
   ```

2. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root directory with the following variables**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ASTRA_DB_TOKEN=your_astra_db_token
   ASTRA_SECURE_CONNECT_BUNDLE_PATH=path_to_your_secure_connect_bundle.zip
   ASTRA_DB_KEYSPACE=your_keyspace_name
   ```

4. **Run the application locally**:
   ```
   streamlit run app.py
   ```
   This will start the app and make it accessible at `http://localhost:8501`.

## 📂 Environment Variables
You need to set up the following environment variables in your `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
ASTRA_DB_TOKEN=your_astra_db_token
ASTRA_SECURE_CONNECT_BUNDLE_PATH=path_to_your_secure_connect_bundle.zip
ASTRA_DB_KEYSPACE=your_keyspace_name
```

---

### 📝 Features in Detail:
1. **Data Generation**: Generates a mock dataset of social media engagement metrics.
2. **Post Performance Analysis**: Analyzes how different types of posts perform based on likes, shares, comments, and views.
3. **Insights Generation**: Provides actionable insights using GPT based on engagement metrics.

---

### 🌐 Deployment
To deploy this application, you can use platforms like Heroku or AWS. Ensure that you configure your environment variables accordingly in your deployment environment.

---

### 🤝 Contributing
If you would like to contribute to this project, feel free to submit a pull request or open an issue on the GitHub repository.
