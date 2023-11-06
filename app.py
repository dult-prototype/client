import asyncio
import helper
import opcodes

import bleak
from bleak import BleakClient, BleakScanner, BleakError
from bleak.backends.characteristic import BleakGATTCharacteristic

"""
This program runs a bluetooth client intended to be the DULT 
application with the following capabilities
- Fetch the accessory (tracker) information
- Play and stop sound on the accessory
- Get serial number of the accessory
"""

# UUID of the non owner accessory service (TODO)
UUID = '00000090-0100-0000-0000-000000000000'


def indication_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """
    Method to handle indications from the accessory
    Different handlers are invoked for the below kinds of indications
    1. Accessory information
    2. Command Response (during sound start, stop operations)
    3. Get Serial Number Response
    """

    opcode = int.from_bytes(data[:2], 'little')
    data = data[2:]
    if opcode in helper.accessory_information:
        data = data.decode()
        value = helper.callbacks[opcode](data)
        try:
            print(
                f'[INDICATION] {helper.accessory_information[opcode]}: {value}', flush=True)
        except Exception as e:
            print(f"ERROR while interpreting {opcode}: {e}", flush=True)
    elif opcode == opcodes.COMMAND_RESPONSE:
        print('[INDICATION] ', helper.command_response_handler(data), flush=True)
    elif opcode == opcodes.GET_SERIAL_NUMBER_RESPONSE:
        print('Serial Number Lookup URL (open in browser): ',
              helper.serial_number_handler(data), flush=True)


devices = {}
devices_list = []


def callback(device, advertisement_data):
    if device not in devices:
        devices[device] = advertisement_data


async def main():
    """
    Main method
    - Scans for bluetooth devices
    - Connects to the specified accessory
    """
    while True:
        devices.clear()
        scanner = BleakScanner(callback)
        print("Scanning for devices...")
        await scanner.start()
        await asyncio.sleep(15)
        await scanner.stop()
        devices_list = list(devices)

        for i, device in enumerate(devices_list):
            print(f"{i + 1}. {device}")

        address = ""
        while True:
            print("\nEnter the index of device to connect to (0 to rescan): ")
            choice = input()
            try:
                choice_idx = int(choice)
                if choice_idx >= 1 and choice_idx <= len(devices_list):
                    address = devices_list[choice_idx - 1].address
                    break
                elif choice_idx == 0:
                    break
                else:
                    print("Please enter a valid index")
            except Exception:
                print("Please enter a valid index")
        if address != "":
            break
    while True:
        print(f"Connecting to {address}...")
        try:
            async with BleakClient(address, timeout=40) as client:
                print(f"Connected to device {address}")
                await client.start_notify(UUID, indication_handler)
                await asyncio.sleep(3)
                try:
                    print("Fetching accessory information..")
                    for opcode in [opcodes.GET_PRODUCT_DATA, opcodes.GET_MANUFACTURER_NAME, opcodes.GET_MODEL_NAME, opcodes.GET_ACCESSORY_CATEGORY, opcodes.GET_ACCESSORY_CAPABILITIES]:
                        opcode_in_bytes = opcode.to_bytes(2, 'little')
                        await client.write_gatt_char(UUID, opcode_in_bytes, response=True)

                    while True:
                        print("1. Sound Start")
                        print("2. Sound Stop")
                        print("3. Serial Number Lookup over BLE")
                        print("4. Exit")
                        inp = input("Enter your choice: ")
                        try:
                            if inp == "1":
                                opcode_in_bytes = opcodes.SOUND_START.to_bytes(
                                    2, 'little')
                                await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                            elif inp == "2":
                                opcode_in_bytes = opcodes.SOUND_STOP.to_bytes(
                                    2, 'little')
                                await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                            elif inp == "3":
                                opcode_in_bytes = opcodes.GET_SERIAL_NUMBER.to_bytes(
                                    2, 'little')
                                await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                            elif inp == "4":
                                raise KeyboardInterrupt
                            print(flush=True)
                        except Exception as e:
                            print("Error while executing operation: ", e)
                except KeyboardInterrupt:
                    print("Disconnecting and exiting program")
                    await client.disconnect()
                    exit(0)
        except Exception as e:
            print(f"ERROR: Could not connect to {address}, {e}")
            print(f"Do you want to retry connecting to {address} (y/n)?")
            choice = input()
            if choice != "y":
                break

asyncio.run(main())
