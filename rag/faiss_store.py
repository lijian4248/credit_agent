from langchain_community.vectorstores import faiss
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.config import RAG_CONFIG
import os,json,glob



# 配置路径
KB_DIR = RAG_CONFIG["KB_DIR"]
DB_PATH = RAG_CONFIG["DB_PATH"]
RECORD_PATH = RAG_CONFIG["RECORD_PATH"]

CHUNK_SIZE = RAG_CONFIG["CHUNK_SIZE"]
CHUNK_OVERLAP = RAG_CONFIG["CHUNK_OVERLAP"]
SEPARATORS = RAG_CONFIG["SEPARATORS"]


def get_text_splitter():
    """全局唯一的文本切分器（消除重复代码）"""
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS
    )


def load_processed_files():
    if os.path.exists(RECORD_PATH):
        with open(RECORD_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_processed_files(processed_files):
    with open(RECORD_PATH, "w", encoding="utf-8") as f:
        json.dump(processed_files, f, ensure_ascii=False, indent=2)


def load_new_documents():
    processed = load_processed_files()
    files = glob.glob(f"{KB_DIR}/*.md") + glob.glob(f"{KB_DIR}/*.txt")

    new_files = [f for f in files if f not in processed]
    if not new_files:
        return [], []

    all_docs = []
    for file in new_files:
        try:
            loader = TextLoader(file, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"跳过 {file}: {e}")

        splitter = get_text_splitter()
        return splitter.split_documents(all_docs), new_files

# 加载【所有】文档（全量重建用）


def load_all_documents():
    files = glob.glob(f"{KB_DIR}/*.md") + glob.glob(f"{KB_DIR}/*.txt")
    all_docs = []
    for file in files:
        try:
            loader = TextLoader(file, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"跳过 {file}：{e}")

    splitter = get_text_splitter()
    return splitter.split_documents(all_docs), files


def build_faiss_vector_db(embeddings, force_rebuild: bool = False):
    if force_rebuild and os.path.exists(DB_PATH):
        import shutil
        shutil.rmtree(DB_PATH)
        if os.path.exists(RECORD_PATH):
            os.remove(RECORD_PATH)
        print("🗑️ 全量重建模式：已清空旧向量库")

    if os.path.exists(DB_PATH):
        db = faiss.FAISS.load_local(DB_PATH, embeddings,allow_dangerous_deserialization=True)
    else:
        db = None

    if force_rebuild or db is None:
        docs, all_files = load_all_documents()
        db = faiss.FAISS.from_documents(docs, embeddings)
        db.save_local(DB_PATH)
        save_processed_files(all_files)
        print("✅ 全量重建完成！")
    else:
        docs, new_files = load_new_documents()
        if docs:
            print(f"📝 新增 {len(docs)} 篇文档，正在加入向量库")
            if db is None:
                db = faiss.FAISS.from_documents(docs, embeddings)
            else:
                db.add_documents(docs)
            db.save_local(DB_PATH)

            processed = load_processed_files()
            processed.extend(new_files)
            save_processed_files(processed)
            print("✅ 更新完成！")

        else:
            print("✅ 暂无新文件，向量库已是最新！")
    return db
