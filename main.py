import render
from growth import *


def main():
    ga = setup()
    render.setup(ga)
    render.start()

if __name__ == '__main__':
    main()