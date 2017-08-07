class PValueCounter:
    def __init__(self, alpha=0.01):
        self.alpha = alpha
        self.total_passed = 0
        self.total_tested = 0
        self.arr = []
        for i in range(0, 10):
            self.arr.append(0)

    def get_proportions(self):
        return self.total_passed / self.total_tested

    def reset(self):
        self.total_passed = 0
        self.total_tested = 0
        self.arr = []
        for i in range(0, 10):
            self.arr.append(0)

    def count_p_values_in_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                self.get_num_into_array(float(line))

    def get_num_into_array(self, num):
        if (num >= 0.0) and (num < 0.1):
            self.arr[0] += 1
        elif (num >= 0.1) and (num < 0.2):
            self.arr[1] += 1
        elif (num >= 0.2) and (num < 0.3):
            self.arr[2] += 1
        elif (num >= 0.3) and (num < 0.4):
            self.arr[3] += 1
        elif (num >= 0.4) and (num < 0.5):
            self.arr[4] += 1
        elif (num >= 0.5) and (num < 0.6):
            self.arr[5] += 1
        elif (num >= 0.6) and (num < 0.7):
            self.arr[6] += 1
        elif (num >= 0.7) and (num < 0.8):
            self.arr[7] += 1
        elif (num >= 0.8) and (num < 0.9):
            self.arr[8] += 1
        else:
            self.arr[9] += 1 # TODO: [0.9, 1.0) interval ???
        # TODO: > or >= ???
        if num > self.alpha:
            self.total_passed += 1
        self.total_tested += 1