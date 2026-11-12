from pydantic import BaseModel, Field
from enum import Enum

class EmailCategory(str, Enum):
    product_inquiry = "Product Inquiry"
    customer_complaint = "Customer Complaint"
    customer_feedback = "Customer Feedback"
    unrelated = "Unrelated"

class EmailCategorizationOutput(BaseModel):
    category: EmailCategory = Field(..., description="The category of the email based on its content.")
    account_id: str | None = Field(None, description="The account ID mentioned in the email, if any.")
    product: str | None = Field(None, description="The product mentioned in the email, if any.")
    urgency: str | None = Field(None, description="The urgency level of the email, if any.")