# pyMaud
scripts to parse and manipulate MAUD project.par files.

MAUD is an amazing tool to analyse diffraction data (and more), checkout here 

 * http://www.ccp14.ac.uk/ccp/web-mirrors/lutterotti/~luttero/maud/Installers/maudInstallers.html
 * https://github.com/luttero/Maud
 
but the manipulation off many files simultaneously is quite difficulte. I have seen many different solution from different people. I propose my scripts, under development, to help, as I have not found what I search around.

## Example 01

extract the cell parameters of the different phases

    #coding: utf-8
    #!/usr/bin/env python

    from maud_parser2 import maud_parser
    from maud_parse_value import parse_single_maud_value_nokeyword, get_value


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
                get_value(_compo)*100,
                get_value(data['data_sample_Sample_x'][key]["_cell_length_a"]),
                get_value(data['data_sample_Sample_x'][key]["_cell_length_b"]),
                get_value(data['data_sample_Sample_x'][key]["_cell_length_c"]),
                ))
            i += 1

will give as result

    data/A01_texture.par
        cementite                ( 3.36%): 4.511985,5.065079,6.7294774
        gamma-Fe                 ( 9.03%): 3.5815272,3.5815272,3.5815272
        martensite               (87.61%): 2.8529925,2.8529925,2.9219563

## Example 02

quick overview of the project by analysing the 'par' file

    #coding: utf-8
    #!/usr/bin/env python

    from maud_analyse_project import maud_project_analysis


    fichier = "data/A01_texture.par"
    maud_project_analysis(fichier) 

will give as result

        --- Maud par file analysis ---
    data/A01_texture.par

    Put a title here
    Last update Thu Feb 23 17:51:40 CET 2017

    Samples
    _ data_sample_Sample_x: Sample description
        cementite                ( 3.36%): 4.511985,5.065079,6.7294774
        gamma-Fe                 ( 9.03%): 3.5815272,3.5815272,3.5815272
        martensite               (87.61%): 2.8529925,2.8529925,2.9219563