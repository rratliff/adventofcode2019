from fuel import getFuel

if __name__ == '__main__':
    with open('day1-modules.txt') as moduleData:
        mass = moduleData.readlines()
        print("Spot-check of the first module's mass:",mass[0])
        fuelRequirements = [getFuel(int(moduleMass)) for moduleMass in mass]
        print("Spot-check of the first module's fuel:",fuelRequirements[0])
        print("Answer: ",sum(fuelRequirements))

