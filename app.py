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
indication = ['']

from threading import Thread, Lock

mutex = Lock()

def indication_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """
    Method to handle indications from the accessory
    Different handlers are invoked for the below kinds of indications
    1. Accessory information
    2. Command Response (during sound start, stop operations)
    3. Get Serial Number Response
    """
    # indication[0] = ''
    value = ''
    opcode = int.from_bytes(data[:2], 'big')
    data = data[2:]
    if opcode in helper.accessory_information:
        data = data.decode()
        # value = helper.callbacks[opcode](data)

        try:
            value += f'[INDICATION] {helper.accessory_information[opcode]}: {helper.callbacks[opcode](data)}<br><br>'
        except Exception as e:
            value += f"ERROR while interpreting {opcode}: {e}<br><br>"
    elif opcode == opcodes.COMMAND_RESPONSE:
        value += '[INDICATION] '+ helper.command_response_handler(data) + '<br><br>'
    elif opcode == opcodes.GET_SERIAL_NUMBER_RESPONSE:
        value += 'Serial Number Lookup URL (open in browser): '+helper.serial_number_handler(data) + '<br><br>'
    print(value)
    with mutex:
        indication[0] += value

def callback(device, advertisement_data):
    if device not in devices:
        devices[device] = advertisement_data

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
devices = {}
addresses = ['']

@app.route('/')
def index():
    return render_template('index.ejs')

@app.route('/start', methods=['POST'])
async def start():
    addresses = ['']
    devices.clear()
    scanner = BleakScanner(callback)
    data = ''
    await scanner.start()
    await asyncio.sleep(15)
    await scanner.stop()
    devices_list = list(devices)
    for i, device in enumerate(devices_list):
        data += f"{i + 1}. {device}<br><br>"
    return jsonify({'data': data})

@app.route('/search', methods=['POST'])
async def search():
    choice = request.form.get('number')
    devices_list = list(devices)
    try:
        choice_idx = int(choice)
        if choice_idx >= 1 and choice_idx <= len(devices_list):
            address = devices_list[choice_idx - 1].address
    except Exception:
        address = ''
    addresses[0] = address
    data = ''
    data += f"Connecting to {address}...<br><br>"
    try:
        async with BleakClient(address, timeout=40) as client:
            data += f"Connected to device {address}<br><br>"
            await client.start_notify(UUID, indication_handler)
            await asyncio.sleep(3)
            try:
                data += "Fetching accessory information..<br><br>"
                for opcode in [opcodes.GET_PRODUCT_DATA, opcodes.GET_MANUFACTURER_NAME, opcodes.GET_MODEL_NAME, opcodes.GET_ACCESSORY_CATEGORY, opcodes.GET_ACCESSORY_CAPABILITIES]:
                    opcode_in_bytes = opcode.to_bytes(2, 'big')
                    await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
            except KeyboardInterrupt:
                data += "Disconnecting and exiting program<br><br>"
                await client.disconnect()
            await asyncio.sleep(15)
            data += indication[0]
            indication[0] = ''
    except Exception as e:
        data += f"ERROR: Could not connect to {address}, {e}<br><br>"
    return jsonify({'data': data})

@app.route('/button_click', methods=['POST'])
async def button_click():
    button_id = request.form.get('button_id')
    data = ''
    if button_id == "button4":
        return jsonify({'data': ''})
    try:
        async with BleakClient(addresses[0], timeout=40) as client:
            data += f"Connected to device {addresses[0]}<br><br>"
            await client.start_notify(UUID, indication_handler)
            await asyncio.sleep(3)
            try:
                if button_id == "button1":
                    opcode_in_bytes = opcodes.SOUND_START.to_bytes(
                        2, 'big')
                    await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                elif button_id == "button2":
                    opcode_in_bytes = opcodes.SOUND_STOP.to_bytes(
                        2, 'big')
                    await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                elif button_id == "button3":
                    opcode_in_bytes = opcodes.GET_SERIAL_NUMBER.to_bytes(
                        2, 'big')
                    await client.write_gatt_char(UUID, opcode_in_bytes, response=True)
                await asyncio.sleep(5)
                print("Indication", indication[0])
                data += indication[0]
                indication[0] = ''
                print(flush=True)
            except Exception as e:
                data += "\nError while executing operation: "+e+'<br><br>'
    except Exception as e:
        data += f"\nERROR: Could not connect to address, {e}"
        # return jsonify({'data': data})
    
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)
