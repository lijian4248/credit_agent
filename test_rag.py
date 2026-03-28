import warnings
warnings.filterwarnings('ignore')

# 导入我们写好的核心模块
from rag.embeddings import get_bge_embeddings
from rag.faiss_store import build_faiss_vector_db
from config.config import RAG_CONFIG
from rag.llm_chain import build_rag_chain
from zai import ZhipuAiClient
from config.config import LLM_CONFIG
from rag.llm_chain import build_rag_chain
from config.prompt_config import RAG_PROMPT
import zai,os
# 确保 PWD 环境变量存在，对于 Windows，可以设置为当前工作目录
if not os.environ.get('PWD'):
    os.environ['PWD'] = os.getcwd()

API_KEY = LLM_CONFIG["API_KEY"]
RAG_PROMPT_TEMPLATE=RAG_PROMPT

# client = ZhipuAiClient(api_key=API_KEY)
# llm=LangChainZhipuAI
# response = client.chat.completions.create(
#     model="glm-5",
#     messages=[
#         {"role": "user", "content": "你好，请介绍一下自己, Z.ai!"}
#     ]
# )
# print(response.choices[0].message.content)

print("🔧 加载向量模型...")
embeddings = get_bge_embeddings()

print("📦 加载向量库...")
db = build_faiss_vector_db(embeddings,True)

print("🔗 创建对话链...")
retriever = db.as_retriever(search_kwargs={"k": RAG_CONFIG["RETRIEVE_K"]})
rag_chain = build_rag_chain(retriever)

# ===================== 对话 =====================
print("\n🎉 智能问答系统已启动！")
while True:
    question = input("\n请输入问题（输入 q 退出）：")
    if question.lower() == "q":
        break
    
        # ===================== 在这里打印完整内容 =====================
    docs = retriever.invoke(question)
    context_content = "\n\n".join([doc.page_content for doc in docs])
    full_prompt = RAG_PROMPT_TEMPLATE.format(
        context=context_content,
        question=question
    )

    print("\n" + "="*80)
    print("📤 完整发送给大模型的 PROMPT")
    print("="*80)
    print(full_prompt)
    print("="*80 + "\n")

    response = rag_chain.invoke(question)
    print("\n🤖 回答：", response)
  










# print(zai.__version__)
# # ====================== 测试开始 ======================
# print("🔧 正在加载 BGE 向量模型...")
# embeddings = get_bge_embeddings()

# print("\n🚀 开始构建 FAISS 向量库...")
# # 第一次运行：自动全量构建
# # 后面运行：自动增量更新
# db = build_faiss_vector_db(embeddings)

# print("\n✅ 向量库准备完成！测试检索功能...")

# # 测试检索：随便写一个问题
# query = "黑名单与失信规则是什么"
# retriever = db.as_retriever(search_kwargs={"k": 2})
# result = retriever.invoke(query)

# print("\n🔍 检索到的内容：")
# for i, doc in enumerate(result):
#     print(f"\n--- 结果 {i+1} ---")
#     print(doc.page_content)
# ======================================================