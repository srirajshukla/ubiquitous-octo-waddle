# ESG SURVEY AUTOMATION - Team Orange
#### Leveraging LLM for gogoolX productivity

### Start app
The instructions to start the app are in [Cookbook.md](Cookbook.md). The application uses docker to build and run a reproducable version of the application. 

### Visit the APP at -
- UI: http://57.151.96.201:8501/
- API: http://57.151.96.201:8000/docs/

Use credentials
```
username: stanleyjobson
password: swordfish
```
when prompted

### Video Link
https://team50filestorage.blob.core.windows.net/demo/hack_demo_uncut.mov

### Assumptions
- Training data documents provided to us, are uploaded via the API **/esgreports/upload**
- This data is listed when calling the API **/esgreports/retrieve**
- **Survey Format**: We assume all surveys (used for testing) have similar format (where question start with **C notation**)
- For API **/questionnaire/generatefirstdraft/generateAnswer**:
    - If a year is provided for which we don’t not have context (eg. 2014) for the model, it will say “No relevant documents found for the year 2014.”
    - If you now upload new documents of year 2014 and then ask again, it will now generate answer based on the newly added context.


### Solution

**LLMs** can be effectively utilized to generate answers for **ESG (Environmental, Social, and Governance) surveys** by utilizing **RAG (Retrieval Augmented Generation)** , thus streamlining the automation process of filling out these survey forms:

**Here’s how it works**:
- **RAG**: LLMs, such as **GPT-4**, **Llama2** combine pre-trained language capabilities with retrieval mechanisms.
- **Retrieval**: The LLM retrieves relevant context from authoritative knowledge bases (external sources).
- **Generation**: Using the retrieved context, the LLM generates contextually accurate and insightful answers.
- **Specificity and Transparency**: LLMs provide answers tailored to the data provided, reducing vagueness and inaccuracies. We can see proper citations (with page numbers) for the answers our LLM generates.

**Components we used for RAG**:
- **Azure OpenAI Chat**: We were provided with access to **GPT-35-Turbo** and it's variants, we found it to be performing better than Llama2 model. We used Azure's **Chat Completion API** wrapped with **Langchain**.
- **Azure OpenAI Embeddings**: We used **text-davinci** model to embed our documents and user queries.
- **Azure FileStorage**: We use File Storage by Azure to store our knowledge base (embeddings of our uploaded documents).
- **Azure SearchAI**: Used to retrieve relevant documents by performing a similarity search on our Stored documents to the Query passed.
- **Azure Blog Storage**: We store **Survey questionnares** and our **Generated Drafts**, as well as our training data on Blog Storage.

**Novelty Factors**:
- Since it was a major challenge to parse questions from **Tables** in our questionnares, we found CDP's URL where it displays a specific question. It was way easier to web-scrape and parse questions to generate answers.
- Docker: docker compose?
- Postgres

### Generating Survey Drafts
The first step to filling out the survey is to extract questions from it.

**Parsing, OCR, Web Scraping**:
-  **Azure Document Intelligence API** serves as a powerful tool for processing documents.Its primary functions include **parsing** and extracting relevant information from various document formats.
- **Optical Character Recognition (OCR)**: This technology allows the API to recognize characters within scanned images or handwritten text.
- **Parsing**: When a document (such as an ESG survey form) is submitted, the API dissects its structure. If the question contains only strings (not tables), we can directly invoke the LLM.
- **Table Extraction**: If it identifies tables within the document, we webscrape the specific table from the internet, as it was a major challenge parsing tables through NLP.
    - URL <https://guidance.cdp.net/en/guidance?cid=C4.2b&ctype=ExternalRef&gettags=0&idtype=RecordExternalRef&incchild=0%C2%B5site%3D0&otype=Guidance&page=1> 
    
    

**Workflow for ESG Survey Form Filling**:
- Once the document is parsed and tables are extracted, the system compiles a **list of questions** from the survey.
- Each question is paired with a specified **response format** (e.g., short answer, numerical value, or paragraph).
- These question-response pairs are then sent to our  **RAG**.
- LLM processes each question, understands the context from documents of that **particular year**, and generates appropriate answers.
- Finally, the answers are formatted and assembled into a resulting **PDF document**.

### Core Python Library
**LangChain** is an open-source framework designed to simplify the creation of applications using large language models (LLMs). It provides a standard interface for chains, numerous integrations with other tools, and end-to-end chains for common applications. 

Langchain modules used:
- **AzureChatOpenAI** and **AzureOpenAIEmbeddings** from langchain_openai 
    - Used to invoke LLMs
- **AzureSearch** from langchain_community.vectorstores.azuresearch
    - To retrieve relevant embeddings based on query
- **PyPDFLoader** from langchain_community.document_loaders
    - Gives us metadata including page number for citations.
- **RetrievalQA** from langchain.chains
    - Used to query LLM with RAG
- **Prompts** from langchain.prompts
    - Prompt templates including System Prompt, User Prompt
 


Application Screenshots for Reference:

![Screen1](https://github.com/Hackathon2024-March/orange/assets/65178804/33115602-5028-4f10-85e5-08089edc5a1e)

![Screen2](https://github.com/Hackathon2024-March/orange/assets/65178804/e25a8099-2b6a-4d89-a51e-89b04b67e7ed)

![Screen3](https://github.com/Hackathon2024-March/orange/assets/65178804/cd883516-acdc-404d-96bd-c2faf7c095de)

![Screen4](https://github.com/Hackathon2024-March/orange/assets/65178804/c5e34558-a7d1-42f1-ada6-aa30666839dd)


#### Other documentation is in BigDocumentation.md (please read thanks)
