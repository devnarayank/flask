import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
# from flask import request
# from io import BytesIO
# from models import Article, db
import time
import requests
import pandas as pd
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
import json
import random
import argparse
import redis


# # OAuth Initialization
# client_id = "265204031707-humurdeb2p58dl9c4ufgcv029k3ponun.apps.googleusercontent.com"
# client_secret = "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"
# scopes = ["https://www.googleapis.com/auth/indexing"]

# # OAuth flow setup
# flow = InstalledAppFlow.from_client_config({
#     "installed": {
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://accounts.google.com/o/oauth2/token"
#     }
# }, scopes)

# credentials = flow.run_local_server(port=0)
# google_api_token = credentials.token

# Function to generate content using ChatGPT
api_key = "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"
#api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
#api_endpoint = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"  # Updated to point to Turbo
api_endpoint = "https://api.openai.com/v1/chat/completions"

def generate_content(topic, api_key, api_endpoint):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Generate Title
    title_prompt = f"Generate a compelling title for an article about {topic}."
    title_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": title_prompt}
        ],
        "max_tokens": 30
    }
    
    title_response = requests.post(api_endpoint, headers=headers, json=title_data)
    try:
        # Modified line: Using get() with default values to prevent KeyError
        article_title = title_response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        print("Article Title:", article_title)
        # Modified line: Added check to ensure title is not empty
        if not article_title:
            raise ValueError("Empty title generated.")
    except (KeyError, ValueError, IndexError) as e:
        # Modified line: Error handling with detailed error message and API response
        print(f"Error generating title: {e}")
        print(title_response.text)
        return None, None  # Return a tuple of None values if there's an error

    # # Generate Article Content
    # content_prompt = (
    #     f"Generate a compelling article about {topic}, focusing on its challenges "
    #     "in professional settings, the corporate world, or businesses that hire employees.\n"
    #     "Write a 600-800 word article in HTML format. Make sure to incorporate relevant SEO tags "
    #     "like H1, H2, H3, etc., without explicitly stating them.\n"
    #     f"Discuss the losses in terms of time, energy, and money citing stats from different newspapers because of {topic}. "
    #     "Explain how the Offer Ghosting Platform, developed by Sumeru Digital, serves as a blockchain-based solution using Hyperledger Fabric.\n"
    #     "Include features such as 'Report Candidate Ghosting,' 'Find Candidates Trust Score,' and 'View Candidate History on Blockchain' "
    #     "to provide a holistic view of the solution.\n"
    #     "Conclude by emphasizing the platform's utility and urging readers to sign up for a free trial. "
    #     "Urge the business owners to start reporting any such ghosting incident they have experienced in the past or recently, "
    #     "which will help to eradicate this pandemic-like problem in the business world and help bring back work commitments.\n"
    #     "Include clickable links to the Offer Ghosting Platform's website (https://offerghosting.com/) "
    #     "and the registration URL (https://app.offerghosting.com/register).\n"
    #     "Highlight crucial points and keywords in bold or italics.\n"
    #     "Make sure to exclude any fake or placeholder URLs."
    # )

    # Placeholder for the main site and sign-up URLs
    main_site_url = "https://offerghosting.com"
    signup_url = "https://app.offerghosting.com/register"

    # Randomly choose between prompting for main site or sign-up
    call_to_action_url = random.choice([main_site_url, signup_url])

    # Generate Article Content
    content_prompt = (
        f"Create a detailed, 2000-word, SEO-optimized article about {topic}, focusing on its challenges "
        "in professional settings, the corporate world, or businesses that hire employees.\n"
        "The article should be in HTML format and have at least 15 headings and subheadings, including H1, H2, H3, and H4 tags.\n"
        "Discuss the losses in terms of time, energy, and money. "
        "Introduce the Offer Ghosting Platform by Sumeru Digital as a blockchain-based solution using Hyperledger Fabric.\n"
        "Highlight features like 'Report Candidate Ghosting,' 'Find Candidates Trust Score,' and 'View Candidate History on Blockchain' "
        "to provide a holistic view of the solution.\n"
        "Conclude by emphasizing the platform's utility and urging readers to learn more or sign up for a free trial by visiting our platform."
        f" For more information or to register, please visit {call_to_action_url}.\n"
        "End with a conclusion paragraph and 5 unique FAQs.\n"
        "Highlight crucial points and keywords in bold or italics.\n"
        "Write in a conversational style, using an informal tone, personal pronouns, rhetorical questions, and analogies.\n"
        "Ensure high levels of perplexity and burstiness without losing specificity or context.\n"
    )

    content_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content_prompt}
        ],
        "max_tokens": 1500
    }

    content_response = requests.post(api_endpoint, headers=headers, json=content_data)

    try:
        # Modified line: Using get() with default values to prevent KeyError
        article_body = content_response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        # Modified line: Added check to ensure content is not empty
        if not article_body:
            raise ValueError("Empty content generated.")
    except (KeyError, ValueError, IndexError) as e:
        # Modified line: Error handling with detailed error message and API response
        print(f"Error generating content: {e}")
        print(content_response.text)
        return article_title, None  # Return the title and None for the body if there's an error

    return article_title, article_body
     # Emitting log message


    # #return article_title.strip(), article_body.strip()
    # print("Sending the following data to the API:")
    # print(json.dumps(data, indent=4))
    
    # response = requests.post(api_endpoint, headers=headers, json=data)
    
    # print(f"API Response: {response.status_code}, {response.json()}")
    
    
    # try:
    #     generated_content = response.json()['choices'][0]['message']['content']
    # except KeyError:
    #     print("KeyError: The API response doesn't contain 'choices'")
    #     return None, None
    
    # article_lines = generated_content.split('\n')
    # article_title = article_lines[0].strip()
    # article_body = '\n'.join(article_lines[1:]).strip()
    
    # return article_title, article_body


# WordPress Setup
# wp_url = "https://offerghosting.com/"
# wp_username = "abjgd108"
# wp_password = "Abjgd#108"
wp_url = "https://ghostingjob.com/"
wp_username = "abjgd"
wp_password = "Abjgd#108"
client = Client(f"{wp_url}/xmlrpc.php", wp_username, wp_password)

def post_to_wordpress(article_title, article_content):
    post = WordPressPost()
    post.title = article_title
    post.content = article_content
    post.post_status = 'publish'
    
    if article_title is not None:
         post.slug = article_title.lower().replace(' ', '-')  
    else:
    # Handle the case where article_title is None
    # For example, set a default slug or log an error
        default_slug = "default-slug"
        post.slug = default_slug
        print("Warning: article_title is None, setting default slug:", default_slug)     
    
    result = client.call(posts.NewPost(post))
    print(f"WordPress Response: {result}")
    return result
     # Emitting log message

# Read keywords from Excel
excel_path = "/home/admin123/Desktop/test3.xlsx"
sheet_name = 'Candidate ghosting company keyw'
# excel_path = r"C:\Users\abjgd\Documents\employment-ghosting.xlsx"

# excel_file = request.files['excel_file'] # Assuming you have Flask request
# excel_data = BytesIO(excel_file.read())

parser = argparse.ArgumentParser(description='Generate content using OpenAI GPT-3.5 Turbo.')
parser.add_argument('--wp_url', type=str, help='WordPress URL')
parser.add_argument('--excel_path', type=str, help='Path to the Excel file')
parser.add_argument('--content_prompt', type=str, help='prompt for article generation')
parser.add_argument('--api_key', type=str, help='openai key ')

args = parser.parse_args()



df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols="A", names=["Keywords"], engine='openpyxl')
keywords = df["Keywords"].dropna().tolist()

# Counter for processed keywords
processed_keywords = 0

# Loop through keywords from Excel
for topic in keywords:
    print(f"Generating article for: {topic}")

    # Generate Content
    article_title, article_content = generate_content(topic, api_key, api_endpoint)


    # Post to WordPress
    post_id = post_to_wordpress(article_title, article_content)
    print(f"Posted article with ID: {post_id}")

    # Generate SEO-friendly article URL
    article_url = f"{wp_url}/{article_title.replace(' ', '-').lower()}"

    # # Request Google to index the new article
    # indexing_response = request_google_indexing(article_url, google_api_token)
    
    # if 'error' in indexing_response:
    #     print(f"Failed to request indexing. Response: {indexing_response}")
    # else:
    #     print(f"Successfully requested indexing for the URL: {article_url}")

    processed_keywords += 1
 # Emitting final log message

# generate article status
# def generate_article(article_id):
#     article = Article.query.get(article_id)

#     if article:
#         try:
#             # Update the article status to 'generating'
#             article.status = 'generating'
#             db.session.commit()

#             # Simulate article generation process
#             time.sleep(5)  # Replace with your actual generation logic

#             # Update the article status to 'generated'
#             article.status = 'generated'
#             db.session.commit()

#             print(f"Article {article_id} generated successfully.")
#         except Exception as e:
#             # Handle exceptions appropriately
#             print(f"Error generating article {article_id}: {str(e)}")
#             article.status = 'failed'
#             db.session.commit()


print(f"All keywords processed. Total keywords: {processed_keywords}")
