from langchain_community.tools.tavily_search import TavilySearchResults #this is the tool that is used to search the web for current information and it is used with langchain

def get_profile(name: str):
    search = TavilySearchResults()
    results = search.run(name)
    summary = "\n\n".join([f"{r['title']} - {r['url']}\n{r['content']}" for r in results])
    return summary
                                                                                                     