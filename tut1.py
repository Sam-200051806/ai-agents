from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


information = """
    Lionel Andrés "Leo" Messi[note 1] (Spanish pronunciation: [ljoˈnel anˈdɾes ˈmesi] ⓘ; born 24 June 1987) is an Argentine professional footballer who plays as a forward for and captains both Major League Soccer club Inter Miami and the Argentina national team. Widely regarded as one of the greatest players of all time, Messi set numerous records for individual accolades won throughout his professional footballing career such as eight Ballon d'Or awards and eight times being named the world's best player by FIFA.[note 2] He is the most decorated player in the history of professional football having won 45 team trophies,[note 3] including twelve Big Five league titles, four UEFA Champions Leagues, two Copa Américas, and one FIFA World Cup. Messi holds the records for most European Golden Shoes (6), most goals in a calendar year (91), most goals for a single club (672, with Barcelona), most goals (474), hat-tricks (36) and assists (192) in La Liga, most assists (18) and goal contributions (32) in the Copa América, most goal contributions (21) in the World Cup, most international appearances (191) and international goals (112) by a South American male, and the second-most in the latter category outright. A prolific goalscorer and creative playmaker, Messi has scored over 850 senior career goals and has provided over 380 assists for club and country.
"""
if __name__ == "__main__":
    print("Initializing ChatGroq model...")
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    summary_template = """
    given the information {information} about the person from I want to you create few things that I will mention below:
      1. A short summary
      2. two insteresting facts in under 5 words
    """
    summary_promt_template = PromptTemplate(
        template=summary_template,
    )
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0.2, 
        max_tokens=1024 
    )
    chain = summary_promt_template | llm
    result = chain.invoke(
        input={"information": information}
    )
    print(result.content)
   