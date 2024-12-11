import streamlit as st
import pandas as pd
from io import BytesIO
import google.generativeai as genai
import os
from dotenv import load_dotenv
from config import GEMINI_API_KEY


# load_dotenv()
# Configure Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print(os.getenv("GEMINI_API_KEY"))

# Set the model and generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",  # You can choose the model variant
    generation_config=generation_config,
)

# Streamlit App Title
st.set_page_config(page_title="Excel Sheet Query Tool", page_icon=":bar_chart:", layout="centered")

st.title("Excel Sheet Query Tool :bar_chart:")
st.write("Upload an Excel file and ask any questions related to its data!")

# Upload Excel section
uploaded_file = st.file_uploader("Choose an Excel file...", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Read the uploaded Excel file
        excel_data = pd.ExcelFile(uploaded_file)
        st.write("### Sheets in the uploaded Excel file:")
        sheet_names = excel_data.sheet_names
        st.write(sheet_names)

        # Select a sheet to work with
        selected_sheet = st.selectbox("Select a sheet to analyze:", sheet_names)

        if selected_sheet:
            # Load the selected sheet into a DataFrame
            df = excel_data.parse(selected_sheet)
            st.write(f"### Data from sheet: {selected_sheet}")
            st.dataframe(df)

            # Text Input for asking a question about the data
            question = st.text_input("Ask a question about this data:")

            if st.button("Ask AI"):
                if question:
                    with st.spinner("Processing your request..."):
                        try:
                            # Convert the DataFrame to a CSV format for input to the model
                            csv_data = df.to_csv(index=False)
                            
                            # Use AI to generate content (mocked for this example)
                            response = model.generate_content([question, csv_data])
                            # response = f"Mock response for question: '{question}' based on sheet: '{selected_sheet}'."
                            
                            st.success("AI Response:")
                            st.write(response)
                        except Exception as e:
                            st.error(f"Error occurred: {str(e)}")
                else:
                    st.error("Please enter a question.")
    except Exception as e:
        st.error(f"Error reading the Excel file: {str(e)}")
else:
    st.write("Please upload an Excel file to proceed.")
