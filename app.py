import streamlit as st
from comparison import Comparison
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import SessionState

ss = SessionState.get(name="", button_sent=False)  # to cache the check button and the result

def update_table(r_a, u_a, result, feedback):
    ### GET THE GOOGLE SHEET
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']  
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    sheet = client.open('answerchecker_proto').get_worksheet(0)
    ### UPDATE THE SHEET
    sheet.append_row([r_a, u_a, result, feedback], 'USER_ENTERED')


### PREPARE THE WIDGETS
st.title('Answer checker')
r_a = st.text_input('Right Answer')
u_a = st.text_input('User Answer')
check_button    = st.button('Check answer', key=1)
feedback = st.selectbox('Why the program is incorrect?',
                        ('Too permissive', 'Too severe', 'Other'))
feedback_button = st.button('Send feedback', key=2)


### WIDGET ACTIONS
if check_button:
    c = Comparison(r_a, u_a)
    ss.result = c.get_result()
    st.write('The answer is {}'.format(ss.result))
    ss.button_sent = True

if feedback_button and ss.button_sent: 
    update_table(r_a, u_a, ss.result, feedback)
    ss.button_sent = False
    st.write('Feedback sent')