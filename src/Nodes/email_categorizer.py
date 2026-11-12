from agents import AGENT_REGISTRY
from utils.state import GraphState

def email_categorizer_node(state: GraphState):
    """
    Node that categorizes the current email in the graph state.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        dict: Only the fields of the state that changed.
    """
    email = state.current_email
    if not email:
        return {"email_category": "No email to categorize"}
    result = AGENT_REGISTRY["email_categorizer"].invoke({"email": email.body})
    return {"email_category": result.category.value}
