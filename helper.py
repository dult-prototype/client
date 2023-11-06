
import opcodes
import http.client

# URL and port number of the tracking network server
# TODO - Determine the url from the accessory itself instead
# of a hard coded value
SERVER_URL = "http://localhost"
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
    command_opcode = int.from_bytes(response[:2], 'big')
    response_status = int.from_bytes(response[2: 4], 'big')
    return opcodes.opcode_values_to_opcodes[command_opcode] + ': ' + opcodes.response_status_mappings[response_status]


def serial_number_handler(response: bytearray) -> str:
    """
    Returns the URL of server for decrypting the serial number
    and fetching owner information
    """
    encrypted_serial_number = response.decode()
    url = f"{SERVER_URL}:{PORT}/serial-number-decrypt?serial-number={encrypted_serial_number}"
    return url


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
