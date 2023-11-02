"""
Contains all opcodes and response codes mentioned in the draft
"""

GET_PRODUCT_DATA = 0x306
GET_MANUFACTURER_NAME = 0x307
GET_MODEL_NAME = 0x308
GET_ACCESSORY_CATEGORY = 0x309
GET_ACCESSORY_CAPABILITIES = 0x30A
GET_SERIAL_NUMBER = 0x404

SOUND_START = 0x300
SOUND_STOP = 0x301
SOUND_COMPLETED = 0x303

GET_PRODUCT_DATA_RESPONSE = 0x311
GET_MANUFACTURER_NAME_RESPONSE = 0x312
GET_MODEL_NAME_RESPONSE = 0x313
GET_ACCESSORY_CATEGORY_RESPONSE = 0x314
GET_ACCESSORY_CAPABILITIES_RESPONSE = 0x315
GET_SERIAL_NUMBER_RESPONSE = 0x405
COMMAND_RESPONSE = 0x302

opcode_values_to_opcodes = {
    SOUND_START: 'Sound start',
    SOUND_STOP: 'Sound stop',
    SOUND_COMPLETED: 'Sound completed'
}

response_status_mappings = {
    0x0: 'Success',
    0x0001: 'Invalid State',
    0x0002: 'Invalid Configuration',
    0x0003: 'Invalid length',
    0x0004: 'Invalid param',
    0xFFFF: 'Invalid command',
}
