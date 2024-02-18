import os
import requests
import streamlit as st
import openai

from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Create a Streamlit interface to take user input
search_term = st.text_input('Enter your search term: ')

if search_term:
    # Make a request to the NewsAPI with the user input as the search term
    response = requests.get(f'https://newsapi.org/v2/everything?q={search_term}&apiKey={NEWS_API_KEY}')
    response_json = response.json()

    # Extract the first news article from the response
    first_article = response_json['articles'][0]['content']

    # Use OpenAI API to summarize the news article
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": f"{first_article}"}
        ]
    )

    # Extract the assistant's reply
    summary = completion['choices'][0]['message']['content']

    # Display the summary on the Streamlit interface
    st.write(summary)