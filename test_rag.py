import warnings
warnings.filterwarnings('ignore')

# 导入我们写好的核心模块
from rag.embeddings import get_bge_embeddings
from rag.faiss_store import build_faiss_vector_db
from config.config import RAG_CONFIG
from rag.llm_chain import build_rag_chain
from config.config import LLM_CONFIG
from rag.llm_chain import build_rag_chain
from config.prompt_config import RAG_PROMPT
import os
# 确保 PWD 环境变量存在，对于 Windows，可以设置为当前工作目录
if not os.environ.get('PWD'):
    os.environ['PWD'] = os.getcwd()

API_KEY = LLM_CONFIG["API_KEY"]
RAG_PROMPT_TEMPLATE=RAG_PROMPT




import sys
import os

# 将项目根目录添加到路径，以便导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.llm_chain import build_analysis_chain
from utils.rules_loader import get_all_rules
from models.schemas import CreditReport

def main():
    print("=== 正在初始化分析链 ===")
    
    # 1. 构建分析链
    chain = build_analysis_chain()
    
    # 2. 加载规则
    static_rules, custom_rules = get_all_rules()
    
    # 3. 准备模拟的用户资料
    # 这里我们模拟一个有风险的用户
    mock_user_profile = """
    客户姓名:张三
    年龄:45岁
    职业:餐饮店老板
    月收入:15000元
    负债情况:目前有两笔贷款在还,每月还款额总计12000元。
    征信记录:近2年内有4次逾期记录,其中一次超过60天。
    申请金额:50万元
    """
    
    # 4. 准备输入字典
    # 注意:我们需要手动传入 format_instructions，或者让 parser 处理
    # 在这里我们手动获取并传入，以确保清晰
    from langchain_core.output_parsers import PydanticOutputParser
    parser = PydanticOutputParser(pydantic_object=CreditReport)
    
    inputs = {
        "rules": static_rules,
        "custom_rules": custom_rules,
        "user_profile": mock_user_profile,
        "format_instructions": parser.get_format_instructions()
    }
    
    print("=== 正在调用大模型进行分析 ===")
    print(f"输入资料长度: {len(mock_user_profile)} 字符")
    
    try:
        # 5. 调用链
        report: CreditReport = chain.invoke(inputs)
        
        # 6. 打印结果
        print("\n=== 分析成功！报告如下 ===")
        print(f"风险等级: {report.risk_level}")
        print(f"信用评分: {report.score}")
        print(f"风险点: {', '.join(report.risk_points)}")
        print(f"建议: {', '.join(report.suggestions)}")
        print(f"详细分析:\n{report.analysis_details}")
        
        # 验证类型
        assert isinstance(report, CreditReport)
        print("\n[测试通过] 返回类型正确，为 CreditReport 对象。")
        
    except Exception as e:
        print(f"\n[错误] 分析失败: {e}")

if __name__ == "__main__":
    main()



# from utils.rules_loader import get_all_rules

# # 获取规则
# static_rules, custom_rules = get_all_rules()

# print("=== 静态规则预览 ===")
# print(static_rules[:200] + "...") # 只打印前200个字符

# print("\n=== 自定义规则预览 ===")
# print(custom_rules)



# from config.prompt_config import analysis_prompt, JSON_FORMAT_INSTRUCTIONS

# # 模拟输入数据
# inputs = {
#     "rules": "规则1:逾期超过3次为高风险。",
#     "custom_rules": "自定义规则:餐饮行业需特别关注。",
#     "user_profile": "用户张三,餐饮行业老板,近半年逾期4次。",
#     "format_instructions": JSON_FORMAT_INSTRUCTIONS
# }

# # 生成最终发送给 LLM 的消息
# prompt_value = analysis_prompt.invoke(inputs)

# # 打印查看内容
# print("=== 最终提示词内容 ===")
# for msg in prompt_value.to_messages():
#     print(f"{msg.type}: {msg.content}")





# from models.schemas import CreditReport

# # 模拟一个 LLM 可能返回的 JSON 数据
# json_data = {
#     "risk_level": "高",
#     "risk_points": ["征信报告显示近24个月逾期6次", "负债率超过70%"],
#     "suggestions": ["建议降低授信额度", "要求增加担保物"],
#     "analysis_details": "用户征信记录较差，且负债压力巨大，违约风险极高。",
#     "score": 30
# }

# # 尝试解析
# try:
#     report = CreditReport(**json_data)
#     print("解析成功！")
#     print(f"风险等级: {report.risk_level}")
#     print(f"评分: {report.score}")
# except Exception as e:
#     print(f"解析失败: {e}")




# print("🔧 加载向量模型...")
# embeddings = get_bge_embeddings()

# print("📦 加载向量库...")
# db = build_faiss_vector_db(embeddings,True)

# print("🔗 创建对话链...")
# retriever = db.as_retriever(search_kwargs={"k": RAG_CONFIG["RETRIEVE_K"]})
# rag_chain = build_rag_chain(retriever)

# # ===================== 对话 =====================
# print("\n🎉 智能问答系统已启动！")
# while True:
#     question = input("\n请输入问题（输入 q 退出）:")
#     if question.lower() == "q":
#         break
    
#         # ===================== 在这里打印完整内容 =====================
#     docs = retriever.invoke(question)
#     context_content = "\n\n".join([doc.page_content for doc in docs])
#     full_prompt = RAG_PROMPT_TEMPLATE.format(
#         context=context_content,
#         question=question
#     )

#     print("\n" + "="*80)
#     print("📤 完整发送给大模型的 PROMPT")
#     print("="*80)
#     print(full_prompt)
#     print("="*80 + "\n")

#     response = rag_chain.invoke(question)
#     print("\n🤖 回答:", response)
  










# print(zai.__version__)
# # ====================== 测试开始 ======================
# print("🔧 正在加载 BGE 向量模型...")
# embeddings = get_bge_embeddings()

# print("\n🚀 开始构建 FAISS 向量库...")
# # 第一次运行:自动全量构建
# # 后面运行:自动增量更新
# db = build_faiss_vector_db(embeddings)

# print("\n✅ 向量库准备完成！测试检索功能...")

# # 测试检索:随便写一个问题
# query = "黑名单与失信规则是什么"
# retriever = db.as_retriever(search_kwargs={"k": 2})
# result = retriever.invoke(query)

# print("\n🔍 检索到的内容:")
# for i, doc in enumerate(result):
#     print(f"\n--- 结果 {i+1} ---")
#     print(doc.page_content)
# ======================================================