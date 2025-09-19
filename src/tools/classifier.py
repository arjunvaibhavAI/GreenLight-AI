from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import Literal

# import the retriever function 
from .retriever import get_retriever

load_dotenv()

# Pydantic Data Structure
class ComplianceResult(BaseModel):
    """A model to hold the result of a compliance check."""
    compliance_status: Literal["Met", "Partially Met", "Not Met", "Uncertain"] = Field(
        description="The compliance status based on the provided texts."
    )
    reasoning: str = Field(
        description="A brief, one-sentence justification for the compliance status."
    )
    summary: str = Field(
        description="A general summary of the company report excerpt, approximately 100-150 words."
    )


# Classifier Tool
def get_compliance_classifier():
    """
    creates and returns a LangChain chain that classifies compliance.
    """
    # create an output parser
    parser = JsonOutputParser(pydantic_object=ComplianceResult)

    # initialize the local LLM, telling it to output JSON
    llm = OllamaLLM(model="qwen2:0.5b", temperature=0, format="json")

    # create the prompt template with format instructions
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert ESG compliance auditor. Your task is to compare an excerpt from a company's report against a specific ESG disclosure requirement. First, provide a general summary of the company's report. Then, determine the compliance status. Respond with a JSON object containing the compliance status, a brief reasoning, and the general summary."),
            ("human", """
            Please analyze the following texts:

            **Official ESG Requirement:**
            ---
            {esg_rule}
            ---

            **Company Report Excerpt:**
            ---
            {company_excerpt}
            ---

            {format_instructions}
            """)
        ]
    ).partial(format_instructions=parser.get_format_instructions()) # Inject the format instructions

    # chain with the parser
    classifier_chain = prompt | llm | parser
    
    print("compliance classifier chain with JSON parser created successfully.")
    return classifier_chain

# Test Block
if __name__ == '__main__':
    print("Testing the compliance classifier tool...")
    retriever = get_retriever()
    rule_query = "What is the requirement for disclosing GHG emissions from Scope 1?"
    retrieved_rule = retriever.invoke(rule_query)[0].page_content
    fake_company_text = "In 2024, our total direct greenhouse gas (GHG) emissions, which fall under Scope 1, were calculated to be 150,000 metric tons of CO2 equivalent. We are committed to transparency and have detailed our methodology in Appendix B."
    
    classifier = get_compliance_classifier()
    
    result = classifier.invoke({
        "esg_rule": retrieved_rule,
        "company_excerpt": fake_company_text
    })

    print("\n--- Classifier Test Result ---")
    print(f"ESG Rule Snippet: {retrieved_rule[:200]}...")
    print(f"Company Excerpt: {fake_company_text}")
    print("---")
    print(f"Compliance Status: {result['compliance_status']}")
    print(f"Reasoning: {result['reasoning']}")