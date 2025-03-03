from langchain.chains import RetrievalQA
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_openai import AzureChatOpenAI


import os

from dotenv import load_dotenv
load_dotenv()

llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="trial1",
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="embed1",
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
)


review_template = """Your job is to use ESG (A sustainability report is a report published by companies on the environmental, social and governance (ESG) impacts of their activities)
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
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [esg_system_prompt, esg_human_prompt]

esg_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)


def query(query, year, allyears):
    if year not in allyears:
        return "No relevant documents found for year "+year+"."
    index_name: str = f"esg-demo-{year}"

    vector: AzureSearch = AzureSearch(
        azure_search_endpoint="https://esg-demo.search.windows.net",
        azure_search_key="m0NJknRuJEIMMLWeYheHYAUBafnvlIuap48eNQuHI2AzSeAQpZND",
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    retriever = vector.as_retriever()

    esg_vector_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )


    response = esg_vector_chain.invoke(query)
    return response
