import intcode

if __name__ == '__main__':
    with open('day2-intcode.txt') as intcodeData:
        line = intcodeData.readline()
        lunarLander = [int(s) for s in line.split(',')]
        lunarLander[1] = 12
        lunarLander[2] = 2
        output = intcode.runComputer(tuple(lunarLander))
        print(output[0])
