import intcode

if __name__ == '__main__':
    with open('day2-intcode.txt') as intcodeData:
        line = intcodeData.readline()
        lunarLander = [int(s) for s in line.split(',')]
        lunarLanderPristine = tuple(lunarLander)
        lunarLander[1] = 12
        lunarLander[2] = 2
        output = intcode.runComputer(tuple(lunarLander))
        print("Part 1 answer: ",output[0])

        for noun in range(0,100):
            for verb in range(0,100):
                lunarLander = list(lunarLanderPristine)
                lunarLander[1] = noun
                lunarLander[2] = verb
                output = intcode.runComputer(tuple(lunarLander))
                if output[0] == 19690720:
                    print("Found it!")
                    print("noun",noun)
                    print("verb",verb)
                    print("magic answer:",100*noun+verb)
                    exit(0)
                else:
                    print("tried noun {}, verb {}, got answer {}".format(noun, verb, output[0]))
