 # -*- coding: utf-8 -*-
#!/usr/bin/env python

from maud_parser2 import maud_parser
from maud_parse_value import parse_single_maud_value_nokeyword


fichier = "data/A01_texture.par"
data = maud_parser(fichier, debug=False)
compo = data['data_sample_Sample_x']['#subordinateObject_layer1']['_pd_phase_atom_%']
    
print(fichier)
i = 0
for key in data['data_sample_Sample_x']:
    if "_pd_phase_name" in data['data_sample_Sample_x'][key]:
        pname = data['data_sample_Sample_x'][key]["_pd_phase_name"]['v_words']['value']
        _compo = parse_single_maud_value_nokeyword(compo[i])
        print("   {:s}{}({:5.2f}%): {},{},{}".format(
            pname,
            ' '*(25-len(pname)),
            float(_compo['v_value']['value'])*100,
            data['data_sample_Sample_x'][key]["_cell_length_a"]['v_value']['value'],
            data['data_sample_Sample_x'][key]["_cell_length_b"]['v_value']['value'],
            data['data_sample_Sample_x'][key]["_cell_length_c"]['v_value']['value'],
            ))
        i += 1
                