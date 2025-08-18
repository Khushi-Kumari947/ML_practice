import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO

# Set Gemini API key
genai.configure(api_key="gemini-api-key")
model = genai.GenerativeModel("gemini-pro")

st.set_page_config(page_title="Dataset Generator using Gemini", layout="centered")

st.title("Dataset Generator")

# User input
prompt = st.text_area("Enter your dataset prompt", placeholder="e.g. Generate a dataset of 50 students with Name, Age, Grade, Email...")

if st.button("Generate Dataset"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating dataset..."):
            try:
                #format as CSV
                full_prompt = (
                    "You are a helpful assistant that generates realistic, well-formatted datasets in CSV format "
                    "based on user prompts. Do not return any explanation—only return the CSV content.\n\n"
                    f"{prompt}"
                )
                response = model.generate_content(full_prompt)
                csv_data = response.text

                #converting to DataFrame
                try:
                    df = pd.read_csv(StringIO(csv_data))
                    st.success("Dataset generated successfully!")
                    st.dataframe(df)

                    # Download
                    csv_download = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download CSV",
                        data=csv_download,
                        file_name="generated_dataset.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error("Failed to convert response to a table.")
                    st.code(csv_data)

            except Exception as e:
                st.error(f"Error: {e}")
