from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains import RetrievalQA

embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

from groq import Groq
from langchain_groq import ChatGroq

llm = ChatGroq(temperature=0,
                      model_name="Llama3-8b-8192",
                      api_key="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",)

loader = JSONLoader(
    file_path='Taxonomy-Fashion.json',
    jq_schema='.',
    text_content=False)

data = loader.load()

docs_list = [item for sublist in data for item in sublist]
print(f"len of documents :{len(docs_list)}")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=512, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)
print(f"length of document chunks generated :{len(doc_splits)}")

vectorstore = Chroma.from_documents(documents=doc_splits,
                                    embedding=embed_model,
                                    collection_name="local-rag")

grok_agent = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever = vectorstore.as_retriever(search_kwargs={"k":2}))

answer = grok_agent.invoke(
    "identify if denim shirt can be categorized into the sub-category for example sneakers can be categorized into shoes,then get all the fields that has the value M ",handle_parsing_errors=True
)

print(answer["output"])