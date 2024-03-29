import streamlit as st
from model.finmodel import FinModel
from tqdm import tqdm
from IPython.display import display, Markdown
import PyPDF2
import os 
import shutil, tempfile

def main():
    st.sidebar.title('FinGenInsights')
    st.sidebar.subheader('Financial Insights for the Future')
    
    st.title('Welcome to FinGenInsights')
    st.text('This is a simple web application to view financial insights')
    
    st.write("Upload your PDF file to get started")
    
    uploaded_file = st.file_uploader("Upload your PDF file to get started", type="pdf")
       
    if uploaded_file is not None:
        st.write("File is uploaded")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            # Write the uploaded file to the temporary file
            shutil.copyfileobj(uploaded_file, tmp)
            tmp_path = tmp.name

        # Pass the temporary file path to the FinModel
        model = FinModel(tmp_path)
        resp = model.as_query_engine().query("Based on document provide me insights as Bullet points about financial status of the speicif quarter.")
        ### we get the resp text and pass it as part of the query to get the tabular data
        resp_text = str(resp)
        #print(resp_text)
        tab_str = resp_text + " Extract total net revenue, Net Income, Total Assets, Loans and Deposits in comparative analysis in tabular format"
        tabular_data = model.as_query_engine().query(tab_str)
        colu1, colu2 = st.columns(2)
        with colu1:
            st.markdown(resp)
        with colu2:
            st.markdown(tabular_data)
        # Delete the temporary file
        os.unlink(tmp_path)
    
if __name__ == '__main__':
    main()