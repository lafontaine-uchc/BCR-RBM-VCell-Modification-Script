from xml.dom import minidom


def list_reactions(xmldoc):
    itemlist = xmldoc.getElementsByTagName('Kinetics')
    for i in itemlist:
        rxn_name=i.parentNode._attrsNS.get((None, 'Name')).firstChild._data
        print(rxn_name)
        for j in i.childNodes:
            if j._attrsNS.get((None, 'Name')).firstChild._data=='J':
                reaction=j.firstChild._data
                print(reaction)


def get_species(xmldoc):
    # from xml.dom import minidom
    # xmldoc = minidom.parse(filename)
    namelist = {}
    for x in xmldoc.childNodes[1].childNodes[0].childNodes[0].childNodes:
        if x.nodeName == "Compound":
            print(x.attributes['Name'].value)
            species = x.attributes['Name'].value
            print("space")
            try:
                print(x.firstChild.firstChild._data)
                bngl_name = x.firstChild.firstChild._data
                namelist[species] = bngl_name
            except:
                print("not bngl generated")


def get_obs_list(rbmxmldoc):
    olist=[]
    itemlist = rbmxmldoc.getElementsByTagName('Observable')
    for i in itemlist:
        name=i._attrsNS.get((None, 'Name')).firstChild._data
        olist.append(name)
    return(olist)


def get_observables(xmldoc, obs_list):
    observables={}
    itemlist = xmldoc.getElementsByTagName('Function')
    for i in itemlist:
        name=i._attrsNS.get((None, 'Name')).firstChild._data
        if name  in obs_list:
            observables[name] = i.firstChild.data
    return(observables)


def add_output_function_to_simulation(function_name, function_content, vcml_doc):
    # new_element = vcml_doc.createElement('AnnotatedFunction')
    # new_text = vcml_doc.createTextNode("(s11 + s30)")
    # new_element.appendChild(new_text)
    #
    # new_element.setAttribute("ErrorString", "")
    # new_element.setAttribute("FunctionType", "Nonspatial")
    # new_element.setAttribute("name", "new_element_name")
    # OutputFunctions = vcml_doc.getElementsByTagName('OutputFunctions')
    # OutputFunctions[0].appendChild(new_element)

    new_element = vcml_doc.createElement('AnnotatedFunction')
    new_text = vcml_doc.createTextNode(function_content)
    new_element.appendChild(new_text)

    new_element.setAttribute("ErrorString", "")
    new_element.setAttribute("FunctionType", "Nonspatial")
    new_element.setAttribute("Name", function_name + "1")
    OutputFunctions = vcml_doc.getElementsByTagName('OutputFunctions')
    OutputFunctions[0].appendChild(new_element)

    return(vcml_doc)


# flattened_doc= minidom.parse('vcml_for_testing_bng_names.vcml')
# original_doc = minidom.parse('dbcl_rbm_blnk_rbm_simplified-5-17-18.vcml')
flattened_doc = minidom.parse('small_model_5-30-18_flattned.vcml')
original_doc = minidom.parse('small_model_5-30-18_rbm.vcml')
with open("test_output_nochange.vcml", "w") as xml_file:
    flattened_doc.writexml(xml_file)
list_reactions(flattened_doc)
get_species(flattened_doc)

#ob=get_observables(original_doc, ["O0_BTK_tot"])
ob = get_observables(original_doc, get_obs_list(original_doc))

flattened_doc=add_output_function_to_simulation("new_element_name", "(s11 + s30)",flattened_doc)
#flattened_doc=add_output_function_to_simulation("new_element_name", "(s11 + s30)",flattened_doc)

for key, value in ob.items():
    print (key, value)
    flattened_doc = add_output_function_to_simulation(key, value, flattened_doc)

with open("test_output_flatadsaf.vcml", "w") as xml_file:
    flattened_doc.writexml(xml_file)

    # kinetics=i.parentNode
    # print(i.childNodes)