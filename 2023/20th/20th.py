import sys
import re
from enum import Enum

# Enumeration Types
class Pulse(Enum):
    LOW  = 0
    HIGH = 1
    
class State(Enum):
    OFF = 0
    ON  = 1

# Class Definitions
class Simulator():
    def __init__(self, netlist):
        self.netlist = netlist
        self.total_events = []
        self.sim_time = 0
            
    def run_sim(self, times=1):
        self.sim_time = times
        
        for t in range(times):
            events = []
            events += self.netlist['broadcaster'].update_output()
            
            while events:
                new_events = []
                for e in events:  
                    e[2].set_input(e[0], e[1])
                    new_events += e[2].update_output()
                self.total_events += events
                events = new_events    
            
            # for e in self.total_events:
            #     print(f'{e[1]} {e[0]} {e[2]}')

                    
    def result_part1(self):
        acc_h = sum([1 for e in self.total_events if e[0] == Pulse.HIGH ]) 
        acc_l = sum([1 for e in self.total_events if e[0] == Pulse.LOW ]) + self.sim_time 
        
        return acc_h * acc_l

class Component():
    
    def __init__(self, name):
        self.name = name
        self.outputs = [] 
        self.inputs = []
        self.state = State.OFF 
    
    def set_input(self, pulse, component):
        pass
    
    def update_output(self):
        return [] 
    
    def add_input(self, input):
        self.inputs.append(input)
        
    def add_output(self, output):
        self.outputs.append(output)
        
    def __str__(self):
        return f"{self.name}"
    
    def reset_state(self):
        self.state = State.OFF
    
class Inverter(Component):
    
    def __init__(self, name):
        super().__init__(name)
        self.state = [State.OFF] * len(self.inputs)
        
    def set_input(self, pulse, component):
        for i, input in enumerate(self.inputs):
            if input == component:
                if pulse == Pulse.LOW:
                    self.state[i] = State.OFF
                else:
                    self.state[i] = State.ON
    
    def update_output(self):
        events = []
        
        if self.state == ([State.ON] * len(self.inputs)):
            output = Pulse.LOW
        else:
            output = Pulse.HIGH

        for o in self.outputs:
            events.append((output, self, o))
        
        return events
    
    def add_input(self, input):
        self.inputs.append(input)
        self.state = [State.OFF] * len(self.inputs)
        
    def reset_state(self):
        self.state = [State.OFF] * len(self.inputs)
        
        
class FlipFlop(Component):
    
    def __init__(self, name):
        super().__init__(name)
        self.state = State.OFF
        self.switched = False
         
    def set_input(self, pulse, component):
        if pulse == Pulse.LOW:
            self.state = State.OFF if self.state == State.ON else State.ON
            self.switched = True
        else:
            self.switched = False
    
    def update_output(self):
        events = []
        
        if self.switched:
            if self.state == State.ON:
                output = Pulse.HIGH
            else:
                output = Pulse.LOW

            for o in self.outputs:
                events.append((output, self, o))
                
            self.switched = False
        return events
            
    def reset_state(self):
        self.state = State.OFF
        self.switched = False

class Broadcaster(Component):
    
    def __init__(self, name, inputs=[], outputs=[]):
        super().__init__(name)
        self.state = State.OFF
    
    def set_input(self, pulse, component):
        if pulse == Pulse.HIGH:
            self.state = State.ON
        else:
            self.state = State.OFF
    
    def update_output(self):
        events = []
        
        if self.state == State.ON:
            output = Pulse.HIGH
        else:
            output = Pulse.LOW

        for o in self.outputs:
            events.append((output, self, o))
            
        return events
    
    def reset_state(self):
        self.state = State.OFF
        
class Terminal(Component):
    
    def __init__(self, name):
        super().__init__(name)

# File Parsing
f = open(sys.argv[1], 'r')
lines = f.read().splitlines()
netlist = {}

def create_netlist(netlist):
    netlist_inst = {}
    
    # First pass instanciating components
    for comp_name in netlist.keys():
        if netlist[comp_name][0] == '%':
            netlist_inst[comp_name] = FlipFlop(comp_name)
        elif netlist[comp_name][0] == '&':
            netlist_inst[comp_name] =  Inverter(comp_name)
        elif netlist[comp_name][0] == 'broadcaster':
            netlist_inst[comp_name] =  Broadcaster(comp_name)
        else:
            raise Exception(f'component type {netlist[name][0]} not recognized')

    # Second pass linking components
    for comp_name in netlist.keys():
        for out_name in netlist[comp_name][2]:
            if not out_name in netlist_inst:
                netlist_inst[out_name] = Terminal(out_name)
            netlist_inst[comp_name].add_output(netlist_inst[out_name])
            netlist_inst[out_name].add_input(netlist_inst[comp_name])
            
    return netlist_inst
    
for l in lines: 
    m = re.match(r"(?:([%&])(\w+)|(broadcaster))\s*->\s*([a-zA-Z0-9,\s]+)",l)
    # outputs = re.findall(r"")
    if m: 
        type = m.group(1) if m.group(1) else m.group(3) 
        name = m.group(2)
        outputs = [s.strip() for s in m.group(4).split(',')]
        
        if type == 'broadcaster':
            netlist[type] = (type, type, outputs)
        else:
            netlist[name] = (type, name, outputs)
    else:
        raise Exception("can't parse the line in file")    

netlist_inst = create_netlist(netlist)
# print(len(netlist))
# for c in netlist_inst:
#     print(netlist_inst[c])
# print(netlist_inst['inv'].state)
# print(len(netlist_inst))

# Part 1 Implementation 
sim = Simulator(netlist_inst)
sim.run_sim(times=1000)
res1 = sim.result_part1()

# Part 2 Implementation 
res2 = 0

# Printing Results
print(f'Result of the pulses multiplication (Part 1) {res1}')