from tools import get_show_id_by_name
import time
from amagi_commander import Amagi_commander
from serial_commander import SerialCommander
from config import BASE_URL, TOKEN, FEED_CODE, HEADEND, TAKE_NEXT_ACTION_NAME, DELAY, SERIAL_PORT
import threading

amagi_commander = Amagi_commander(BASE_URL, TOKEN, FEED_CODE)

show_id = None

def on_cts_change(cts):
    if not cts:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(t, "CTS is ON. Enviando TAKE NEXT para Amagi...")
        amagi_commander.action(action_name=TAKE_NEXT_ACTION_NAME)
    else:
        print("CTS is OFF.")

def on_dsr_change(dsr):
    pass

def update_show_id_from_live_playlist():
    last_your = time.strftime("%H", time.localtime(time.time()))
    amagi_commander.update_show_id_from_live_playlist()
    while True:
        if last_your != time.strftime("%H", time.localtime(time.time())):
            last_your = time.strftime("%H", time.localtime(time.time()))
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"[{timestamp}] updating show_id from live playlist...")
            amagi_commander.update_show_id_from_live_playlist()
    

def main():
    global show_id
    
    amagi_commander.update_show_id_from_live_playlist()    
    serial_commander = SerialCommander(port=SERIAL_PORT, baudrate=9600, timeout=1, on_cts=on_cts_change, on_dsr=on_dsr_change)
    serial_commander.start()
    threading.Thread(target=update_show_id_from_live_playlist, daemon=True).start()
    serial_commander.join()


if __name__ == "__main__":
    main()