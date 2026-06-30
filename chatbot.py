from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

model = init_chat_model("google/gemma-4-26b-a4b-it",
                        model_provider="openai", max_tokens=50)

print("_"*50+ "Simple AI Chatbot"+ "_"*50)
print()
print("Choose mode of AI agent you wanna use: ")
print("1: Funny Mode")
print("2: Angry Mode")
print("3: Sad Mode")
print()

try:
    choice = int(input("Enter AI Mode (1, 2, or 3): "))
except ValueError:
    print("Invalid input! Defaulting to Helpful Mode.")
    choice = 0

if choice == 1:
    system_prompt = "You are a funny AI assistant."
    print("😄 Funny Mode activated!")
elif choice == 2:
    system_prompt = "You are an angry AI assistant who responds rudely."
    print("😡 Angry Mode activated!")
elif choice == 3:
    system_prompt = "You are a sad AI assistant who sounds melancholic."
    print("😢 Sad Mode activated!")
else:
    system_prompt = "You are a helpful AI assistant."
    print("🤖 Helpful Mode activated!")

messages =[
        SystemMessage(content=system_prompt)
]

while True:
        prompt = input("User: ").strip()
        if prompt.lower()=='exit':
                break
        
        if not prompt:
               continue
        
        messages.append(HumanMessage(content=prompt))
        try:
            response = model.invoke(messages)
            messages.append(AIMessage(content=response.content))
            print(f"Bot: {response.content}\n")

        except Exception as e:
            print("Error:", e)
            print("Please try again.\n")

print("\n👋 Thanks for chatting!")   

