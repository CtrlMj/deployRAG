from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.document_loaders import PyPDFLoader


def index_documents_to_elasticsearch(pdf_path="../random machine learing pdf.pd", es_url="http://localhost:9200", index_name="pdf-index"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    ElasticsearchStore.from_documents(
        documents,
        embedding=None,
        es_url=es_url,
        index_name=index_name
    )
