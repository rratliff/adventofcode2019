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

    def setParameter(self, pos,offset, val):
        self.memory[self.memory[pos+offset]] = val

class add(Instruction):
    def execute(self,pos):
        self.setParameter(pos,3, self.getParameter(pos,1) + self.getParameter(pos,2))
        return pos+4

class mul(Instruction):
    def execute(self,pos):
        self.setParameter(pos,3, self.getParameter(pos,1) * self.getParameter(pos,2))
        return pos+4

class inp(Instruction):
    def execute(self,pos):
        self.setParameter(pos,1,self.inQ.popleft())
        return pos+2

class outp(Instruction):
    def execute(self,pos):
        self.outQ.append(self.getParameter(pos,1))
        return pos+2

class jit(Instruction):
    def execute(self,pos):
        return self.getParameter(pos,2) if self.getParameter(pos,1) != 0 else pos+3

class jif(Instruction):
    def execute(self, pos):
        return self.getParameter(pos,2) if self.getParameter(pos,1) == 0 else pos+3

class lt(Instruction):
    def execute(self,pos):
        self.setParameter(pos,3, 1 if self.getParameter(pos,1) < self.getParameter(pos,2) else 0)
        return pos + 4

class eq(Instruction):
    def execute(self, pos):
        self.setParameter(pos,3, 1 if self.getParameter(pos,1) == self.getParameter(pos,2) else 0)
        return pos+4

opcode_mappings = {1:add,2:mul,3:inp,4:outp,5:jit,6:jif,7:lt,8:eq}

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
        position = opcode_mappings[opcode](memory, inQueue, output).execute(position)
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

    def test_comparison(self):
        equalityComputer = (3,9,8,9,10,9,4,9,99,-1,8)
        self.assertEqual(runComputer(equalityComputer, [9])[1], [0])
        self.assertEqual(runComputer(equalityComputer, [8])[1], [1])
        lt8Computer = (3,9,7,9,10,9,4,9,99,-1,8)
        self.assertEqual(runComputer(lt8Computer, [8])[1], [0])
        self.assertEqual(runComputer(lt8Computer, [-42])[1], [1])
        eq8Computer = (3,3,1108,-1,8,3,4,3,99)
        self.assertEqual(runComputer(eq8Computer, [8])[1], [1])
        self.assertEqual(runComputer(eq8Computer, [-42])[1], [0])
        lt8Computer = (3,3,1107,-1,8,3,4,3,99)
        self.assertEqual(runComputer(lt8Computer, [8])[1], [0])
        self.assertEqual(runComputer(lt8Computer, [-42])[1], [1])

    def test_jump(self):
        jumpComputerPosMode = (3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9)
        self.assertEqual(runComputer(jumpComputerPosMode, [0])[1], [0])
        self.assertEqual(runComputer(jumpComputerPosMode, [1])[1], [1])
        jumpImmediateMode = (3,3,1105,-1,9,1101,0,0,12,4,12,99,1)
        self.assertEqual(runComputer(jumpImmediateMode, [0])[1], [0])
        self.assertEqual(runComputer(jumpImmediateMode, [1])[1], [1])

    def test_largerExample(self):
        largerExample = (3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, \
                1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,\
                999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99)
        self.assertEqual(runComputer(largerExample, [0])[1], [999])
        self.assertEqual(runComputer(largerExample, [8])[1], [1000])
        self.assertEqual(runComputer(largerExample, [20])[1], [1001])
if __name__ == '__main__':
    unittest.main()
