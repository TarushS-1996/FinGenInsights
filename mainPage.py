import os
import boto3
import streamlit as st
from model.finmodel import FinModel
from streamlit_option_menu import option_menu
from page import insightsPage, retrieveinfo
from chatpage import chatPage
from insightspage2 import insights_page2
import tempfile
from dotenv import load_dotenv
from model.geminimodel import GeminiModel
from chatgemini import chatGemini
from loginPage import loginpage
# Load environment variables
load_dotenv()

# Define your main function
def main():
    sidebar_bg_color = "#2D2D2D"
    sidebar_text_color = "#FFFFFF"
    sidebar_title_size = 25
    sidebar_subheader_size = 15
    # Initialize a session using environment credentials
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    # Create an S3 client
    s3 = session.client('s3')

    bucket_name = 'fingeninsights'  # Name of your S3 bucket

    # Define the file keys for the two PDFs
    file_keys = [
        'JPMC_Quaterly_Financial_Report/merged_pdf.pdf',
        'Stock_Market_Information/stock_info.pdf'
    ]

    # Check if 'selected' is in session_state, otherwise initialize it
    if 'selected' not in st.session_state:
        st.session_state['selected'] = 'Chat'


    # Set up the UI layout with sidebar and option menu
    st.sidebar.image("images/NewLogo.png", width=200)
    st.sidebar.title('FinGenInsights')
    st.sidebar.subheader('Financial Insights for the Future')

    
    


    with st.container():
        # Provide options for selecting the PDF file
        selected_file = st.selectbox('Choose a Data Source:', ['JPMC financial info', 'Stock market info'])
        selected_file_key = file_keys[0] if selected_file == 'JPMC financial info' else file_keys[1]
        
        # Use the session state for the option menu
        st.session_state['selected'] = option_menu(menu_title=None, 
                                                   options=['Chat', 'Insights', 'ChatXGemini'],
                                                   icons=['chat-left-text-fill', 'lightbulb-fill', 'google'],
                                                   
                                                   default_index=0,  # Set the default index if needed
                                                   orientation='horizontal' 
                                                   
                                                   
                                                   
                                                   )

    try:
        # Load file from S3 based on the selected file key
        response = s3.get_object(Bucket=bucket_name, Key=selected_file_key)
        file_content = response['Body'].read()

        # Save file to a temporary file
        tmp_file_path = None
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        # Pass the file path to the model
        vec = FinModel(tmp_file_path)

        # Check the value of 'selected' to determine which page to display
        if st.session_state['selected'] == 'Insights':
            insights_page2(model=vec)
        elif st.session_state['selected'] == 'Chat':
            chatPage(model=vec)
        elif st.session_state['selected'] == 'ChatXGemini':
            gemini_vec = GeminiModel(tmp_file_path)
            chatGemini(gemini_vec)    
    finally:
        # Ensure the temporary file is deleted if it was created
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

if __name__ == '__main__':
    page = loginpage()
    if page:
        main()
