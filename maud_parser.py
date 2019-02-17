
from maud_parse_value import parse_single_maud_value

def parse_datablock(texte):
    block_key = texte[0]
    texte = texte[1:]
    data = {}
    
    parser = True
    
    while len(texte) and parser not in [parse_datablock, None]:
        while len(texte) and not len(texte[0]): texte = texte[1:]
        if len(texte):
            parser = get_parser(texte[0])
            if parser not in [parse_datablock, None]:
                key, value, texte = parser(texte)
                data[key] = value

    while len(texte) and not len(texte[0]): texte = texte[1:]
        
    return block_key, data, texte

def parse_cifloop(texte):
    ligne = texte[0]
    key = texte[1]
    value = []
    i = 2
    while len(texte[i]):
        value.append(texte[i])
        i += 1
    
    texte = texte[i:]
    while len(texte) and not len(texte[0]): texte = texte[1:]
        
    return key, value, texte

def parse_custom_object(texte):
    ligne0 = texte[0]
    _key = ligne0[15:]
    _end_key = "#end_custom_object_{}".format(_key)
    
    data = {}
    texte = texte[1:]
    
    parser = None
    
    while len(texte) and not (texte[0] == _end_key):
        while len(texte) and not len(texte[0]):
            texte = texte[1:]
        if len(texte):
            print(_end_key)
            parser = get_parser(texte[0])
            if parser is not None:
                key, value, texte = parser(texte)
                data[key] = value

    print(_end_key)

    texte = texte[1:]
    while len(texte) and not len(texte[0]): texte = texte[1:]
        
    return _key, data, texte

def parse_subordinateobject(texte):
    ligne0 = texte[0]
    _key = ligne0[19:]
    _end_key = "#end_subordinateObject_{}".format(_key)
    
    ligne2 = texte[2]
    key = ligne2.split(" ")[0]
    
    data = {}
    data[key] = " ".join(ligne2.split(" ")[1:])
    
    texte = texte[2:]
    
    parser = None
    
    while len(texte) and not (texte[0] == _end_key):
        while len(texte) and not len(texte[0]):
            texte = texte[1:]
        if len(texte):
            parser = get_parser(texte[0])
            if parser is not None:
                key, value, texte = parser(texte)
                data[key] = value
   
    texte = texte[1:]
    while len(texte) and not len(texte[0]): texte = texte[1:]

    return key, data, texte


def parse_value(texte):
    ligne = texte[0]
    key = ligne.split(" ")[0]
    value = " ".join(ligne.split(" ")[1:])
    
    parsed_value = parse_single_maud_value(ligne)

    texte = texte[1:]
    while len(texte) and not len(texte[0]): texte = texte[1:]
    
    return parsed_value['v_name']['value'], value, texte



def get_parser(ligne):
    if ligne.startswith("data_"):
        print("parsed data_: {}".format(ligne))
        return parse_datablock
    elif ligne.startswith("loop_"):
        print("parsed loop_: {}".format(ligne))
        return parse_cifloop
    elif ligne.startswith("#subordinateObject_"):
        print("parsed subordinateObject_: {}".format(ligne))
        return parse_subordinateobject
    elif ligne.startswith("#custom_object_"):
        print("parsed custom_object_: {}".format(ligne))
        return parse_custom_object
    elif ligne.startswith("_"):
        print("parsed value_: {}".format(ligne))
        return parse_value
    else:
        print("not parsed: {}".format(ligne))
        return None
    


def parse_maud(texte):
    data = {}
    while len(texte):
        while len(texte) and not len(texte[0]):
            #print("ligne vide : {}".format(texte[0]))
            texte = texte[1:]
        if len(texte):
            parser = get_parser(texte[0])
            if parser is not None:
                key, value, texte = parser(texte)
                data[key] = value
            else:
                print("error with line:\n  {}".format(texte[0]))
                texte = []
    return data

def maud_parser(fichier):
    f = open(fichier)
    raw_data = f.read()
    raw_data = raw_data.split('\n')
    data = parse_maud(raw_data)
    return data






if __name__ == "__main__":
    import pprint
    fichier = "data/A01_texture.par"
    data = maud_parser(fichier)
    print("\n")
    #pprint.pprint(data)
    print("\n")
    
    fichier = "data/y2o3.par"
    data = maud_parser(fichier)
    print("\n")
    pprint.pprint(data)
    print("\n")
    
    fichier = "data/cif_loop.par"
    data = maud_parser(fichier)
    print("\n")
    pprint.pprint(data)
    print("\n")
    
    
    fichier = "data/cif_data.par"
    data = maud_parser(fichier)
    print("\n")
    pprint.pprint(data)
    print("\n")
    
    
    fichier = "data/cif_subordinateObject.par"
    data = maud_parser(fichier)
    print("\n")
    pprint.pprint(data)
    print("\n")