from pymodbus.client import ModbusTcpClient
import time

PLC_HOST = "192.168.1.231"
PLC_PORT = 502
UNIT_ID = 1

AHU_ON_ADDR = 8990            # BOOL (Write Coil)

def main():
    client = ModbusTcpClient(host=PLC_HOST, port=PLC_PORT)
    if not client.connect():
        raise RuntimeError(f"Failed to connect to PLC at {PLC_HOST}:{PLC_PORT}")

    # 1. Read current status
    print("Reading current AHU status...")
    rr = client.read_coils(AHU_ON_ADDR, count=1, unit=UNIT_ID)
    if rr.isError():
        print("Error reading status:", rr)
        client.close()
        return

    original_state = rr.bits[0]
    print(f"Current AHU status is: {'ON' if original_state else 'OFF'} ({original_state})")

    # 2. Toggle status
    new_state = not original_state
    print(f"Toggling AHU state to: {'ON' if new_state else 'OFF'}...")
    cw = client.write_coil(AHU_ON_ADDR, new_state, unit=UNIT_ID)
    if cw.isError():
        print("Error toggling state:", cw)
    else:
        print("Toggle successful.")

    # 3. Wait 2 seconds
    time.sleep(2)

    # 4. Revert to original state
    print(f"Reverting AHU back to original state: {'ON' if original_state else 'OFF'}...")
    cw = client.write_coil(AHU_ON_ADDR, original_state, unit=UNIT_ID)
    if cw.isError():
        print("Error reverting state:", cw)
    else:
        print("Revert successful.")

    client.close()

if __name__ == "__main__":
    main()