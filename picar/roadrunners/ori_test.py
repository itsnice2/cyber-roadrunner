import time
from ori import Ori as fu
import picar_4wd as fc
speed = 100

def main():
    fu.geradeaus(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()