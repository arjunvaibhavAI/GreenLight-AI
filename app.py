import streamlit as st
from pypdf import PdfReader
from io import BytesIO

from src.agent import app as audit_agent

# page Configuration
st.set_page_config(
    page_title="GreenLight AI: ESG Auditor",
    page_icon="💡",
    layout="wide"
)

# header
st.title("💡 GreenLight AI: Your ESG Compliance Auditor")
st.markdown("Upload your company's annual or sustainability report (in PDF format) to get an automated compliance analysis against GRI standards.")

# application
uploaded_file = st.file_uploader("Upload your report PDF", type="pdf")

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    if st.button("Start Audit", type="primary"):
        with st.spinner("The AI Auditor is at work... This may take a few moments..."):
            try:
                # read the PDF content
                bytes_data = uploaded_file.getvalue()
                pdf_reader = PdfReader(BytesIO(bytes_data))
                
                # extract text from all pages
                report_text = ""
                for page in pdf_reader.pages:
                    report_text += page.extract_text() or ""

                st.info("Successfully extracted text from the PDF.")

                # input for the LangGraph agent
                initial_state = {"company_report_text": report_text}
                
                # invoke the agent
                st.info("Running compliance checks...")
                final_state = audit_agent.invoke(initial_state)
                
                # display the results
                st.subheader("Audit Findings:")
                if final_state.get("audit_findings"):
                    for finding in final_state["audit_findings"]:
                        st.markdown(f"- {finding}")
                else:
                    st.warning("The audit completed, but no specific findings were generated.")

                if final_state.get("error"):
                    st.error(f"An error occurred during the audit: {final_state['error']}")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

else:
    st.info("Please upload a PDF file to begin the audit.")