import jsonpickle
import os

def writer(data) -> None:
    temp = []
    tempStr = []
    fname = './data.json'
    if not os.path.isfile(fname):
        with open(fname, 'a') as f:
            f.write(jsonpickle.encode(data))
    
    else:
        with open(fname, 'r') as f:
            temp.append(jsonpickle.decode(f.read(-1)))
        
        temp.append(data)

        for t in temp:
            tempStr.append(jsonpickle.encode(t))

        print(type(tempStr[0]))

        with open(fname, 'a') as f:
            f.writelines(tempStr)

