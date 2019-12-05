from collections import deque
import unittest

class Instruction():
    def __init__(self, memory, inQ, outQ):
        self.memory = memory
        self.inQ = inQ
        self.outQ = outQ

    def getParameter(self,pos,offset):
        modes = list(reversed(getModes(self.memory[pos])))
        val = self.memory[pos+offset]
        immediateMode = modes[offset-1] if offset <= len(modes) else False
        return val if immediateMode else self.memory[val]

class add(Instruction):
    def execute(self,pos):
        outAddr = self.memory[pos+3]
        self.memory[outAddr] = self.getParameter(pos,1) + self.getParameter(pos,2)
        return 4

class mul(Instruction):
    def execute(self,pos):
        outAddr = self.memory[pos+3]
        self.memory[outAddr] = self.getParameter(pos,1) * self.getParameter(pos,2)
        return 4

class inp(Instruction):
    def execute(self,pos):
        self.memory[self.memory[pos+1]] = self.inQ.popleft()
        return 2

class outp(Instruction):
    def execute(self,pos):
        self.outQ.append(self.memory[self.memory[pos+1]])
        return 2

opcode_mappings = {1:add,2:mul,3:inp,4:outp}

def getOpcode(ins):
    digits = [i for i in str(ins)]
    opcode = ''.join(digits[-2:])
    modes = [bool(int(x)) for x in digits[:-2]]
    return int(opcode), modes

def getModes(ins):
    return getOpcode(ins)[1]

def runComputer(memoryTuple, inList=[]):

    memory = list(memoryTuple)
    inQueue = deque(inList)
    output = []
    position = 0
    while True:
        opcode = getOpcode(memory[position])[0]
        if opcode == 99:
            break
        position += opcode_mappings[opcode](memory, inQueue, output).execute(position)
    return tuple(memory), output

class TestIntcode(unittest.TestCase):

    def test_termination(self):
        self.assertEqual(runComputer((99,)), ((99,),[]))

    def test_finalState(self):
        self.assertEqual(runComputer((1,0,0,0,99)), ((2,0,0,0,99),[]))

    def test_runComputer(self):
        self.assertEqual(runComputer((2,3,0,3,99)), ((2,3,0,6,99),[]))
        self.assertEqual(runComputer((2,4,4,5,99,0)), ((2,4,4,5,99,9801),[]))
        self.assertEqual(runComputer((1,1,1,4,99,5,6,0,99)), ((30,1,1,4,2,5,6,0,99), []))

    def test_input(self):
        self.assertEqual(runComputer((3,0,99), [42]), ((42,0,99), []))

    def test_output(self):
        self.assertEqual(runComputer((4,0,99), []), ((4,0,99), [4]))

    def test_inAndOut(self):
        self.assertEqual(runComputer((3,0,4,0,99), [13]), ((13,0,4,0,99), [13]))

    def test_getOpcode(self):
        self.assertEqual(getOpcode(1002), (2, [True, False]))
        self.assertEqual(getOpcode(2),(2,[]))

    def test_mappings(self):
        self.assertEqual(opcode_mappings[2], mul)
        self.assertIsInstance(opcode_mappings[2]([],[],[]), mul)

    def test_execute(self):
        memory = [1,0,0,0]
        self.assertEqual(add(memory, [], []).execute(0), 4)
        self.assertEqual(memory, [2,0,0,0])

        memory = [1101,0,0,0]
        self.assertEqual(add(memory, [], []).execute(0), 4)
        self.assertEqual(memory, [0,0,0,0])

        memory = [1002,4,3,4,33]
        self.assertEqual(mul(memory, [], []).execute(0), 4)
        self.assertEqual(memory, [1002,4,3,4,99])

    def test_runComputerWithParameterModes(self):
        self.assertEqual(runComputer((1002,4,3,4,33)), ((1002,4,3,4,99), []))

    def test_getParameter(self):
        memory = [1002,4,3,4,33]
        self.assertEqual(Instruction(memory, [], []).getParameter(0,1), 33)
        self.assertEqual(Instruction(memory, [], []).getParameter(0,2), 3)

if __name__ == '__main__':
    unittest.main()
