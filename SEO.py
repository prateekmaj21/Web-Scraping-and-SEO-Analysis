# Importing Libraries 
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
from requests_html import HTMLSession
import streamlit as st
import warnings
from PIL import Image

# Suppress warnings
warnings.filterwarnings('ignore')

# Set up the Streamlit app
st.title('SEO Analysis App')
st.markdown("This application helps to analyze the SEO for a particular search engine query 🔎.")

# Display an image
image = Image.open('seo-1.png')
st.image(image)

# Provide information about the query
st.markdown("The query is the string you search in Google.")
st.markdown("The search here is automated.")

# Input for the search query
query = st.text_input("Enter the string to be searched")
st.write('The string entered by the user is:', query)

# Slider to select the number of links to search
link_count = st.slider("Enter the number of links to be searched", 0, 100)
st.write('The number of links that need to be searched are:', link_count)

# Input for the top level domain
st.markdown("The domain is to be entered, e.g., co.in, co.uk, .com etc.")
tld = st.text_input("Enter the top level domain")
st.write('The top level domain entered by the user is:', tld)

# Initialize variables
links = []
body = ""

# Perform the search and display links
st.subheader("The links searched are:")
for i in search(query, tld=tld, lang='en', num=link_count, start=0, stop=link_count, pause=2.0):
    st.write(i)
    links.append(i)

# Extract and process the content from each link
for k in links:
    try:
        html_content = requests.get(k).text
        soup = BeautifulSoup(html_content, "lxml")
        body += soup.body.text if soup.body else " "
    except Exception as e:
        st.write(f"Error fetching content from {k}: {e}")

# Process the combined body text
body = re.sub(r'[^\w\s]', '', body.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')).lower()
num = body.count(query.lower())

st.write("The frequency of the string", query, "in all the link's body combined is:", num)

# Initialize variables for titles and meta descriptions
title_full = ""
meta_full = ""

for j in links:
    try:
        session = HTMLSession()
        response = session.get(j)
        title = response.html.find('title')
        title_full += title[0].text if title else " "
        meta_desc = response.html.xpath('//meta[@name="description"]/@content')
        meta_full += meta_desc[0] if meta_desc else " "
    except Exception as e:
        st.write(f"Error processing link {j}: {e}")

# Process the combined title and meta description text
title_full = title_full.lower()
meta_full = meta_full.lower()

st.subheader("Title (From all the Links combined)")      
st.write(title_full)

st.subheader("Meta (From all the Links combined)")
st.write(meta_full)

num2 = title_full.count(query.lower())
st.write("The frequency of the string", query, "in all the link's titles is:", num2)

num3 = meta_full.count(query.lower())
st.write("The frequency of the string", query, "in all the link's meta descriptions is:", num3)

st.title("Developed by-")
st.markdown("Sayanti Dutta & Prateek Majumder")

