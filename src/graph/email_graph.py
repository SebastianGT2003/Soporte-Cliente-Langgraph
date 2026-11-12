from langgraph.graph import START, StateGraph
from Nodes import NODES
from utils.state import GraphState

class EmailSupportGraph():
    """
    A graph that listens for new emails and categorizes them.
    """
    def __init__(self):
        workflow = StateGraph(GraphState)
        workflow.add_node("load_emails", NODES["email_listener"])
        workflow.add_node("categorize_email", NODES["email_categorizer"])

        workflow.add_edge(START, "load_emails")
        workflow.add_edge("load_emails", "categorize_email")

        self.graph = workflow.compile()
