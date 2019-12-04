import unittest

def runComputer(machineCodeTuple):

    machineCode = list(machineCodeTuple)
    position = 0
    while True:
        if machineCode[position] == 99:
            return tuple(machineCode)
        if len(machineCode) < 4:
            raise ValueError("Smaller machine code than expected.")
        operation = machineCode[position:position+4]
        opcode, left, right, output = operation
        if (opcode == 1):
            result = machineCode[left] + machineCode[right]
            machineCode[output] = result
        elif opcode == 2:
            result = machineCode[left] * machineCode[right]
            machineCode[output] = result
        position += 4

class TestIntcode(unittest.TestCase):

    def test_termination(self):
        self.assertEqual(runComputer((99,)), (99,))

    def test_finalState(self):
        self.assertEqual(runComputer((1,0,0,0,99)), (2,0,0,0,99))

    def test_runComputer(self):
        self.assertEqual(runComputer((2,3,0,3,99)), (2,3,0,6,99))
        self.assertEqual(runComputer((2,4,4,5,99,0)), (2,4,4,5,99,9801))
        self.assertEqual(runComputer((1,1,1,4,99,5,6,0,99)), (30,1,1,4,2,5,6,0,99))

if __name__ == '__main__':
    unittest.main()
