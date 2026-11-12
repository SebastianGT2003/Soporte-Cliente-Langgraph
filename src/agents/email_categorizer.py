from promps import EMAIL_CATEGORIZER_PROMPT
from structured_outputs import EmailCategorizationOutput
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def categorize_email():
    email_categorizer_promp = PromptTemplate(
        template=EMAIL_CATEGORIZER_PROMPT,
        input_variables=["email"]
    )
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    return email_categorizer_promp | llm.with_structured_output(EmailCategorizationOutput)