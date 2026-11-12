from utils.state import GraphState
from utils.gmail_utils import get_most_recent_email

def email_listener_node(state: GraphState):
    """
    Node that listens for new emails and updates the graph state accordingly.

    Args:
        state (GraphState): The current state of the graph.
    """
    email = get_most_recent_email()
    return {"current_email": email}
