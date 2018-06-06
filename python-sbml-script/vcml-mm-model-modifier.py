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
        if name in obs_list:
            observables[name] = i.firstChild.data
    return(observables)


def get_node_by_attribute(parent_node,att_name,att_value):
    for x in parent_node.childNodes:
        if x.attributes.getNamedItem(att_name).firstChild.data == att_value:
            return x


def add_output_function_to_simulation(function_name, function_content, vcml_doc):

    new_element = vcml_doc.createElement('AnnotatedFunction')
    new_text = vcml_doc.createTextNode(function_content)
    new_element.appendChild(new_text)
    new_element.setAttribute("ErrorString", "")
    new_element.setAttribute("FunctionType", "Nonspatial")
    new_element.setAttribute("Name", function_name + "1")
    OutputFunctions = vcml_doc.getElementsByTagName('OutputFunctions')
    OutputFunctions[0].appendChild(new_element)
    return(vcml_doc)
def convert_mass_action_to_michaelis_menten(simple_reaction_node):

    print(simple_reaction_node.attributes.getNamedItem("Name").firstChild.data)
    kinetics = simple_reaction_node.getElementsByTagName("Kinetics")[0]
    A = get_node_by_attribute(kinetics, "Role", "reaction rate")
    Ks = get_node_by_attribute(kinetics, 'Role', 'forward rate constant')
    k, K = Ks.childNodes[0].data.replace("(", "").replace(")", "").split(" + ")
    print(A.firstChild.data)
    rxn = A.firstChild.data
    reactants = simple_reaction_node.getElementsByTagName('Reactant')
    reactant_names = []
    for reactant in reactants:
        print(reactant.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
        reactant_names.append(reactant.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)

    products = simple_reaction_node.getElementsByTagName('Product')
    product_names = []
    for product in products:
        print(product.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
        product_names.append(product.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
    catalyst = list(set(reactant_names) & set(product_names))[0]
    print(reactant_names)
    reactant_names.remove(catalyst)
    print(reactant_names)
    substrate = reactant_names[0]

    product_names.remove(catalyst)
    product_name = product_names[0]
    print("substrate: ", substrate, "product_name: ", product_name, "catalyst: ", catalyst)
    new_rxn = "((" + k + " * " + catalyst + " * " + substrate + ") / (" + K + " + " + substrate + "))"
    A.firstChild.data = new_rxn
    print(get_node_by_attribute(simple_reaction_node.getElementsByTagName("Kinetics")[0], "Role", "reaction rate").firstChild.data)
    # kinetics.attributes.getNamedItem("KineticsType").firstChild.data = 'GeneralKinetics'

    #removed to test new piece
    kinetics.setAttribute("KineticsType", 'GeneralKinetics')
    get_node_by_attribute(kinetics, "Role", "forward rate constant").setAttribute("Role", 'user defined')
    get_node_by_attribute(kinetics, "Role", "reverse rate constant").setAttribute("Role", 'user defined')
    return simple_reaction_node










flattened_doc = minidom.parse('small_model_6-5-18_flattned.vcml')
original_doc = minidom.parse('small_model_6-5-18_rbm.vcml')
with open("test_output_nochange.vcml", "w") as xml_file:
    flattened_doc.writexml(xml_file)
list_reactions(flattened_doc)
get_species(flattened_doc)

#ob=get_observables(original_doc, ["O0_BTK_tot"])
ob = get_observables(original_doc, get_obs_list(original_doc))


for key, value in ob.items():
    print (key, value)
    flattened_doc = add_output_function_to_simulation(key, value, flattened_doc)

flattened_doc = add_output_function_to_simulation("pLyn_norm", "(pLYN / (3.27 * 9.2961E-4))", flattened_doc)
flattened_doc = add_output_function_to_simulation("pSyk_norm", "(pSYK / 1.18)", flattened_doc)

xml_doc=flattened_doc
xml_doc.getElementsByTagName("SimpleReaction")

t = flattened_doc.getElementsByTagName("SimpleReaction")


for x in t:
    if "BLNK_phos" in x.attributes.getNamedItem("Name").firstChild.data:
        convert_mass_action_to_michaelis_menten(x)
    if "BLNK_dephos" in x.attributes.getNamedItem("Name").firstChild.data:
        convert_mass_action_to_michaelis_menten(x)
    if "CD19_phos" in x.attributes.getNamedItem("Name").firstChild.data:
        convert_mass_action_to_michaelis_menten(x)
    if "CD19_dephos" in x.attributes.getNamedItem("Name").firstChild.data:
        convert_mass_action_to_michaelis_menten(x)
t=flattened_doc.getElementsByTagName("SimpleReaction")

#adds initial conditions

#adds fsyk flyn to math




# new_element = flattened_doc.createElement('Constant')
# new_text = flattened_doc.createTextNode('1.0')
# new_element.appendChild(new_text)
# new_element.setAttribute("Name", "fsyk")
# flattened_doc.getElementsByTagName("MathDescription")[0].appendChild(new_element)
#
# new_element = flattened_doc.createElement('Parameter')
# new_text = flattened_doc.createTextNode('1.0')
# new_element.appendChild(new_text)
# new_element.setAttribute("Name", "fsyk")
# new_element.setAttribute("Role", "user defined")
# new_element.setAttribute("Unit", "l")
# flattened_doc.getElementsByTagName("ApplicationParameters")[0].appendChild(new_element)

IC_species={"BLNK" : 0.65, "pSYK" : "(fsyk * Tsyk * ((syk_e1 * exp( - (t * syk_tau1))) + (syk_e2 * exp( - (t * syk_tau2)))))",
            "pLYN" : "(flyn * Tlyn * ((lyn_e1 * exp( - (t * lyn_tau1))) + (lyn_e2 * exp( - (t * lyn_tau2)))))",
            "BCAP" : 0.9,
            "shp1": 6.9,
            "CD19": 0.83,
            "T_d": 1
            }
for key, val in IC_species.items():
    get_node_by_attribute(flattened_doc.getElementsByTagName("ReactionContext")[0], "LocalizedCompoundRef",
                          key).childNodes[0].firstChild.data = val


for x in t:
    if "BLNK_phos" in x.attributes.getNamedItem("Name").firstChild.data:
        print(x.attributes.getNamedItem("Name").firstChild.data)
        kinetics=x.getElementsByTagName("Kinetics")[0]
        A=get_node_by_attribute(kinetics, "Role", "reaction rate")
        # Ks=get_node_by_attribute(kinetics, 'Role', 'forward rate constant')
        # k, K = Ks.childNodes[0].data.replace("(", "").replace(")", "").split(" + ")
        print(A.firstChild.data)
        rxn=A.firstChild.data
        reactants = x.getElementsByTagName('Reactant')
        reactant_names = []
        for reactant in reactants:
            print(reactant.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
            reactant_names.append(reactant.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)

        products = x.getElementsByTagName('Product')
        product_names = []
        for product in products:
            print(product.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
            product_names.append(product.attributes.getNamedItem("LocalizedCompoundRef").firstChild.data)
        catalyst = list(set(reactant_names) & set(product_names))[0]
        print(reactant_names)
        reactant_names.remove(catalyst)
        print(reactant_names)
        substrate = reactant_names[0]

        product_names.remove(catalyst)
        product_name = product_names[0]
        print("substrate: ", substrate, "product_name: ", product_name, "catalyst: ", catalyst)
        print(kinetics.attributes.getNamedItem("KineticsType").firstChild.data)

with open("test_output_flatadsaf_new.vcml", "w") as xml_file:
    flattened_doc.writexml(xml_file)