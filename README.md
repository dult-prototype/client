## Client for DULT

This is a CLI simulation of the DULT application which interacts with the unwanted tracker (server)

### Install

```pip install bleak```

### Run

1. Run the server code present in https://github.com/dult-prototype/server (on a Ubuntu server).
2. Run the client code on a separate windows or Ubuntu device using the command ```python3 app.py```

### Functionality

![WhatsApp Image 2023-10-18 at 19 40 23](https://github.com/dult-prototype/client/assets/78913321/cd0940f9-489f-4c1d-bb88-e0b571d767aa)
1. The program initially requests from the accessory (server) its Prouct Data, Manufacturer Name, Model Name, Accessory Category and Accessory Capability.
2. These details requested are returned in the form of the indications and are displayed appropriately.
3. Then, the program provides 3 choices
    - Start sound - Starts playing sound on the accessory
    - Stop sound - Stops playing sound on the accessory
    - Get Serial Number - Fetches the serial number of the accessory
        (assumed to be encrypted) and decrypts it by calling the decryption server

### Note
1. The results of operations (such as a success for sound start) might not be displayed immediately due to python not flushing the output.
2. Another machine must be used to run the server.

### Improvements
1. Making a mobile app for the application would be more suitable


