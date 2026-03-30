import os
import json


# 定义规则文件的路径
# 假设项目根目录是当前文件所在目录的上一级
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_RULES_DIR = os.path.join(BASE_DIR, "data", "knowledge")
CUSTOM_RULES_PATH = os.path.join(BASE_DIR, "data", "custom_rules.json")

def load_static_rules():
    """
    加载静态规则库文件。
    读取 data/knowledge 目录下的所有 markdown 和 txt 文件，并合并内容。
    """
    rules_text = ""
    
    if not os.path.exists(STATIC_RULES_DIR):
        print(f"警告：规则目录 {STATIC_RULES_DIR} 不存在。")
        return rules_text
    
     # 遍历目录下的文件
    for filename in os.listdir(STATIC_RULES_DIR):
        filepath = os.path.join(STATIC_RULES_DIR, filename)
        # 只处理 .md 和 .txt 文件
        if filename.endswith(".md") or filename.endswith(".txt"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    rules_text += f"### {filename} ###\n{content}\n\n"
            except Exception as e:
                print(f"读取规则文件 {filename} 失败: {e}")
    
    return rules_text

def load_custom_rules():
    """
    加载自定义规则。
    从 data/custom_rules.json 读取规则列表，并格式化为文本。
    如果文件不存在或为空，返回空字符串。
    """
    if not os.path.exists(CUSTOM_RULES_PATH):
        return ""
    
    try:
        with open(CUSTOM_RULES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if not data:
                return ""
                
            # 假设 JSON 结构是一个列表: [{"id": "...", "content": "..."}]
            # 我们将其格式化为 "ID: 内容" 的文本列表
            rules_list = [f"{rule.get('id', 'Unknown')}: {rule.get('content', '')}" for rule in data]
            return "\n".join(rules_list)
            
    except Exception as e:
        print(f"读取自定义规则失败: {e}")
        return ""
    
def get_all_rules():
    """
    获取所有规则的组合文本。
    返回: (static_rules_text, custom_rules_text)
    """
    static_rules = load_static_rules()
    custom_rules = load_custom_rules()
    
    return static_rules, custom_rules