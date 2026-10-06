# from dotenv import load_dotenv
# from langchain_mistralai import ChatMistralAI
# from langchain_mistralai.embeddings import MistralAIEmbeddings
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
# from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace


from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
)
# loading the model 
# llm = ChatMistralAI(model="mistral-medium-3-5")


# llm2 = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-V4.1-Flash",temperature=0.4,max_new_tokens=1000)
# llm = ChatHuggingFace(llm = llm2)


# llm = ChatNVIDIA( model="nvidia/nemotron-3.5-lightning-30b-a3b",
#   temperature=0.3,
#   chat_template_kwargs={"enable_thinking":True})

# #making embedding model
# embedding = MistralAIEmbeddings(model="mistral-embed")


# from langchain_nvidia_ai_endpoints import ChatNVIDIA

# models = ChatNVIDIA.get_available_models()

# for model in models:
#     if model.supports_tools:
#         print(model.id)