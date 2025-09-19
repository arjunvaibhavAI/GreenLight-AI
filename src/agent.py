from typing import TypedDict, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END

# import our existing tools
from .tools.retriever import get_retriever
from .tools.classifier import get_compliance_classifier

# Agent's State
# this is the "notepad" our agent will use to keep track of its work.
class AuditState(TypedDict):
    company_report_text: str  # The full text of the uploaded company report
    topics: List[str]         # A list of key ESG topics to audit (e.g., ["Emissions", "Labor Practices"])
    current_topic: str        # The topic currently being audited
    audit_findings: List[str] # A list of formatted strings summarizing the findings
    error: str                # To store any errors that occur


# Agent's Nodes
# Initialize our tools once to be used by the nodes
try:
    retriever = get_retriever()
    classifier = get_compliance_classifier()
    print("tools loaded successfully for the agent.")
except Exception as e:
    print(f"Error loading tools: {e}")
    retriever = None
    classifier = None

def start_audit(state: AuditState) -> AuditState:
    """
    Node: audit process, hardcode the topics.
    """
    print("--- Starting Audit ---")
    state["topics"] = ["GHG emissions"] 
    state["audit_findings"] = []
    return state

def process_topic(state: AuditState) -> AuditState:
    """
    Node: takes the next topic from the list, runs it through the tools,
    and handles potential errors gracefully.
    """
    if not state["topics"]:
        print("--- All topics processed ---")
        return state
    
    current_topic = state["topics"].pop(0)
    state["current_topic"] = current_topic
    print(f"\n--- Processing Topic: {current_topic} ---")
    
    try:
        # retriever to find the official ESG rule for this topic
        esg_rule = retriever.invoke(current_topic)[0].page_content
        company_excerpt = state["company_report_text"]

        # classifier tool to get a judgment
        print("   Invoking classifier...")
        result = classifier.invoke({
            "esg_rule": esg_rule,
            "company_excerpt": company_excerpt
        })
        
        # Format and save the finding from the dictionary
        finding = (
            f"**Topic:** '{current_topic}'\n\n"
            f"**Status:** {result['compliance_status']}\n\n"
            f"**Reasoning:** {result['reasoning']}\n\n"
            f"**General Summary of Report:**\n{result['summary']}"
        )
        print(f"   Finding Recorded for '{current_topic}'")
        state["audit_findings"].append(finding)

    except Exception as e:
        print(f"   ERROR processing topic '{current_topic}': {e}")
        error_finding = f"Topic: '{current_topic}' | Status: Error | Reasoning: Failed to get a valid structured response from the language model."
        state["audit_findings"].append(error_finding)

    return state

# graph

def should_continue(state: AuditState) -> str:
    """
    If there are more topics it continues the loop.
    """
    if state["topics"]:
        return "continue"
    else:
        return "end"

# create a graph
workflow = StateGraph(AuditState)

# add the nodes
workflow.add_node("start_audit", start_audit)
workflow.add_node("process_topic", process_topic)

# set the entry point
workflow.set_entry_point("start_audit")

# add the edges
workflow.add_conditional_edges(
    "start_audit",
    should_continue,
    {
        "continue": "process_topic",
        "end": END
    }
)
workflow.add_conditional_edges(
    "process_topic",
    should_continue,
    {
        "continue": "process_topic",
        "end": END
    }
)

# compile the graph into a runnable app
app = workflow.compile()
print("LangGraph workflow compiled successfully.")