import streamlit as st
from comparison import Comparison
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import SessionState

ss = SessionState.get(name="", button_sent=False)  # to cache the check button and the result

### GET THE GOOGLE SHEET
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']  
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
@st.cache(allow_output_mutation=True)
def get_table():
    client = gspread.authorize(creds)
    sheet = client.open('answerchecker_proto').get_worksheet(0)
    return sheet

sheet = get_table()

def update_table(r_a, u_a, result, feedback):
    sheet.append_row([r_a, u_a, result, feedback], 'USER_ENTERED')


### CHECK ANSWER
st.title('Answer checker')
r_a = st.text_input('Right Answer')
u_a = st.text_input('User Answer')
check_button    = st.button('Check answer')

if check_button:
    c = Comparison(r_a, u_a)
    ss.result = c.get_result()
    st.write('The answer is {}'.format(ss.result))
    ss.button_sent = True

### FEEDBACK
st.subheader('Send a feedback')
if st.button('Acceptable') and ss.button_sent: 
    update_table(r_a, u_a, ss.result, 'acceptable')
    ss.button_sent = False
    st.write('Feedback sent')

if st.button('Too permissive') and ss.button_sent: 
    update_table(r_a, u_a, ss.result, 'permissive')
    ss.button_sent = False
    st.write('Feedback sent')

if st.button('Too severe') and ss.button_sent: 
    update_table(r_a, u_a, ss.result, 'severe')
    ss.button_sent = False
    st.write('Feedback sent')