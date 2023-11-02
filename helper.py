
import opcodes
import http.client

# URL and port number of the serial number decryption server
SERVER_URL = "localhost"
PORT = 8080

accessory_capabilities = [
    'Play Sound',
    'Motion detector UT',
    'Serial Number lookup by NFC',
    'Serial Number lookup by BLE'
]

accessory_categories = {
    1: 'Finder',
    129: 'Luggage',
    130: 'Backpack',
    # .. and so on
}

UNKNOWN_ACCESSORY_CATEGORY = 'Unknown'

# Mapping from opcode to the corresponding accessory information
accessory_information = {
    opcodes.GET_PRODUCT_DATA_RESPONSE: 'Product Data',
    opcodes.GET_MODEL_NAME_RESPONSE: 'Model Name',
    opcodes.GET_MANUFACTURER_NAME_RESPONSE: 'Manufacturer Name',
    opcodes.GET_ACCESSORY_CATEGORY_RESPONSE: 'Accessory Category',
    opcodes.GET_ACCESSORY_CAPABILITIES_RESPONSE: 'Accessory Capabilities'
}

"""
The followind methods are the handlers for indications mentioned in app.py
Parameter: Response (as string) from the accessory
"""


def accessory_capabilities_handler(response: str) -> list:
    """
    Returns the list of supported capabilities based on the response
    """
    val = bin(int(response))[2:].zfill(len(accessory_capabilities))
    supports = []
    for i in range(len(accessory_capabilities)):
        if val[i] == '1':
            supports.append(accessory_capabilities[i])
    return supports


def accessory_category_handler(response: str) -> str:
    """
    Returns the accessory category based on the response
    """
    response = int(response)
    if response in accessory_categories:
        return accessory_categories[response]
    return UNKNOWN_ACCESSORY_CATEGORY


def default_handler(response: str) -> str:
    """
    Returns the response as it is
    """
    return response


def command_response_handler(response: bytearray) -> str:
    """
    Returns the command which invoked this response and the response status
    In the format "Command: Response Status"
    """
    command_opcode = int.from_bytes(response[:2], 'little')
    response_status = int.from_bytes(response[2: 4], 'little')
    # print(command_opcode, response_status)
    return opcodes.opcode_values_to_opcodes[command_opcode] + ': ' + opcodes.response_status_mappings[response_status]


def serial_number_handler(response: bytearray) -> str:
    """
    Queries the decryption server with the serial number fetched
    from the accessory for decryption
    Prints the decrypted serial number
    """
    encrypted_serial_number = response.decode()

    conn = http.client.HTTPConnection(SERVER_URL, PORT)
    path = f"/decrypt?serial_number={encrypted_serial_number}"
    conn.request("GET", path)

    response = conn.getresponse()
    if response.status == 200:
        decrypted_serial_number = response.read().decode()
        print(f"Decrypted Serial Number: {decrypted_serial_number}")
        return decrypted_serial_number
    else:
        return f"Error: {response.status} - {response.reason}"

# Callback methods for different opcodes
callbacks = {
    opcodes.GET_PRODUCT_DATA_RESPONSE: default_handler,
    opcodes.GET_MODEL_NAME_RESPONSE: default_handler,
    opcodes.GET_MANUFACTURER_NAME_RESPONSE: default_handler,
    opcodes.GET_SERIAL_NUMBER_RESPONSE: default_handler,
    opcodes.GET_ACCESSORY_CATEGORY_RESPONSE: accessory_category_handler,
    opcodes.GET_ACCESSORY_CAPABILITIES_RESPONSE: accessory_capabilities_handler,
    opcodes.COMMAND_RESPONSE: command_response_handler
}
