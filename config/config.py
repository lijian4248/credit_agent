# RAG 配置中心（企业级：所有参数都在这里）
RAG_CONFIG = {
    # 知识库路径
    "KB_DIR": "./data/knowledge",
    "DB_PATH": "./data/faiss_db",
    "RECORD_PATH": "./data/processed_files.json",

    # 文本分块配置
    "CHUNK_SIZE": 300,
    "CHUNK_OVERLAP": 50,
    "SEPARATORS": ["\n\n", "\n", " "],
    # 检索参数
    "RETRIEVE_K": 2,
    

    "MODEL_NAME": "BAAI/bge-small-zh-v1.5",
    "DEVICE": "cpu",
    "NORMALIZE_EMBEDDINGS": True,
    "CACHE_FOLDER": "./model",
    "HF_MIRROR": "https://hf-mirror.com",  # 镜像也进配置！
}


LLM_CONFIG = {
    # 通用 OpenAI 兼容格式
    # "API_KEY": "0977ac840a824e60be73cd40162f55ed.axmsebIlf8XWWYw7",
    "API_KEY": "9b630547-378d-4fd3-8542-ef4bb152d0f1",
    # "BASE_URL": "https://open.bigmodel.cn/api/paas/v4/",
    "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
    "MODEL_NAME": "doubao-seed-2-0-code-preview-260215",
    "TEMPERATURE": 0.1,
    "MAX_TOKENS": 2048
    
}