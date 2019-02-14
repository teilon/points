from source import read_file
from output import write_file


def main():

    filename = 'source/points.xlsx'
    data = read_file(filename)
    write_file(data[data['count'] > 20])

    print('done')


if __name__ == '__main__':
    main()
