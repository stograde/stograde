import statistics
import sys

def avg(data):
    return sum(data) / len(data)

def stdev(data):
    return statistics.stdev(data)

def main():
    data = sys.stdin.read().split()
    data = [int(datum) for datum in data]

    print('Average: {}'.format(avg(data)))
    print('Std Dev: {}'.format(stdev(data)))

if __name__ == '__main__':
    main()

