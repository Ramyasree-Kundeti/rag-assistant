from langchain_huggingface import HuggingFaceEmbeddings

#MODEL_NAME = "intfloat/multilingual-e5-small"
MODEL_NAME = "intfloat/multilingual-e5-base"

def get_embeddings():

    #E5 models expects "passage: " before documents and "query: " before questions
    return HuggingFaceEmbeddings(
        model_name = MODEL_NAME,
        encode_kwargs = {"normalize_embeddings":True,"prompt":"passage: "},
        query_encode_kwargs={"normalize_embeddings":True,"prompt":"query: "},
    )
