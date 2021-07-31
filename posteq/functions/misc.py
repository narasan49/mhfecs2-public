import pickle, base64

"""
配列を pickle 化してモデルに保存できるようにする。
"""
def EncoArray(data):
    dump_data = pickle.dumps(data)
    b64_data = base64.b64encode(dump_data)
    return b64_data

"""
非　pickle　化
"""
def DecoArray(b64_data):
    pickle_data = base64.b64decode(b64_data.encode()[2:-1])
    res = pickle.loads(pickle_data)
    return res
