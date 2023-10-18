import asyncio
import logging
import helper
import sys
import opcodes

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

# server bluetooth address
address = "34:E6:AD:A0:6A:58"

UUID = '00000090-0100-0000-0000-000000000000'

def indication_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    opcode = int.from_bytes(data[:2], 'little')
    data = data[2:]
    if opcode in helper.accessory_information:
        data = data.decode()
        value = helper.callbacks[opcode](data)
        try:
            print(f'[INDICATION] {helper.accessory_information[opcode]}: {value}', flush=True)
        except Exception as e:
            print(f"ERROR while interpreting {opcode}: {e}", flush=True)
    elif opcode == opcodes.COMMAND_RESPONSE:
        print('[INDICATION] ', helper.command_response_handler(data), flush=True)
    elif opcode == opcodes.GET_SERIAL_NUMBER_RESPONSE:
        print('[INDICATION] Serial Number: ', helper.serial_number_handler(data), flush=True)

async def main(address):
    async with BleakClient(address, timeout=40) as client:
        print(f"Connected to server {address}")
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
                print("4. Do nothing")
                inp = input("Enter your choice: ")
                try:
                    if inp == "1":
                        opcode_in_bytes = opcodes.SOUND_START.to_bytes(2, 'little')
                        await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                    elif inp == "2":
                        opcode_in_bytes = opcodes.SOUND_STOP.to_bytes(2, 'little')
                        await client.write_gatt_char(UUID, opcode_in_bytes, response=True)   
                    elif inp == "3":
                        opcode_in_bytes = opcodes.GET_SERIAL_NUMBER.to_bytes(2, 'little')
                        await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                    print(flush=True)
                except Exception as e:
                    print("Error while executing operation: ", e)
        except KeyboardInterrupt:
            print("Exiting program")
            await client.disconnect()
asyncio.run(main(address))