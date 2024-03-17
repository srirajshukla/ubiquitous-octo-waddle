import os

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores.azuresearch import AzureSearch

os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://openaimodelv3si.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "e248b8e8dbf94849ac6888971cacc9ae"
os.environ["AZURE_SEARCH_ENDPOINT"] = "https://esg-demo.search.windows.net"
os.environ["AZURE_SEARCH_KEY"] = "m0NJknRuJEIMMLWeYheHYAUBafnvlIuap48eNQuHI2AzSeAQpZND"

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="trial1",
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="embed1",
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
)

def gen_esg_vector(year):
    index_name: str = "esg-demo-all"
    vector_all: AzureSearch = AzureSearch(
        azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    index_name: str = "esg-demo-2021"
    vector_2021: AzureSearch = AzureSearch(
        azure_search_endpoint="https://esg-demo.search.windows.net",
        azure_search_key="m0NJknRuJEIMMLWeYheHYAUBafnvlIuap48eNQuHI2AzSeAQpZND",
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )
    index_name: str = "esg-demo-2022"
    vector_2022: AzureSearch = AzureSearch(
        azure_search_endpoint="https://esg-demo.search.windows.net",
        azure_search_key="m0NJknRuJEIMMLWeYheHYAUBafnvlIuap48eNQuHI2AzSeAQpZND",
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )
    index_name: str = "esg-demo-2023"
    vector_2023: AzureSearch = AzureSearch(
        azure_search_endpoint="https://esg-demo.search.windows.net",
        azure_search_key="m0NJknRuJEIMMLWeYheHYAUBafnvlIuap48eNQuHI2AzSeAQpZND",
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    if year == "2021":
        retriever = vector_2021.as_retriever()
    elif year == "2022":
        retriever = vector_2022.as_retriever()
    elif year == "2023":
        retriever = vector_2023.as_retriever()
    else:
        retriever = vector_all.as_retriever()
    
    review_template = """Your job is to use environmental, social and governance (ESG) 
    documents and annual reports to answer questions. Use
    the following context to answer questions. Be as detailed as possible, but
    don't make up any information that's not from the context. If you don't know
    an answer, say you don't know.
    {context}
    """

    esg_system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["context"], template=review_template)
    )

    esg_human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["question"], template="Answer the given question according to the response-option strictly and keep it concise if provided: {question}")
    )

    messages = [esg_system_prompt, esg_human_prompt]

    esg_prompt = ChatPromptTemplate(
        input_variables=["context", "question"], messages=messages
    )

    esg_vector_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    esg_vector_chain.combine_documents_chain.llm_chain.prompt = esg_prompt

    return esg_vector_chain
