
import opcodes


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
    #.. and so on
}

UNKNOWN_ACCESSORY_CATEGORY = 'Unknown'

# returns the list of supported capabilities based on the response
def accessory_capabilities_interpreter(response: str) -> list:
    val = bin(int(response))[2:].zfill(len(accessory_capabilities))
    supports = []
    for i in range(len(accessory_capabilities)):
        if val[i] == '1':
            supports.append(accessory_capabilities[i])
    return supports

# returns the accessory category based on the response
def accessory_category_interpreter(response: str) -> str:
    response = int(response)
    if response in accessory_categories:
        return accessory_categories[response]
    return UNKNOWN_ACCESSORY_CATEGORY

def default_interpreter(response: str) -> str:
    return response

def command_response_handler(response: bytearray) -> str:
    command_opcode = int.from_bytes(response[:2], 'little')
    response_status = int.from_bytes(response[2: 4], 'little')
    # print(command_opcode, response_status)
    return opcodes.opcode_values_to_opcodes[command_opcode] + ': ' + opcodes.response_status_mappings[response_status]

def serial_number_handler(response: bytearray) -> str:
    return response.decode()

callbacks = {
    opcodes.GET_PRODUCT_DATA_RESPONSE : default_interpreter,
    opcodes.GET_MODEL_NAME_RESPONSE : default_interpreter,
    opcodes.GET_MANUFACTURER_NAME_RESPONSE: default_interpreter,
    opcodes.GET_SERIAL_NUMBER_RESPONSE: default_interpreter,
    opcodes.GET_ACCESSORY_CATEGORY_RESPONSE: accessory_category_interpreter,
    opcodes.GET_ACCESSORY_CAPABILITIES_RESPONSE: accessory_capabilities_interpreter,
    opcodes.COMMAND_RESPONSE: command_response_handler
}

accessory_information = {
    opcodes.GET_PRODUCT_DATA_RESPONSE : 'Product Data',
    opcodes.GET_MODEL_NAME_RESPONSE : 'Model Name',
    opcodes.GET_MANUFACTURER_NAME_RESPONSE: 'Manufacturer Name',
    opcodes.GET_ACCESSORY_CATEGORY_RESPONSE: 'Accessory Category',
    opcodes.GET_ACCESSORY_CAPABILITIES_RESPONSE: 'Accessory Capabilities'
}