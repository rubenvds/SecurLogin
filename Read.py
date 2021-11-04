import serial
import multiprocessing
import time


def Read_Card():
    key=170
    cyphertext = []
    bin =[]
    plain_bin=[]
    UID= ""
    print("Wait for the card ")
    ser = serial.Serial("COM5", 9600)
    k = 0  # check which port was really used
    while k < 8:
        x = ser.readline()
        string_ = x.decode()
        if string_[0].isdigit()==True:
            cyphertext.append(string_.split("\r\n")[0])
            k = k + 1
    ser.close()
    print(cyphertext)
    for i in cyphertext :
        x = int (i) #the incripted cyphertext
        y=x^key
        UID=UID+chr(y)
    print(UID)
    return UID




def Read_It():
    p = multiprocessing.Process(target=Read_Card, name="Read_card", args=())
    p.start()

    # Wait 10 seconds for Read_Card
    time.sleep(10)

    # Terminate Read_card
    p.terminate()

    # Cleanup
    p.join()


Read_Card()
