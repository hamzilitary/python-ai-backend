from langchain_ollama import ChatOllama

model = ChatOllama(
    model = "gemma3"
)

response = model.invoke("Explain what a python dictionary is on one sentence.")

print(response)
print(type(response))
print(response.content)