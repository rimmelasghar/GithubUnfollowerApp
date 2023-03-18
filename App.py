import requests
import streamlit as st
import numpy as np
import pandas as pd
from load import Load
import webbrowser


@st.cache_data
def verify_user(username):
   api_url=f"https://api.github.com/users/{username}"
   res = requests.get(api_url)
   data = res.json()
   if "message" in data.keys():
      return []
   else:
      return data

def get_unfollowers(lsta,lstb):
   lst = []
   for i in lstb:
      if i not in lsta:
         lst.append(i)
   return lst

@st.cache_data
def generate(username):
   follower_lst = Load(f"{username}","followers").get_data()
   following_lst = Load(f"{username}","following").get_data()
   lst = get_unfollowers(follower_lst[f"{username}"],following_lst[f"{username}"])
   return lst


with open('style.css')as f:
   st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


def App():
   st.title('Github Unfollowers')
   st.markdown("_Get to know about people Who did'nt follow you back_")
   st.markdown('_created by Rimmel with ❤️_')
   st.markdown("""<a href='https://github.com/rimmelasghar/GithubUnfollowerApp'><img src='https://img.shields.io/github/stars/rimmelasghar/GithubUnfollowerApp?color=red&label=star%20me&logoColor=red&style=social'></a>""",unsafe_allow_html=True) 
   username = st.text_input('Enter Your Github Username')
   btn = st.button('Generate')
   elements = st.container()

   if btn:
      data = verify_user(username)
      if data:
         with elements:
            st.components.v1.html(f"""
            <script src="https://unpkg.com/@rocktimsaikia/github-card@1.0.0/dist/widget.min.js" type="module"></script>
            <div id='container'>
                  <h1 style="text-align: center;color:white; font-family: 'Roboto', sans-serif; ">Your Github Profile</h1>
                     <div style="width: 50%; margin: 0 auto;"> 
                        <github-card data-user="{username}" data-theme="dark"></github-card>
                     </div>""",height=600) 
            st.markdown(f"""<table>
                     <tr>
                     <th>Stats</th>
                     <th>Streak</th>
                     <th>Languages</th>
                     </tr>
                     <tr>
                     <td><img src='http://github-profile-summary-cards.vercel.app/api/cards/stats?username={username}&theme=github_dark' width=200px height=100px></td>
                     <td><img src='https://streak-stats.demolab.com?user={username}&theme=github-dark&hide_border=true&border_radius=32&date_format=j%20M%5B%20Y%5D&ring=888888' width=180px height=100px></td>
                     <td><img src='http://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username={username}&theme=github_dark' width= 200px height=100px></td>
                     </tr>
                     </table><br><br>
                     </div> <h1 style="text-align: center;color:white; font-family: 'Roboto', sans-serif; ">{username}'s Unfollowers</h1><br>
                     <p>These are those people who did'nt follow you back</p>""",unsafe_allow_html=True)
         lst = generate(username)
         elements.markdown(f'_Found {len(lst)} result_')
         col1,col2,col3= elements.columns(3)
         col1.header("Profile")
         col2.header("Username")
         col3.header("Action")
         for i in range(len(lst)):
            col1.image(lst[i]["avatar_url"],width=25)
            col2.write(lst[i]["login"])
            col3.markdown(f"""<a href="https://github.com/{lst[i]["login"]}" target="_blank">Github Profile</a>""",unsafe_allow_html=True)
      else:
         st.markdown('_username not found_')


   st.markdown("""<link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">""",unsafe_allow_html=True)

if __name__=="__main__":
       App()
   