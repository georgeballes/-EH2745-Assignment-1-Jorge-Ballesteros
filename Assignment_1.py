# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:24:38 2020

@author: georg
"""


# First thing we need to do is to import the ElementTree library
import xml.etree.ElementTree as ET
#import the pandapower module
import pandapower as pp
#import the pandapower plotting module
import pandapower.plotting as plot

def execute_my_script(EQ_file, SSH_file):
    #Next step is to create a tree by parsing the XML file referenced
    # We are here using ENTSO-E  model files used in Interoperability testing
    
    EQ_tree = ET.parse(EQ_file)
    SSH_tree = ET.parse(SSH_file)
    # We can access the root (raiz) of the tree and print it
    EQ_microgrid = EQ_tree.getroot()
    SSH_microgrid = SSH_tree.getroot()
    
    # To make working with the file easier, it may be useful to store the 
    # namespace identifiers in strings and reuse when you search for tags
        
    ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
          'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
          'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}
    
    
    #create an empty network 
    net = pp.create_empty_network()
    
    #to see al the elements in our system:
    EQ_tag=[]
    for eq in EQ_microgrid:
         if (ns['cim'] in eq.tag):
             equipment = eq.tag.replace("{"+ns['cim']+"}","")
             if equipment not in EQ_tag :
                 EQ_tag.append(equipment)
    print(EQ_tag)
    print("---------------------------------------------------------")
    
    # My goal here it's to create a dictionary that links voltage level with their respective ID
    
    # I want to to avoid repetition in the loop when finding the match voltage level of the equipment
    voltage_levels_dic = {}
    for voltage_level in EQ_microgrid.findall('cim:VoltageLevel', ns):
        voltage_name = float(voltage_level.find('cim:IdentifiedObject.name', ns).text)
        voltage_levels_dic[voltage_level.attrib.get(ns['rdf']+'ID')] = voltage_name
    print(voltage_levels_dic)
    
    # Create buses in the pandapower system from the XML file data adquired
    for bus in EQ_microgrid.findall('cim:BusbarSection', ns):
        # Extracting the name from the BusbarSection element
        bus_name = bus.find('cim:IdentifiedObject.name', ns).text
        # I the next line of code we want to obtain the Equipment.EquipmentContainer ID of each busbar section and take with it the corresponding bus 
        # voltage level relation that we have previously determined in the dictionary
        bus_voltage_level = voltage_levels_dic[bus.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')]
        pp.create_bus(net, bus_voltage_level, name=bus_name)
    
    print(net.bus)
    print("---------------------------------------------------------")
    
    # Create lines in the pandapower system from the XML file data adquired
    for line in EQ_microgrid.findall('cim:ACLineSegment', ns):
        #I want to get the ID of each line
        line_id = line.attrib.get(ns['rdf'] + 'ID')
        print (line_id)
        # next step will be retrieving the name of the line
        line_name =  line.find('cim:IdentifiedObject.name', ns).text
        print (line_name)
        # Now I want to get the length of the line
        line_length = float(line.find('cim:Conductor.length', ns).text)
        print (line_length)
        # get the resistance of the line
        line_resistance_per_km = float(line.find('cim:ACLineSegment.r', ns).text)/line_length
        # get the reactance of the line
        line_rectance_per_km = float(line.find('cim:ACLineSegment.x', ns).text)/line_length
        # I want to find the ID of the terminals where the line is connected to
        # Basically we want to know to wich 2 terminals each line is connected to in order to later define
        # from/to which buses the lines are connected to 
        for terminal in EQ_microgrid.findall('cim:Terminal', ns):
            line_Te_CE = terminal.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            line_sequence_number = terminal.find('cim:ACDCTerminal.sequenceNumber', ns).text
            if line_id == line_Te_CE: # We do this in order to select the terminals related to the lines
                if line_sequence_number == '1': 
                    #This is because for each line we have 2 terminals, the one with sequence number 1 and the other with seq number 2
                    # Gets the connectivity node ID from the terminals
                    line_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') 
                    # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                    # I want to obtain for each connectivitynode their corresponding id and container association
                    for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                        if CN.attrib.get(ns['rdf'] + 'ID') == line_Te_CN:
                            CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                            CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                    for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                        if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                            Line_Te1 = BusBar.find('cim:IdentifiedObject.name', ns).text
                elif line_sequence_number == '2':
                 # Gets the connectivity node ID from the terminals
                    line_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') 
                    # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                    # I want to obtain for each connectivitynode their corresponding id and container association
                    for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                        if CN.attrib.get(ns['rdf'] + 'ID') == line_Te_CN:
                            CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                            CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                    for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                        if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                            Line_Te2 = BusBar.find('cim:IdentifiedObject.name', ns).text
        Line_from_Bus = pp.get_element_index(net, "bus", Line_Te1)
        Line_to_Bus = pp.get_element_index(net, "bus", Line_Te2)
        pp.create_line(net, Line_from_Bus, Line_to_Bus, length_km=line_length,std_type='NAYY 4x50 SE', name=line_name)# parallel=hv_line.parallel)
    
    # show line table
    print(net.line)
    print("---------------------------------------------------------")
    
    
    # Create transformers in the pandapower system from the XML file data adquired
    for transformers in EQ_microgrid.findall('cim:PowerTransformer', ns):
        #I want to get the ID of each transformer
        transformer_id = transformers.attrib.get(ns['rdf'] + 'ID')
        # next step will be retrieving the name of the transformer
        transformers_name = transformers.find('cim:IdentifiedObject.name', ns).text
        print(transformers_name)
        # I want to find the ID of the terminals where the transformer is connected to
        for transformer_end in EQ_microgrid.findall('cim:PowerTransformerEnd', ns):
            transformer_end_id = transformer_end.find('cim:PowerTransformerEnd.PowerTransformer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            # Find the side of the power transformer
            if transformer_id == transformer_end_id:
                transformer_end_number = transformer_end.find('cim:TransformerEnd.endNumber', ns).text
                # I want to find the value of the TransformerEnd.endNumber because it will give you the information about if 
                # it is the HV(=1) or LV(=2) 
                print(transformer_end_number)
                
                if transformer_end_number == '1':
                # As we did previously for the lines we use did if in order to create 2 paths, one will define the
                # parameters of HV side and the other the parameters of the LV side
                # I am taking the information of the transformer, Power rating of the transformer 
                # The parameters are taking on the  HV(=1) side because is where the data about r,x is stored at the XML file
                    transformer_S = float(transformer_end.find('cim:PowerTransformerEnd.ratedS', ns).text)
                    transformer_hv_kv = float(transformer_end.find('cim:PowerTransformerEnd.ratedU', ns).text)
                    transformer_r = float(transformer_end.find('cim:PowerTransformerEnd.r', ns).text)
                    transformer_x = float(transformer_end.find('cim:PowerTransformerEnd.x', ns).text)
                    transformer_z = (transformer_r ** 2 + transformer_x ** 2) ** (1/2)
                    # I am going to neglect the iron losses, the open loop losses, shift degree
                    # Find the terminal the transformer end is connected to
                    transformer_end_terminal = transformer_end.find('cim:TransformerEnd.Terminal', ns).attrib.get(ns['rdf'] + 'resource').replace('#','')
                    for terminal in EQ_microgrid.findall('cim:Terminal', ns):
                        terminal_id = terminal.attrib.get(ns['rdf'] + 'ID')
                        if terminal_id == transformer_end_terminal:
                            # Take the connectivity node's ID from the terminal
                            transformer_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                            # I want to obtain for each connectivitynode their corresponding id and container association
                            for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                                if CN.attrib.get(ns['rdf'] + 'ID') == line_Te_CN:
                                    transformer_CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                                    transformer_CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                            for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                                if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                                    transformer_Te1 = BusBar.find('cim:IdentifiedObject.name', ns).text
                # Now we want to do the same for the LV side                    
                elif transformer_end_number == '2':
                    transformer_lv_kv = float(transformer_end.find('cim:PowerTransformerEnd.ratedU', ns).text)
                    # Find the terminal the transformer end is connected to
                    transformer_end_terminal = transformer_end.find('cim:TransformerEnd.Terminal', ns).attrib.get(ns['rdf'] + 'resource').replace('#','')
                    for terminal in EQ_microgrid.findall('cim:Terminal', ns):
                        terminal_id = terminal.attrib.get(ns['rdf'] + 'ID')
                        if terminal_id == transformer_end_terminal:
                            # Take the connectivity node's ID from the terminal
                            transformer_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                            # I want to obtain for each connectivitynode their corresponding id and container association
                            for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                                if CN.attrib.get(ns['rdf'] + 'ID') == line_Te_CN:
                                    transformer_CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                                    transformer_CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                            for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                                if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                                    transformer_Te2 = BusBar.find('cim:IdentifiedObject.name', ns).text
                                    
        hv_bus = pp.get_element_index(net, "bus", transformer_Te1)
        lv_bus = pp.get_element_index(net, "bus", transformer_Te2)
        pp.create_transformer_from_parameters(net, hv_bus, lv_bus, sn_mva=transformer_S, vn_hv_kv=transformer_hv_kv, vn_lv_kv=transformer_lv_kv, vkr_percent=0.06,
                                          vk_percent=8, pfe_kw=0, i0_percent=0, tp_pos=0, shift_degree=0, name=transformers_name)
    
    print(net.trafo) # show trafo table  
    print("---------------------------------------------------------")
    
    # Create Loads in the pandapower system from the XML file (SSH) data adquired
    # In order to do this, firs we will take the name and ID of the loads from the EQ file, afterwards we will use this
    # Id that we have obtained before to look for its corresponding P & Q data stored in the SSH file
    
    for load in EQ_microgrid.findall('cim:EnergyConsumer', ns):
        #I want to get the ID of each load
        eq_load_id = load.attrib.get(ns['rdf'] + 'ID')
        # next step will be retrieving the name of the load
        load_name = load.find('cim:IdentifiedObject.name', ns).text
        print(load_name)
        for ssh_load in SSH_microgrid.findall('cim:EnergyConsumer', ns):
            ssh_load_id = ssh_load.attrib.get(ns['rdf'] + 'about').replace('#', '')
            print(ssh_load_id)
            if ssh_load_id == eq_load_id:
                P_load = float(ssh_load.find('cim:EnergyConsumer.p', ns).text)
                Q_load = float(ssh_load.find('cim:EnergyConsumer.q', ns).text)
        # After we got the P & Q for each load, now I want to find the terminal associated to each load (from the EQ file again)
        for terminal in EQ_microgrid.findall('cim:Terminal', ns):
            load_Te_CE = terminal.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            if eq_load_id == load_Te_CE: # We do this in order to select the terminals related to the loads
                load_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') 
                # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                # I want to obtain for each connectivitynode their corresponding id and container association
                for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                        if CN.attrib.get(ns['rdf'] + 'ID') == load_Te_CN:
                            CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                            CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                    if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                        Load_Te = BusBar.find('cim:IdentifiedObject.name', ns).text
                        
        bus_idx = pp.get_element_index(net, "bus", Load_Te)
        pp.create_load(net, bus_idx, p_mw=P_load, q_mvar=Q_load, name=load_name)
    
    # show load table
    print(net.load)
    print("---------------------------------------------------------")
    
    # Create generators in pandapower, 
    for generator in EQ_microgrid.findall('cim:GeneratingUnit', ns):
        generator_id = generator.attrib.get(ns['rdf'] + 'ID')
        generator_name = generator.find('cim:IdentifiedObject.name', ns).text
        generator_initial_P = float(generator.find('cim:GeneratingUnit.initialP', ns).text)
        # Looking for the SynchronousMachine related to the generator unit
        for synch_machine in  EQ_microgrid.findall('cim:SynchronousMachine', ns):
            synch_machine_id = synch_machine.attrib.get(ns['rdf'] + 'ID')
            if synch_machine.find('cim:RotatingMachine.GeneratingUnit', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == generator_id:
                synch_machine_ratedU = float(synch_machine.find('cim:RotatingMachine.ratedU', ns).text)
                # print(synch_machine_ratedU)
                synch_machine_id = synch_machine.attrib.get(ns['rdf'] + 'ID')
                synch_machine_equip_cont = synch_machine.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
        
        for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
            BusBar_equip_cont = BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            if BusBar_equip_cont == synch_machine_equip_cont:
                generator_busbar = BusBar.find('cim:IdentifiedObject.name', ns).text
                bus_voltage = voltage_levels_dic[BusBar_equip_cont]
               # print(bus_voltage)
                vm_pu = synch_machine_ratedU / bus_voltage
                print(vm_pu)
        pp.create_gen(net, pp.get_element_index(net, "bus", generator_busbar), generator_initial_P, vm_pu, name=generator_name)    
        # vm_pu=1.0 this is because there is no extra info about vm_pu in the xml file. Thus, as the rated voltage 
        # of the synch.machine is exactly the same as the bus which it is connected
        # Find the terminal the generator is connected to
    print(net.gen)
    print("---------------------------------------------------------")
    
    # Create shunt capacitors in pandapower. 
    # To define shunt in pandapower we need: the bus that is connected to, p_mw=0, q_mvar, name.
    for shunt in EQ_microgrid.findall('cim:LinearShuntCompensator', ns):
        shunt_id = shunt.attrib.get(ns['rdf'] + 'ID')
        shunt_name = shunt.find('cim:IdentifiedObject.name', ns).text
        shunt_b = float(shunt.find('cim:LinearShuntCompensator.bPerSection', ns).text)
        shunt_nom_U = float(shunt.find('cim:ShuntCompensator.nomU', ns).text)
        # In a shunt capacitor, Q = b*(Unom^2) because g = 0
        shunt_Q = shunt_b*(shunt_nom_U**2)
        shunt_equip_cont = shunt.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
        for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
            BusBar_equip_cont = BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            if BusBar_equip_cont == shunt_equip_cont:
                shunt_busbar = BusBar.find('cim:IdentifiedObject.name', ns).text
        
        pp.create_shunt(net, pp.get_element_index(net, "bus", shunt_busbar), p_mw=0, q_mvar=shunt_Q, name=shunt_name)
    
            
    print(net.shunt)
    print("---------------------------------------------------------")
    
    # Create breakers in pandapower. 
    for breaker in EQ_microgrid.findall('cim:Breaker', ns):
        breaker_id = breaker.attrib.get(ns['rdf'] + 'ID')
        breaker_name = breaker.find('cim:IdentifiedObject.name', ns).text
        breaker_position = breaker.find('cim:Switch.normalOpen', ns).text
        # Breaker position in the EQ.xml file determines if the sitch is open(=TRUE), but for pandapower
        # the parameteres examines if the switch is closed(=FALSE), thi is why we need to create
        # an if condition to readjust this as we want
        if breaker_position == 'false':
            breaker_position = True
        elif breaker_position == 'true':
            breaker_position = False
        # I want to find the ID of the terminals where the breaker is connected to
        # Basically we want to know to wich 2 terminals each breaker is connected to in order to later define
        # from/to which buses the breaker are connected to 
        for terminal in EQ_microgrid.findall('cim:Terminal', ns):
            breaker_Te_CE = terminal.find('cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
            breaker_sequence_number = terminal.find('cim:ACDCTerminal.sequenceNumber', ns).text
            if breaker_id == breaker_Te_CE:
                if breaker_sequence_number == '1':
                # Take the connectivity node's ID from the terminal
                    breaker_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                    # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                    # I want to obtain for each connectivitynode their corresponding id and container association
                    for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                        if CN.attrib.get(ns['rdf'] + 'ID') == breaker_Te_CN:
                            CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                            CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                     # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                     # and the corresponding busbarsection 
                    for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):                    
                        if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                            breaker_Te1 = BusBar.find('cim:IdentifiedObject.name', ns).text
                            print(breaker_Te1)
                elif breaker_sequence_number == '2':
                    # Gets the connectivity node ID from the terminals
                    breaker_Te_CN = terminal.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') 
                    # With this new for loop the objective is to find the ConnectivityNode associaton, in other words
                    # I want to obtain for each connectivitynode their corresponding id and container association
                    for CN in EQ_microgrid.findall('cim:ConnectivityNode', ns):
                        if CN.attrib.get(ns['rdf'] + 'ID') == line_Te_CN:
                            CN_id = CN.attrib.get(ns['rdf'] + 'ID')
                            CN_container = CN.find('cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '')
                            # I want now to stablish a connection between the ConnectivityNode.ConnectivityNodeContainer
                            # and the corresponding busbarsection 
                    for BusBar in EQ_microgrid.findall('cim:BusbarSection', ns):
                        if BusBar.find('cim:Equipment.EquipmentContainer', ns).attrib.get(ns['rdf'] + 'resource').replace('#', '') == CN_container:
                            breaker_Te2 = BusBar.find('cim:IdentifiedObject.name', ns).text
                            print(breaker_Te2)
                            print("---------------------------------------------------------")
    
        from_bus = pp.get_element_index(net, "bus", breaker_Te1)
        to_bus = pp.get_element_index(net, "bus", breaker_Te2)
        pp.create_switch(net, from_bus, to_bus, et='b', closed=breaker_position, type='CB', name=breaker_name)
    
    print(net.switch)
    
    plot.to_html(net, 'plot_system.html')
    #plot.simple_plot(net, respect_switches=False, line_width=1.0, bus_size=1.0, ext_grid_size=1.0, trafo_size=1.0, plot_loads=False, plot_sgens=False, load_size=1.0, sgen_size=1.0, switch_size=2.0, 
     #                switch_distance=1.0, plot_line_switches=False, scale_size=True, bus_color='b', line_color='grey', trafo_color='k', ext_grid_color='y', switch_color='k', library='igraph', show_plot=True, ax=None)               
                    
                    
#execute_my_script('MicroGridTestConfiguration_T1_BE_EQ_V2.xml', 'MicroGridTestConfiguration_T1_BE_SSH_V2.xml')                 