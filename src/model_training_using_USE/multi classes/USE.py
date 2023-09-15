import tensorflow as tf
import tensorflow_hub as hub
embed = None
def set_up():
    global embed
    embed = hub.load("F:\\universal-sentence-encoder-large_5")
    return embed
def apply_USE(text):
    # print("Applying USE")   
    # print([text])
    return embed([text])[0]
set_up()
# print(apply_USE(["the quick brown fox jumps over the lazy dog","I am a sentence for which I would like to get its embedding"]))