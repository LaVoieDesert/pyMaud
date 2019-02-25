# -*- coding: utf-8 -*-
#!/usr/bin/env python

from maud_parser2 import maud_parser
from maud_parse_value import parse_single_maud_value_nokeyword, get_value


def maud_get_samples(data):
    samples = []
    for key in data.keys():
        if key.startswith("data_sample_"):
            samples.append(key)
    return samples


def maud_get_compo(data, sample_name):
    return data[sample_name]["#subordinateObject_layer1"]["_pd_phase_atom_%"]


def maud_get_cellparameters(data, sample_name):
    compo = maud_get_compo(data, sample_name)
    cell_parameters = []
    i = 0
    for key in data[sample_name]:
        if "_pd_phase_name" in data[sample_name][key]:
            pname = get_value(data[sample_name][key]["_pd_phase_name"])
            _compo = parse_single_maud_value_nokeyword(compo[i])
            cell_parameters.append(
                [
                    pname,
                    " " * (25 - len(pname)),
                    get_value(_compo) * 100,
                    get_value(data[sample_name][key]["_cell_length_a"]),
                    get_value(data[sample_name][key]["_cell_length_b"]),
                    get_value(data[sample_name][key]["_cell_length_c"]),
                ]
            )
            i += 1
    return cell_parameters


def maud_project_analysis(fichier, debug=False):
    data = maud_parser(fichier, debug)

    print("    --- Maud par file analysis ---")
    print(fichier)
    print("")

    data_global = data["data_global"]
    print(get_value(data_global["_publ_section_title"]))
    print(get_value(data_global["_audit_update_record"]))
    print("")

    print("Samples")
    samples = maud_get_samples(data)
    for sample in samples:
        print(
            " _ {}: {}".format(sample, get_value(data[sample]["_pd_spec_description"]))
        )
        cellparameters = maud_get_cellparameters(data, sample)
        for phase in cellparameters:
            print("      {:s}{}({:5.2f}%): {},{},{}".format(*phase))


if __name__ == "__main__":

    fichier = "data/A01_texture.par"
    maud_project_analysis(fichier)
