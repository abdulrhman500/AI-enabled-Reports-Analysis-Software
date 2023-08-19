import tensorflow as tf
import tensorflow_hub as hub
model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
def setup_USE():
    # Load the Universal Sentence Encoder model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    model = hub.load(module_url)
    # Encode a single sentence
    sentence = "This is an example sentence."
    sentence_embedding = model([sentence])

    # Encode a list of sentences
    sentences = ["I love machine learning.", "Natural language processing is fascinating."]
    sentences_embeddings = model(sentences)
    # Calculate similarity between sentences
    similarity_matrix = tf.matmul(sentences_embeddings, sentences_embeddings, transpose_b=True)
    print(similarity_matrix)

# Use the embeddings for downstream tasks like text classification, clustering, etc.



def clean (text):
    stop = set(stopwords.words('English'))
    text = text.lower()
    temp = ""
    for word in text :
        if word not in stop:
            temp += word 
    return temp
        
def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
    
if __name__ == "__main__":
    print("start")
    text = read_file("data.txt")
    print(text)
    print("end")
    print(clean(text))    