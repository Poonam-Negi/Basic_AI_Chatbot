from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
model = init_chat_model("google/gemma-4-26b-a4b-it",
                        model_provider="openai", max_tokens=500)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an information extraction system.

Analyze the provided text and return:

1. Main Topic
2. Key Entities (people, organizations, products, locations)
3. Important Facts
4. Numbers/Dates Mentioned
5. Action Items (if any)
6. Risks/Issues (if any)
7. Final Summary

Rules:
- Keep only high-value information.
- Eliminate redundancy.
- Preserve factual accuracy.
- Use bullet points where appropriate.
- If a section is missing, write "Not mentioned".
- Do not invent information.
- Base all outputs strictly on the provided text.
"""
    ),
    (
        "human",
        """
Extract information from the following text:

{text}
"""
    ),
])

para = input("Enter Your Content Here:\n")
main_prompt = prompt.invoke({
    "text":para
})

response = model.invoke(main_prompt)
print(response.content)