from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from third_party.linkedin import linkedin_profile
from help_tools.tool import get_profile # this is the tool that is used to search the web for current information and it is used with langchain
if __name__ == "__main__":
    # Initialize the ChatGroq model
    print("Initializing ChatGroq model...")
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    summary_template = """
    given the LinkedIn information {information} about the person from I want to you create few things that I will mention below:
      1. A short summary
      2. two insteresting facts in under 5 words
      3. provide me link of the profile image
    """
    summary_promt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0.2, 
        max_tokens=1024 
    )
    linkedin_data = linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/sambhav-seth-bbb440258/",mock=True)
    chain = summary_promt_template | llm 
    result = chain.invoke(
        input={"information": linkedin_data}
    )
    print(result.content)
   



