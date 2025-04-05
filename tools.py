from langchain_community.tools import DuckDuckGoSearchResults 
from langchain.tools import Tool

# Initialize DuckDuckGo search with more reasonable parameters
search = DuckDuckGoSearchResults(
    max_results=3,  # Limit results to avoid overwhelming the model
)

# Create the search tool
search_tool = Tool(
    name="web_search",
    func=search.run,
    description="Useful for searching the web for current information. Input should be a search query."
)

