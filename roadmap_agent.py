from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
import json
from typing import List, Any
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()

class InterviewRound(BaseModel):
    """Schema for a single interview round."""
    type: str = Field(
        description="Type of interview round, e.g., 'MCQ', 'Coding', 'HR', 'System Design', 'Managerial'."
    )
    topics: List[str] = Field(
        description="List of key topics covered in this specific round. Topics should be specific (e.g., 'Dynamic Programming', 'Load Balancing')."
    )

class PreparationRoadmap(BaseModel):
    """The final structured roadmap output schema."""
    company: str = Field(description="The name of the company derived from the input.")
    role: str = Field(description="The job role derived from the input.")
    rounds: List[InterviewRound] = Field(
        description="List of all predicted interview rounds, including topics, inferred from the JD and company research."
    )
    difficulty: str = Field(
        description="Predicted difficulty level of the entire interview process: 'Easy', 'Medium', or 'Hard'."
    )
    recommended_order: List[str] = Field(
        description="Suggested order of preparation topics/domains, e.g., ['Data Structures and Algorithms', 'System Design Fundamentals', 'Behavioral Communication']."
    )

@tool
def google_search(query: str) -> str:
    """
    Use this tool to search for real-time, external information about a company's interview process,
    typical interview rounds, or required skills/tools.
    """
    print(f"\n--- TOOL CALLED: Searching Google for: {query} ---")
    return "Search results for the company's interview process are being provided to the model."

def create_roadmap_agent(llm_name: str = "gemini-2.5-flash-preview-09-2025") -> Any:
    """
    Initializes the Gemini model, defines the agent prompt, and creates the chain.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "The GEMINI_API_KEY environment variable is not set. "
            "Ensure it is defined in your .env file and loaded correctly."
        )

    try:
        llm = ChatGoogleGenerativeAI(
            model=llm_name, 
            temperature=0.2, 
            google_api_key=api_key
        )
        
        llm_with_tools = llm.bind_tools([google_search], tool_config={"google_search": {"max_usage_count": 2}})
        structured_llm = llm_with_tools.with_structured_output(schema=PreparationRoadmap)

        system_instruction = f"""
        You are a world-class AI Career Preparation Agent. Your task is to generate a comprehensive, structured interview preparation roadmap.
        
        Follow these mandatory steps:
        1. Parse the Job Description (JD) : Extract required technical skills, tools, and responsibilities. Map these extracted keywords to general preparation topics (e.g., 'TensorFlow' -> 'Deep Learning', 'REST API' -> 'Backend Development').
        2. Company Research: Use the `Google Search` tool to gather current, real-world information about the interview process, round types, and expected difficulty for the given Company and Role. This is mandatory for grounding the analysis.
        3. Synthesize & Structure : Combine the JD analysis (Step 1) and external research (Step 2) to accurately fill the required JSON schema ({PreparationRoadmap.__name__}).
            - Rounds : Predict the typical rounds (e.g., Coding, System Design) and populate the most likely topics for each round.
            - Difficulty : Predict the overall difficulty ('Easy', 'Medium', or 'Hard').
            - Recommended Order : Suggest a logical, sequential order of preparation domains.
        
        The final output MUST be a valid JSON object matching the requested schema.
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_instruction),
                ("user", "Company: {company}\nRole: {role}\nJob Description:\n---\n{job_description}\n---")
            ]
        )
        roadmap_chain = prompt_template | structured_llm
        return roadmap_chain
    except Exception as e:
        print(f"Error during LLM or Chain initialization: {e}")
        return None
    
if __name__ == "__main__":
    sample_company = "Google"
    sample_role = "Software Development Engineer (SDE) - L3"
    sample_jd = """
    We are looking for a Software Engineer to join our core infrastructure team.
Responsibilities include designing, developing, and deploying high-volume, low-latency services
using Python and Go. Candidates must have a strong foundation in Data Structures and Algorithms (DSA),
System Design principles (microservices, distributed caches), and expertise in designing and
implementing RESTful APIs. Experience with cloud platforms (GCP, AWS) is a plus.
Excellent communication skills and behavioral fit are essential.
    """

    print("--- Interview Roadmap Generation Agent Initialized ---")
    print(f"Analyzing Job Description for {sample_company} - {sample_role}...")

    try:
        agent_chain = create_roadmap_agent()

        if agent_chain:
            agent_input = {
                "company": sample_company,
                "role": sample_role,
                "job_description": sample_jd
            }

            result: PreparationRoadmap = agent_chain.invoke(agent_input)

            print("\n--- Generation Complete: Final Roadmap (JSON) ---\n")
            
            print(json.dumps(result.model_dump(), indent=4))
            
            output_filepath = "roadmap_output.json"
            with open(output_filepath, 'w') as f:
                json.dump(result.model_dump(), f, indent=4)
            print(f"\nSuccessfully saved roadmap to {output_filepath}")

    except ValueError as ve:
        print(f"\nFATAL ERROR: {ve}")
        print("Error in gemini api key")

    except Exception as e:
        print(f"\n--- An unexpected error occurred during execution ---")
        print(f"Error: {e}")
