from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
import os
os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openaimodelv3si.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "e248b8e8dbf94849ac6888971cacc9ae"

def pdf_loader(filenames):
    print("starting pdf loader")
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="embed1",
        openai_api_version="2024-02-15-preview",
    )
    print("loaded embeddings")

    index_name: str = "esg-survey"
    vector: AzureSearch = AzureSearch(
        azure_search_endpoint="https://esg-survey.search.windows.net",
        azure_search_key="G3KuN7j6O10Tn2AOgJXlgEhDgKqStP9iZQdLor9ajaAzSeBVCNBy",
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )
    print("loaded vector")
    outs = []
    for filename in filenames:
        loader = PyPDFLoader(filename)
        pages = loader.load_and_split()
        print(f"{filename} has {len(pages)} pages")
        out = vector.add_documents(documents=pages)
        outs.append(out)

    return outs
