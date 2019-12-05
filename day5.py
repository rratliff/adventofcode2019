import intcode

if __name__ == '__main__':

    with open('day5.txt') as intcodeData:
        line = intcodeData.readline()
        diagnostic = [int(s) for s in line.split(',')]
        diagOriginal = tuple(diagnostic)
        inp = [1]
        memory, outp = intcode.runComputer(diagnostic, inp)
        print("Part 1, air conditioning",outp)

        inp = [5]
        memory, outp = intcode.runComputer(diagOriginal, inp)
        print("Part 2, thermal radiator", outp)
