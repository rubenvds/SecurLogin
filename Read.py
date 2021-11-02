import serial
import multiprocessing
import time


def Read_Card():
    print("Wait for the card ")
    ser = serial.Serial("COM3", 9600)
    k = 0;  # check which port was really used
    while k == 0:
        x = ser.readline()
        str = x.decode()
        if str.find("UID") != -1:
            k = 1
    ser.close()
    print(str[10:])
    return str


Read_Card()
def Read_It():
    if __name__ == '__main__':
        p = multiprocessing.Process(target=Read_Card, name="Read_card", args=())
        p.start()

        # Wait 10 seconds for Read_Card
        time.sleep(10)

        # Terminate Read_card
        p.terminate()

        # Cleanup
        p.join()
