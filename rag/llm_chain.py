from config.config import RAG_CONFIG
from config.prompt_config import RAG_PROMPT
from langchain_core.prompts import PromptTemplate
from config.config import LLM_CONFIG
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from volcenginesdkarkruntime import Ark
from langchain_community.llms import volcengine_maas

# 读取配置
API_KEY = LLM_CONFIG["API_KEY"]
BASE_URL = LLM_CONFIG["BASE_URL"]
MODEL = LLM_CONFIG["MODEL_NAME"]
TEMPERATURE = LLM_CONFIG["TEMPERATURE"]
MAX_TOKENS = LLM_CONFIG["MAX_TOKENS"]
PROMPT_TEMPLATE = RAG_PROMPT
# RETRIEVE_K = RAG_CONFIG["RETRIEVE_K"]


def get_llm():
    llm = ChatOpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        model=MODEL,  # 添加模型参数

    )
    return llm


def build_rag_chain(retriever):
    prompt = ChatPromptTemplate.from_template(
        template=PROMPT_TEMPLATE
    )
    llm=get_llm()
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain=(
        {
         "context": retriever | format_docs,
         "question": RunnablePassthrough(),
        }
        |prompt
        |llm
        |StrOutputParser()
        )
  
  
    return rag_chain
