import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("✅ Import successful")
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor , create_react_agent
from langchain import hub
from help_tools.tool import get_profile # this is the tool that is used to search the web for current information and it is used with langchain
# from help_tools.tool import get_profile
#it creates a react agent that can do reasoning things in this and provide me the link of the profile page of the person in linkedIn
# it uses the groq model to do reasoning things in this and provide me the link of the profile page of the person in linkedIn
def lookup(name: str) -> str:
    
    llm = ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model_name="llama3-8b-8192",
        temperature=0.2, 
        max_tokens=1024 
    )
    template = """"
        given the name {name} of the person I want you to find the LinkedIn profile URL of the person.
        your answer should be in the format of a URL.
    """
    prompt_template = PromptTemplate(
        input_variables=["name"],
        template=template,
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile,
            description="Useful for searching the web for current information. Input should be a search query. it is useful when you get thr LinkedIn page URL. "
        )
    ]
    react_prompt = hub.pull("hwchase17/react") # load the react prompt from hub and do reasoning things in this 
    agent = create_react_agent(llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent,verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name=name)}
    )
    url = result["output"]
    return url


if __name__ == "__main__":
    linkedin_url = lookup("Riya Arora abes Engineering college")
    print(linkedin_url)


# make llm -> prompt template -> tools -> react promt(hwchase17/react) -> agent -> agent executor -> and then results