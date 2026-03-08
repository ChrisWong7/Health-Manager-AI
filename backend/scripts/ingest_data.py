from app.core.vector_store import vector_store
import uuid

def ingest_knowledge_base():
    """
    Ingest initial medical knowledge into Vector DB.
    In a real app, this would read from PDF/Markdown files.
    """
    
    knowledge_data = [
        {
            "text": "高血压（Hypertension）是一种以体循环动脉血压增高为主要特征的临床综合征。根据《中国高血压防治指南》，在未使用降压药物的情况下，诊室收缩压≥140mmHg和/或舒张压≥90mmHg即为高血压。高血压是中风、心脏病、血管疾病和肾脏病的主要危险因素。",
            "metadata": {"title": "中国高血压防治指南(2023年修订版)", "type": "guideline"}
        },
        {
            "text": "高血压患者应坚持长期治疗。生活方式干预是基础，包括：减少钠盐摄入（每人每日食盐摄入量不超过5克），减轻体重，规律运动（每周至少150分钟中等强度运动），戒烟限酒，保持心理平衡。",
            "metadata": {"title": "中国高血压防治指南(2023年修订版)", "type": "guideline"}
        },
        {
            "text": "持续性头痛可能由多种原因引起，常见原因包括紧张性头痛（双侧压迫感或紧箍感）、偏头痛（单侧搏动性疼痛，常伴恶心）、颈椎病（伴颈部僵硬）或高血压（晨起头痛）。若头痛剧烈且突发（雷击样），或伴有发热、神志不清、视力障碍，应立即就医排除脑出血或脑膜炎。",
            "metadata": {"title": "头痛分类与诊断流程", "type": "medical_manual"}
        },
        {
            "text": "糖尿病典型症状为'三多一少'：多尿、多饮、多食和体重下降。空腹血糖≥7.0mmol/L或餐后2小时血糖≥11.1mmol/L可诊断。长期高血糖可导致视网膜病变、肾病和神经病变。",
            "metadata": {"title": "中国2型糖尿病防治指南", "type": "guideline"}
        }
    ]

    documents = [item["text"] for item in knowledge_data]
    metadatas = [item["metadata"] for item in knowledge_data]
    ids = [str(uuid.uuid4()) for _ in knowledge_data]

    print(f"Ingesting {len(documents)} documents into Vector Store...")
    vector_store.add_documents(documents, metadatas, ids)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_knowledge_base()
