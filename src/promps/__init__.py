from .agents import EMAIL_CATEGORIZER
from .tasks import EMAIL_CATEGORIZER_TASK


EMAIL_CATEGORIZER_PROMPT = f"{EMAIL_CATEGORIZER}\n\n{EMAIL_CATEGORIZER_TASK}"

def main() -> None:
    print("Hello from soporte-cliente!")
