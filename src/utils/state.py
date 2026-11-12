from pydantic import BaseModel, Field


class Email(BaseModel):
    """
    Represents an email with its relevant details.
    """
    id: str = Field(..., description="The unique identifier of the email.")
    subject: str = Field(..., description="The subject of the email.")
    sender: str = Field(..., description="The sender of the email.")
    date: str = Field(..., description="The date the email was sent.")
    body: str = Field(..., description="The body of the email.")

class GraphState(BaseModel):
    """
    Represents the state of a graph.
    """
    current_email: Email | None = Field(None, description="The current email in the graph.")
    email_category: str = Field("", description="The category of the current email.")