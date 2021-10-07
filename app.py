import streamlit as st
from comparison import Comparison
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import SessionState

### GET THE GOOGLE SHEET
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']  
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)

@st.cache(allow_output_mutation=True)
def get_sheet():
    client = gspread.authorize(creds)
    return client.open('answerchecker_proto').get_worksheet(0)

sheet = get_sheet()
ss = SessionState.get(name="", button_sent=False)  # to cache the check button

### EVALUATE THE RIGHT AND USER ANSWERS
st.title('Answer checker')

r_a = st.text_input('Right Answer')
u_a = st.text_input('User Answer')

check_button    = st.button('Check answer', key=1)

feedback = st.selectbox('Why the program is incorrect?',
                        ('Too permissive', 'Too severe', 'Other'))

feedback_button = st.button('Send feedback', key=2)

if check_button:
    c = Comparison(r_a, u_a)
    ss.result = c.get_result()
    st.write('The answer is {}'.format(ss.result))
    ss.button_sent = True

if feedback_button and ss.button_sent:
    sheet.append_row([r_a, u_a, ss.result, feedback], 'USER_ENTERED')
    ss.button_sent = False
    st.write('Feedback sent')