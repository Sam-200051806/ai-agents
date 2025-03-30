from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Chat Model
llm = ChatGroq(
    api_key=GROQ_API_KEY, 
    model_name="llama3-8b-8192",
    temperature=0.7,
    max_tokens=1024
)

# Create a simpler prompt without Pydantic parsing
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a research assistant that helps users find information.
        Use the provided tools to search for information when needed.
        Be concise and helpful in your responses."""),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create the agent with the tool
agent = create_tool_calling_agent(llm=llm, tools=[search_tool], prompt=prompt)

# Create the executor
executor = AgentExecutor(agent=agent, verbose=True, tools=[search_tool])

# Run the agent with user input
query = input("🔍 What can I help you with in searching? ")

try:
    response = executor.invoke({"query": query})
    print("\nFinal Answer:")
    print(response["output"])
except Exception as e:
    print(f"Error occurred: {str(e)}")
    print("Try searching for something different or check your API key.")
# print(response) #it will print the raw response
# Extract the structured response
# structured_response = parser.parse(response["output"][0]["text"])
# print(structured_response)
# if isinstance(response, dict):  # Ensure it's a dictionary
#     if "output" in response and isinstance(response["output"], list) and len(response["output"]) > 0:
#         if "text" in response["output"][0]:
#             structured_response = parser.parse(response["output"][0]["text"])
#         else:
#             print("Error: 'text' key missing in response['output'][0]")
#     elif "output" in response:  # Different structure
#         print("Unexpected structure in response['output']: ", response["output"])
#     else:
#         print("Error: 'output' key missing in response")
# else:
#     print("Error: Response is not a dictionary")