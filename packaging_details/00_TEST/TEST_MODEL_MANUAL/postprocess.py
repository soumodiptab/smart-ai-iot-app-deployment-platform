from tensorflow.keras.applications.resnet50 import decode_predictions

def postprocess(data):
    a=decode_predictions(data,top=3)[0]
    l=["rifle",'assault_rifle','bulletproof_vest','revolver','holster']
    x=0
    for i in a:
        if i[1] in l:
            x=1
    return x
