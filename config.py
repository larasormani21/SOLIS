from langchain_openai import ChatOpenAI
import os, dotenv

dotenv.load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY", "")
lm_studio_host = os.getenv("LM_STUDIO_HOST", "")
lm_studio_api_key = os.getenv("LM_STUDIO_API_KEY", "")
tavily_api_key = os.getenv("TAVILY_API_KEY", "")
mongo_uri = os.getenv("MONGO_URI", "")
testing_mode = os.getenv("TESTING_MODE", False)
testing_mode_agents = os.getenv("TESTING_MODE_AGENTS", "").split(",")

def build_llm_from_model_and_temperature(model_name: str, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=lm_studio_host,
        api_key=lm_studio_api_key,
        model=model_name,
        temperature=temperature,
    )
