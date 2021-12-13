from Pyro4 import expose
import math

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        print("Workers %d" % len(self.workers))

        (n, m) = self.read_input()
        step = (m - n) / len(self.workers)

        mapped = []
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(n + i * step, n + (i + 1) * step))

        pals = self.reduce_files(mapped)

        self.write_output(pals)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        squares = []
        for n in range(a, b + 1):
            if n >= 1:
                for j in range(int(n / 2) + 1):
                    if (j * j) == n:
                        squares.append(str(n))

        return squares

    @staticmethod
    @expose
    def reduce_files(mapped):
        print("reduce")
        output = []

        for val in mapped:
            print("reduce loop")
            output = output + val.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        a = int(f.readline())
        b = int(f.readline())
        f.close()
        return a, b

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(', '.join(output))
        f.write('\n')
        f.close()
        print("output done")
