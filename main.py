from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define response structure
class ResearchResponse(BaseModel):
    topic: str = Field(description="The main topic that was researched")
    summary: str = Field(description="A summary of the research findings")
    sources: list[str] = Field(description="List of sources used for the research")
    tools_used: list[str] = Field(description="List of tools used for the research")

# Initialize Chat Model
llm = ChatGroq(
    api_key=GROQ_API_KEY, 
    model_name="llama3-8b-8192",
    temperature=0.2,  # Lower temperature for more structured responses
    max_tokens=1024
)

# Set up the output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create the agent prompt without Pydantic constraints
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a research assistant that helps users find information.
        Use the provided tools to search for information when needed.
        Be thorough and helpful in your responses."""),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create the agent with the tool
agent = create_tool_calling_agent(llm=llm, tools=[search_tool], prompt=agent_prompt)

# Create the executor
executor = AgentExecutor(agent=agent, verbose=True, tools=[search_tool])

# Run the agent with user input
query = input("🔍 What can I help you with in searching? ")

try:
    # Get raw search results
    raw_response = executor.invoke({"query": query})
    raw_result = raw_response["output"]
    
    print("\nPreparing structured response...")
    
    # Manually create a structured response
    structured_data = {
        "topic": query,
        "summary": raw_result,
        "sources": ["Web search"],
        "tools_used": ["DuckDuckGoSearch"]
    }
    
    # Create a ResearchResponse object
    response_obj = ResearchResponse(**structured_data)
    
    # Print the structured response
    print("\n=== STRUCTURED RESPONSE ===")
    print(f"Topic: {response_obj.topic}")
    print(f"Summary: {response_obj.summary}")
    print(f"Sources: {', '.join(response_obj.sources)}")
    print(f"Tools Used: {', '.join(response_obj.tools_used)}")
    print("===========================")
    
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