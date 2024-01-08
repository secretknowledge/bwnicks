import pickle


with open("cache.bin", "wb") as f:
    f.write(pickle.dumps(dict()))
