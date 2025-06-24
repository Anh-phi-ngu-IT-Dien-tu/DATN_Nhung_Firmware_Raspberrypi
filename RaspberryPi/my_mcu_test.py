from my_mcu import MyMCU
import time

mcu = MyMCU("COM29", 115200)
mcu.start()

# # read() test case
# try:
#     while True:
#         print(mcu.read())
#         time.sleep(0.5)
# except KeyboardInterrupt:
#     mcu.stop()

# write() test case
mcu.write(333.3333, 14444.4444)
mcu.stop()