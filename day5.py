import intcode

if __name__ == '__main__':

    with open('day5.txt') as intcodeData:
        line = intcodeData.readline()
        diagnostic = [int(s) for s in line.split(',')]
        inp = [1]
        memory, outp = intcode.runComputer(diagnostic, inp)
        print(outp)
