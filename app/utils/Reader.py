import jsonpickle

def reader() -> None:
    with open('./data.json', 'r') as f:
        plainObj = f.read(-1)

    # obj = jsonpickle.decode(plainObj)
    print(jsonpickle.decode(str(plainObj))) 
