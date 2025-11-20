import logging
import random
import time
import threading

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusServerContext,
    ModbusSequentialDataBlock,
)
from pymodbus.device import ModbusDeviceIdentification

"""
HR map (holding registers):

HR0 = PROCESS_VALUE  (symulowana wartość procesu, 0–100, tylko READ z HMI)
HR1 = SETPOINT       (nastawa z HMI – zmieniana przez Modbus WRITE, PLC jej nie nadpisuje)
"""

logging.basicConfig(level=logging.INFO)


def updating_loop(context: ModbusServerContext) -> None:
    """Symulacja procesu – co 2 sekundy zmienia rejestr 0 (PROCESS_VALUE)."""
    slave_id = 0x00
    fc = 3  # holding registers

    while True:
        # losowa wartość procesu 0–100
        process_value = random.randint(0, 100)

        # czytamy aktualne HR0 i HR1 (PROCESS_VALUE i SETPOINT)
        hr_values = context[slave_id].getValues(fc, 0, count=2)
        # hr_values[0] = stary PROCESS_VALUE
        # hr_values[1] = SETPOINT – tego NIE zmieniamy w PLC

        hr_values[0] = process_value  # aktualizujemy tylko PROCESS_VALUE
        context[slave_id].setValues(fc, 0, hr_values)

        logging.info(
            f"PLC updated: PROCESS_VALUE (HR0) = {process_value}, "
            f"SETPOINT (HR1) = {hr_values[1]}"
        )

        time.sleep(2)


def main() -> None:
    # Tworzymy kontekst z 10 rejestrami HR (0–9) na wszelki wypadek.
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * 10),
        co=ModbusSequentialDataBlock(0, [0] * 10),
        hr=ModbusSequentialDataBlock(0, [0] * 10),
        ir=ModbusSequentialDataBlock(0, [0] * 10),
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Ustawiamy domyślny SETPOINT (HR1) na 50.
    slave_id = 0x00
    fc = 3  # holding registers
    context[slave_id].setValues(fc, 1, [50])

    # Startujemy wątek, który aktualizuje tylko HR0 (PROCESS_VALUE)
    t = threading.Thread(target=updating_loop, args=(context,), daemon=True)
    t.start()

    # Dane identyfikacyjne urządzenia (czysto informacyjne)
    identity = ModbusDeviceIdentification()
    identity.VendorName = "OT Lab"
    identity.ProductCode = "PLC"
    identity.VendorUrl = "https://example.com"
    identity.ProductName = "Demo PLC"
    identity.ModelName = "DemoPLC1"
    identity.MajorMinorRevision = "1.0"

    # Start Modbus TCP server na porcie 502
    StartTcpServer(
        context,
        identity=identity,
        address=("0.0.0.0", 502),
    )


if __name__ == "__main__":
    main()
