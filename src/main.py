from graph.email_graph import EmailSupportGraph
from utils.state import Email

def main():
    print("Starting Langraph Email Support Workflow!")
    # El nodo "load_emails" se encarga de traer el correo desde Gmail.
    initial_state = {
        "current_email": None,
        "email_category": ""
    }
    workflow= EmailSupportGraph()
    graph = workflow.graph
    for output in graph.stream(initial_state):
        for _, value in output.items():
            current_email = value.get("current_email")
            if isinstance(current_email, Email):
                print(current_email.body)
            print(value.get("email_category", "No category determined"))

if __name__ == "__main__":
    main()