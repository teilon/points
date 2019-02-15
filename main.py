from source import read_file
from output import write_file
from db import db_connet


def main():

    filename = 'source/points.xlsx'
    data = read_file(filename)
    write_file(data[data['count'] > 20])

    db_connet()
    print('done')


if __name__ == '__main__':
    main()
