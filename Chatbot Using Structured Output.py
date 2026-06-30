from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

from langchain.chat_models import init_chat_model
model = init_chat_model("google/gemma-4-26b-a4b-it",
                        model_provider="openai", max_tokens=500)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

class content(BaseModel): #schema
    title:str
    key_entities:List[str]
    imp_facts: List[str]
    dates: Optional[int]
    risks: List[str]
    actions: Optional[str]
    final: str

parser = PydanticOutputParser(pydantic_object=content)


prompt = ChatPromptTemplate.from_messages([
    ('system','''
     Extract information from the paragraph
     {format_instructions}
     '''),
     ('human',"{text}"
)
])

para = input("Enter Your Content Here:\n")
main_prompt = prompt.invoke({
    "text":para,
    "format_instructions": parser.get_format_instructions()
})


response = model.invoke(main_prompt)
data = parser.parse(response.content)
print(data)