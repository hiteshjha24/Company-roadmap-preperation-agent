AI Interview Roadmap Generator Agent

Project for: GENAI Task - Research Agent

This project is an advanced AI Agent built using the Gemini API and LangChain, designed to cut through the noise and provide targeted, structured interview preparation plans. It transforms a generic Job Description (JD) into a clear, actionable roadmap, integrating both the specific requirements of the role and the public knowledge of the target company's interview process.

The Problem Solved

Preparing for a tech interview is often overwhelming. Candidates typically have to:

Manually dissect a Job Description to find keywords.

Independently research the company's specific interview rounds (e.g., "Does Google still do 5 coding rounds?").

Synthesize this information into a logical study plan.

This agent automates the entire process, providing a data-driven, structured JSON output ready for use.

Technology Stack

Core Logic: Python

LLM: Gemini API (gemini-2.5-flash-preview-09-2025)

Orchestration & Tooling: LangChain Expression Language (LCEL)

Structured Output: Pydantic (ensuring reliable JSON schema)

Dependency Management: python-dotenv

Agent Architecture & Reasoning Flow

The core of this project lies in its ability to execute a multi-step reasoning process, combining internal analysis with external, real-time data using the Google Search tool.

1. The Input

The agent is provided with three mandatory inputs: Company Name, Job Role, and the raw Job Description (JD) text.

2. Job Description Parsing (Internal Analysis)

The agent performs granular analysis to extract skills and map them to foundational domains:

Skill Extraction: Finds explicit requirements (e.g., "Microservices," "Python," "Data Structures").

Keyword Mapping: Translates extracted skills into generalized preparation topics (e.g., "REST APIs" → "Backend Development," "Binary Trees" → "Data Structures & Algorithms").

3. Company & Difficulty Prediction (External Grounding)

The agent strategically uses the Google Search tool to bridge the gap between the JD and reality:

Tool Use: The agent is prompted to query for "[{Company} {Role} interview process and difficulty]".

Information Gathering: It gathers data on typical round types (MCQ, Coding, System Design, Behavioral) and infers the overall complexity level ("Easy," "Medium," or "Hard").

4. Roadmap Synthesis & Structured Output

The agent synthesizes the internal skill map (Step 2) and external interview data (Step 3) to fill a strict Pydantic JSON schema, guaranteeing a clean and standardized result.

JSON Field

Source of Information

rounds

Inferred from Google Search data & JD topics.

topics (per round)

Specific skills from JD, categorized into rounds.

difficulty

Inferred from Company/Role profile (e.g., FAANG = Hard).

recommended_order

Logical sequence for studying based on domain importance.

How to Run the Agent

Prerequisites

Clone this repository.

Install dependencies:

pip install langchain-google-genai pydantic python-dotenv

Execution
python roadmap_agent.py


Example Output (JSON)

The final output is a beautiful, structured JSON object:

<<----Google---->>


{
    "company": "Google",
    "role": "Software Development Engineer (SDE) - L3",
    "rounds": [
        {
            "type": "Technical Coding",
            "topics": ["Data Structures and Algorithms", "Greedy Algorithms", "Dynamic Programming", "Graphs"]
        },
        {
            "type": "System Design",
            "topics": ["Distributed Systems", "Scaling", "Microservices Architecture", "Load Balancing"]
        },
        {
            "type": "Behavioral",
            "topics": ["Googliness & Leadership", "Communication", "Conflict Resolution"]
        }
    ],
    "difficulty": "Hard",
    "recommended_order": [
        "Data Structures and Algorithms",
        "System Design Fundamentals",
        "Python/Go Language Syntax",
        "Behavioral Interview Preparation"
    ]
}



<<----Amazon---->>

{
    "company": "Amazon",
    "role": "Applied Scientist",
    "rounds": [
        {
            "type": "Screening/Technical Deep Dive (Theory)",
            "topics": [
                "Probability and Statistics",
                "Linear Algebra",
                "Optimization Techniques (e.g., SGD, Adam)",
                "Classic ML Algorithms (e.g., SVM, Boosting)",
                "Deep Learning Architectures (CNNs, RNNs, Transformers)",
                "Model Optimization and Regularization"
            ]
        },
        {
            "type": "Coding/Technical Interview",
            "topics": [
                "Data Structures (Arrays, Hash Maps, Trees)",
                "Algorithms (Sorting, Searching, Dynamic Programming)",
                "Time and Space Complexity Analysis",
                "Implementation of ML components (e.g., custom loss functions, model layers)",
                "Python proficiency"
            ]
        },
        {
            "type": "ML System Design",
            "topics": [
                "Designing and scaling a large-scale ML system (e.g., recommendation engine, search ranking)",
                "Data pipelines and feature engineering at scale",
                "Model deployment strategies (A/B testing, canary releases)",
                "MLOps tools (SageMaker, Kubeflow)",
                "Monitoring and logging in production"
            ]
        },
        {
            "type": "Cloud/Deployment Deep Dive",
            "topics": [
                "AWS services (SageMaker, S3, EC2, Lambda)",
                "Deployment strategies for deep learning models",
                "Latency and throughput optimization",
                "Cost management for ML infrastructure"
            ]
        },
        {
            "type": "Behavioral/Bar Raiser",
            "topics": [
                "Amazon Leadership Principles (e.g., Ownership, Invent and Simplify, Deliver Results)",
                "Situational questions based on past projects (STAR method)",
                "Handling ambiguity and failure in research/development",
                "Deep dive into publication record/PhD thesis"
            ]
        }
    ],
    "difficulty": "Hard",
    "recommended_order": [
        "Machine Learning Fundamentals & Deep Learning Theory",
        "Coding & Data Structures/Algorithms",
        "ML System Design & MLOps",
        "AWS & Cloud Deployment",
        "Behavioral & Leadership Principles"
    ]
}