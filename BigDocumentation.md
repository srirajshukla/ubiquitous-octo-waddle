# ESG Hackthon

## Challenges faced

### PDF Parsing

- Parsing Unstructured data like Table, where column values are referenced in the subsequent pages making it difficult to understand the contextual meaning.
- Differentiating Table Headers and data rows, and line breaks often mistaken as the next row in the parser.
- Tables are broken manually and referenced at later part of the page due to space constraint, making it difficult for the parser to correlate the context.
- Couldn’t use Python libraries to extract the tables as they aren’t able to distinguish between table response format and table headers.
- Azure Document Intelligence has two different APIs for paragraph and table extraction. We had to come up with a solution that could return both.

### Questions Extraction

- Extracting questions from the survey PDFs was a major challenge with the assumption that there is no particular format for the questions.
- We tried different approaches like extracting questions with the help of LLM models and techniques like OCR (Optical Character Recognition)
- A major problem in extraction via the LLM approach was the inconsistency in question formatting which led to inaccurate responses by the model (It was not able to identify all the existing questions in PDFs accurately)
- We also finetuned this process by splitting the file data into small chunks for better results by the model. The results improved greatly but still the response were inconsistent and inaccurate to some extent.
- The major problem with this approach was parsing data like Tables and other formatted data which led us to jump on to another approach using OCR

### PDF generation

- Due to the unpredictability of LLM results and the table format returned, it was almost impossible to create a table from the response.
- Sometimes LLMs weren’t able to answer the questions resulting in empty tables.
- Formatting the table to accommodate the pages without overflow.

### Application Deployment
- We were using docker-compose to create and orchestrate our deployments. We couldn't use Azure Web Apps and Azure App Instances to deploy our apps.
- We had to deploy an Azure Virtual Machine and setup docker environment there for deployments.
- Since we were using docker compose files, after setting up the environment however, our deployment process was quite simple.
- We just run docker comopse up and our application was up and running.


## Approaches (the roads ~~not taken~~ tried and tested)

### Retrievers

- Local retrievers (FAISS and Chroma)
- Azure Search : Azure Search: [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/) (formerly known as "Azure Cognitive Search") is an AI-powered information retrieval platform that helps developers build rich search experiences and generative AI apps that combine large language models with enterprise data.

### Vector stores

- FAISS : Facebook AI Similarity Search (Faiss) is **a library for efficient similarity search and clustering of dense vectors**. It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM.
- Chroma : **[Chroma DB](https://docs.trychroma.com/)** is an open-source vector store used for storing and retrieving vector embeddings. Its main use is to save embeddings along with metadata, can also be used for semantic search engines over text data.
- Azure Search indexes

Challenges 
- adding documents dynamically to vectorstore: azure solved problem
- saving vector store locally and loading(solved with FAISS), instead of creating new vector space each time when local application is run

### Choice of LLM

- Llama2 : Llama 2 is Meta's open source large language model ([LLM](https://zapier.com/blog/best-llm)). Tried with Llama2 running locally (using Ollama), but 7b parameter version did not provide good results and more powerful models (13B, 70B) needed lot more computational resources.
    
- gpt3.5-turbo vs gpt3.5-turbo-instruct: The instruct model is much more terse and concise, it just does what it is instructed to do.
    
    `gpt-3.5-turbo` is chatty, it will talk to you beyond what is asked.
    
    So, if you want a model to *do* something the instruct model will typically work better and use fewer tokens doing so.
    
    If you want a model to *interact* with users in a natural, conversational manner the chat model will be much better.

### Choice of embedding:

- Llama2 uses Ollama embeddings, GPT models use ***Azure*** OpenAI ***embeddings.***

- Used  ***Azure*** OpenAI ***embeddings*** API wrapper provided by langchain to embed our documents and store them to Azure Search Indices.

### Finetuning the Model
- For even better performance, we tried fine-tuning our models as well.
- We took data from the training materials and transformed them into a JSON of question-answer pairs. It was in a format where it could be used to train the models. However, we felt this was not the best data we could get from these pdf files.
- The Azure subscription didn't have options for us to try finetuning the models. So, in the interest of time, we decided this was an excellent thing to try later on, and moved on to building other features.
