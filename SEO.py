

#Importing Libraries 
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
from requests_html import HTMLSession
import streamlit as st
import warnings
warnings.filterwarnings('ignore') 
from PIL import Image


st.title('SEO Analysis App')
st.markdown("This application helps to analyse the SE0 for a particular Se🔎 arch Engine query .")

image = Image.open('seo-1.png')
st.image(image)

st.markdown("The query is the string you search in Google.")
st.markdown("The search here is automated.")

query = st.text_input("Enter the string to be searched")
'The string entered  by the user is: ', query

link=st.slider("Enter the number of links to be searched",0,100)
'The number of links that needs to be searched are : ',link

st.markdown("The domain is to be entered, eg co.in, co.uk, .com etc.")
tld=st.text_input("Enter the top level domain")
'The top level domain entered by the user is:',tld

links=[None]*link
j=0
st.subheader("The links searched are:")
for i in search(query, tld='co.in', lang='en', num=link, start=0, stop=link, pause=2.0):
    st.write(i)
    links[j]=i
    j=j+1

body=" "


for k in links:
    html_content = requests.get(k).text
    soup = BeautifulSoup(html_content, "lxml")
    try:
        body=body+soup.body.text
    except:
        body= body+" "
    
meta_tag=soup.findAll('meta')


body= body.replace('\n', ' ')
body= body.replace('\t', ' ')
body= body.replace('\r', ' ')
body=re.sub(r'[^\w\s]', '', body) 
body=body.lower()
num=body.count(query)

('-------')
st.write("The frequency of the string "",query,""in the all the link's body combined is :",num)

title_full=" "
meta_full=" "

for j in links:
    try:
        
        session = HTMLSession()
        response = session.get(j)
    
    except requests.exceptions.RequestException as e:
        st.write(e)
        

    title =  response.html.find('title')
    try:
        
        title_full= title_full+ (title[0].text)
    except:
        title_full= title_full+ " "
        
        
    meta_desc =  response.html.xpath('//meta[@name="description"]/@content')
    try:
        meta_full=meta_full+ (meta_desc[0])
    except:
        meta_full=meta_full+" "
    
    
    
meta_full=meta_full.lower()        
title_full=title_full.lower()

('-------')
 
st.subheader ("Title (From all the Links combined)")      
st.write(title_full)

('-------')
st.subheader ("Meta  (From all the Links combined)")
st.write(meta_full)

('-------')

num2=title_full.count(query)
st.write("The frequency of the string ",query,"in all the link's title is :",num2)

('-------')

num3=meta_full.count(query)
st.write("The frequency of the string ",query,"in all the link's meta is:",num3)


('-------')

st.title("Developed by-")
st.markdown("Sayanti Dutta & Prateek Majumder")
st.markdown("All code rights belong to the authors.")