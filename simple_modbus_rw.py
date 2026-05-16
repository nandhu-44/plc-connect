from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian

PLC_HOST = "192.168.1.100"
PLC_PORT = 502
UNIT_ID = 1

REGISTER_ADDR = 0  # holding register address (often zero-based)
WRITE_VALUE = 123456  # 32-bit integer

def main():
    client = ModbusTcpClient(host=PLC_HOST, port=PLC_PORT)
    if not client.connect():
        raise RuntimeError("Failed to connect to PLC")

    # Read two holding registers (32-bit value)
    rr = client.read_holding_registers(REGISTER_ADDR, count=2, unit=UNIT_ID)
    if rr.isError():
        print("Read error:", rr)
    else:
        decoder = BinaryPayloadDecoder.fromRegisters(
            rr.registers,
            byteorder=Endian.BIG,
            wordorder=Endian.BIG,
        )
        print("Read value:", decoder.decode_32bit_int())

    # Write two holding registers (32-bit value)
    builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
    builder.add_32bit_int(WRITE_VALUE)
    payload = builder.to_registers()
    wr = client.write_registers(REGISTER_ADDR, payload, unit=UNIT_ID)
    if wr.isError():
        print("Write error:", wr)
    else:
        print("Write OK")

    client.close()

if __name__ == "__main__":
    main()