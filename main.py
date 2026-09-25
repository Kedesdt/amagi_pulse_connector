from tools import get_show_id_by_name
from amagi_commander import Amagi_commander
from serial_commander import SerialCommander
from config import BASE_URL, TOKEN, FEED_CODE, HEADEND, TAKE_NEXT_ACTION_NAME, DELAY, SERIAL_PORT

amagi_commander = Amagi_commander(BASE_URL, TOKEN, FEED_CODE)

show_id = None

def on_cts_change(cts):
    if not cts:
        print("CTS is ON. Enviando TAKE NEXT para Amagi...")
        amagi_commander.action(action_name=TAKE_NEXT_ACTION_NAME)
    else:
        print("CTS is OFF.")

def on_dsr_change(dsr):
    pass

def main():
    global show_id
    show_name = input("Enter the show name to get its ID: ")
    show_id = get_show_id_by_name(BASE_URL, TOKEN, show_name)
    
    if show_id:
        print(f"Show ID for '{show_name}': {show_id}")
        amagi_commander.set_show_id(show_id)
        
        serial_commander = SerialCommander(port=SERIAL_PORT, baudrate=9600, timeout=1, on_cts=on_cts_change, on_dsr=on_dsr_change)
        serial_commander.start()
        serial_commander.join()
    else:
        print("Show ID not found. Exiting.")

if __name__ == "__main__":
    main()