from langchain_community.tools import DuckDuckGoSearchResults 
from langchain.tools import Tool


search = DuckDuckGoSearchResults(
    max_results=3,  
)


search_tool = Tool(
    name="web_search",
    func=search.run,
    description="Useful for searching the web for current information. Input should be a search query."
)

