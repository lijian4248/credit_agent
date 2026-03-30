from config.prompt_config import RAG_PROMPT
from config.config import LLM_CONFIG
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from models.schemas import CreditReport  # 引入第一步定义的数据模型
from langchain_core.output_parsers import PydanticOutputParser # 引入 Pydantic 解析器
from config.prompt_config import analysis_prompt, JSON_FORMAT_INSTRUCTIONS

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


def build_analysis_chain():
    """
    构建信贷分析链。
    
    该链的工作流程：
    1. 接收输入（规则、用户资料、格式说明）。
    2. 通过 analysis_prompt 格式化为提示词。
    3. 发送给 LLM 进行推理。
    4. 使用 PydanticOutputParser 将输出解析为 CreditReport 对象。
    
    Returns:
        LangChain Chain 对象
    """
    
    # 1. 初始化 Pydantic 解析器，绑定 CreditReport 模型
    # 解析器会自动根据 CreditReport 的字段生成 JSON 格式说明
    parser = PydanticOutputParser(pydantic_object=CreditReport)
    
    llm = get_llm()
    
    
    chain = analysis_prompt | llm | parser
    
    return chain