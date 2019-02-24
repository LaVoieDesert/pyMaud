import pyparsing as pp

value = pp.Word(pp.nums+'.'+'E'+'-').setResultsName('value')

v_name = pp.Group(pp.Combine("_" + pp.Word(pp.alphanums+"_/")).setResultsName('value')).setResultsName('v_name')

v_value = pp.Group(value).setResultsName('v_value') + pp.Optional(pp.Group("("+value+")").setResultsName('v_error'))

v_min = pp.Group(pp.Keyword("#min") + value).setResultsName('v_min')
v_max = pp.Group(pp.Keyword("#max") + value).setResultsName('v_max')
v_positive = pp.Group(pp.Keyword("#positive").setResultsName('value')).setResultsName('v_positive')
v_autotrace = pp.Group(pp.Keyword("#autotrace").setResultsName('value')).setResultsName('v_autotrace')
v_options = pp.ZeroOrMore(v_autotrace | v_positive | v_min | v_max)

v_words = pp.Group("'" + pp.Combine(pp.OneOrMore(pp.Word(pp.alphanums+" :.,_+-/\()?!@"))).setResultsName('value') + "'").setResultsName('v_words')

v_word = pp.Group(pp.Word(pp.alphanums+"?").setResultsName('value')).setResultsName('v_word')

v_all = v_name + ((v_value + v_options) | v_words | v_word)

def parse_single_maud_value(ligne):
    return v_all.parseString(ligne)

def parse_single_maud_value_nokeyword(ligne):
    v_all_nokeyword = ((v_value + v_options) | v_words | v_word)
    return v_all_nokeyword.parseString(ligne)


if __name__ == "__main__":

    print(v_name.parseString("_pd_proc_intensity_incident")['v_name'])

    print(v_value.parseString("134.80128(0.27891675)"))

    print(v_min.parseString("#min 0.0"))
    print(v_min.parseString("#min 0.0")['v_min']['value'])

    print(v_max.parseString("#max 2.1"))
    print(v_max.parseString("#max 2.1")['v_max']['value'])

    print(v_positive.parseString("#positive"))
    print(v_positive.parseString("#positive")['v_positive']['value'])

    print(v_autotrace.parseString("#autotrace"))
    print(v_autotrace.parseString("#autotrace")['v_autotrace']['value'])

    print(v_options.parseString("#min 0.0 #max 10000.0"))

    print(v_words.parseString("'Luca Lutterotti'"))
    print(v_words.parseString("\'test 1\'"))

    print(v_word.parseString("Luca Lutterotti"))
    print(v_word.parseString("test"))


    print("\n\n\n")



    ex = ["_riet_par_spec_layer_thickness 6500000.0(1.0) #autotrace #positive #min 0.1 #max 1.0E8",
        "_publ_contact_author_name 'Luca Lutterotti'",
        "_maud_store_spectra_with_analysis true",
        "_cell_length_a 10.6033125(1.3484144E-5) #min 0.1",
        "_atom_site_B_iso_or_equiv 0.2942433(0.006691931) #min -1.0 #max 10.0 #ref0",
        "_atom_site_B_iso_or_equiv 0.2942433 #min -1.0 #max 10.0 #equalTo 0 + 1 * #ref0"]
    for e in ex:

        res = v_all.parseString(e)

        print(e)
        print(res)
        print(list(res.keys()))
        for k in res.keys():
            print("  {}: {}".format(k, res[k]['value']))
        print("\n")

