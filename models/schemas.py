from typing import List
from pydantic import BaseModel, Field


class CreditReport(BaseModel):
    """
    信贷风险评估报告的数据结构定义。
    用于规范大模型输出的报告格式。
    """
    
    # 风险等级：高、中、低
    risk_level: str = Field(
        ..., 
        description="风险等级，仅限 '高'、'中'、'低' 三个值之一"
    )
    
    risk_points:List[str]=Field(
        ...,
        description="风险点列表，例如：'逾期记录、不良信用记录'"
    )
    
    
    # 建议列表：针对风险点的处理建议
    suggestions: List[str] = Field(
        ..., 
        description="针对该用户的建议列表，例如：'建议降低授信额度'"
    )
    
    # 详细分析：LLM 的推理过程或详细理由
    analysis_details: str = Field(
        ..., 
        description="详细的分析过程或理由，解释为什么给出上述评级和建议"
    )
    
    
    # 可选：综合评分 (0-100)
    score: int = Field(
        default=0,
        description="综合信用评分，范围 0-100，分数越高信用越好"
    )