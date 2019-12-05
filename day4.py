import unittest

def digits(number):
    return [int(i) for i in str(number)]

def meetCriteria(password):
    repeats = False
    increasing = True
    prev = None
    for d in digits(password):
        if prev == d:
            repeats = True
        if prev is not None and prev > d:
            increasing = False
            break
        prev = d
    return repeats and increasing

def part2(password):
    increasing = True
    prev = None
    groupSizes = []
    for d in digits(password):
        if prev != d:
            # first digit or a new group
            groupSizes.append(1)
        else:
            groupSizes[-1] += 1
        if prev is not None and prev > d:
            increasing = False
            break
        prev = d
    return 2 in groupSizes and increasing

class TestCriteria(unittest.TestCase):
    def test_criteria(self):
        self.assertTrue(meetCriteria(111111))
        self.assertFalse(meetCriteria(223450))
        self.assertFalse(meetCriteria(123789))

    def test_part2(self):
        self.assertFalse(part2(111111))
        self.assertTrue(part2(112233))
        self.assertFalse(part2(123444))
        self.assertTrue(part2(111122))

if __name__ == '__main__':
    count = 0
    p2count = 0
    for pw in range(240298,784956+1):
        if meetCriteria(pw):
            count += 1
        if part2(pw):
            p2count += 1
    print("Part 1 How many: ",count)
    print("Part 2 How many: ",p2count)



