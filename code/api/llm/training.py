from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
import os

from dotenv import load_dotenv
load_dotenv()


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
        azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
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
