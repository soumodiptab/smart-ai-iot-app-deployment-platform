def postprocess(l):
    l=l[0]
    d = {0:'Drizzle', 1:'Fog', 2:'Rain', 3:'Snow', 4:'Sun'}
    return d[l]
