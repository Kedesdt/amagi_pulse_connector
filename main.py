from api_commander import ApiCommander
from tools import get_show_id_by_name
import time
from amagi_commander import Amagi_commander
from serial_commander import SerialCommander
from pulse_filter import PulseFilter
from config import BASE_URL, TOKEN, FEED_CODE, HEADEND, TAKE_NEXT_ACTION_NAME, DELAY, SERIAL_PORT
import argparse
import threading




class Manager:
    def __init__(self, show_id=None):
        self.active = True
        self.show_id = show_id
        self.pulse_filter = PulseFilter()
        self.serial_commander = None #Definido em main()
        self.api_commander = None # Definido em main()
        self.amagi_commander = Amagi_commander(BASE_URL, TOKEN, FEED_CODE)
        if show_id:
            self.amagi_commander.set_show_id(show_id)

    def on_cts_change(self, cts):
        if not cts:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print(t, f"CTS is ON. Enviando TAKE NEXT para Amagi em {DELAY} segundos...")
            time.sleep(float(DELAY))
            print(t, f"Enviando TAKE NEXT para Amagi...")
            if self.active:
                if self.pulse_filter.filter():
                    self.amagi_commander.action(action_name=TAKE_NEXT_ACTION_NAME)
                else:
                    print(t, "Pulse is filtered out. No action will be sent.")
            else:
                print(t, "CTS is ON but the system is inactive. No action will be sent.")
                
        else:
            print("CTS is OFF.")

    def on_dsr_change(self, dsr):
        pass

    def on_action(self):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(t, f"Action triggered. Enviando TAKE NEXT para Amagi em {DELAY} segundos...")
        time.sleep(float(DELAY))
        print(t, f"Enviando TAKE NEXT para Amagi...")
        if self.active:
            self.amagi_commander.action(action_name=TAKE_NEXT_ACTION_NAME)
        else:
            print(t, "Action triggered but the system is inactive. No action will be sent.")

    def update_show_id_from_live_playlist(self):
        last_your = time.strftime("%H", time.localtime(time.time()))
        self.amagi_commander.update_show_id_from_live_playlist()
        while True:
            time.sleep(1)
            if last_your != time.strftime("%H", time.localtime(time.time())):
                time.sleep(60)            
                last_your = time.strftime("%H", time.localtime(time.time()))
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"[{timestamp}] updating show_id from live playlist...")
                self.amagi_commander.update_show_id_from_live_playlist()

    def set_active(self, active=None):
        if active is not None:
            self.active = active
        return self.active
    def get_active(self):
        return self.active

        

    def main(self):
        try:
            self.amagi_commander.update_show_id_from_live_playlist()
        except Exception as e:
            print(f"Error updating show ID from live playlist: {e}")
        self.serial_commander = SerialCommander(port=SERIAL_PORT, baudrate=9600, timeout=1, on_cts=self.on_cts_change, on_dsr=self.on_dsr_change)
        self.serial_commander.start()
        self.api_commander = ApiCommander(callback=self.on_action, host="0.0.0.0", port=1708, set_active=self.set_active, get_active=self.get_active)
        self.api_commander.start()
        self.api_commander.set_pulse_filter(self.pulse_filter)
        
        threading.Thread(target=self.update_show_id_from_live_playlist, daemon=True).start()
        try:
            self.serial_commander.join()
        except KeyboardInterrupt:
            print("Encerrando o sistema...")
        finally:
            self.serial_commander.stop()
            self.serial_commander.join(timeout=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inicia o conector do Pulse.")
    parser.add_argument(
        "--show-id",
        help="ID do show que sera usado nas acoes enviadas ao Amagi.",
    )
    args = parser.parse_args()

    manager = Manager(show_id=args.show_id)
    manager.main()