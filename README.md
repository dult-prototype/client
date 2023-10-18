## Client for DULT

This is a CLI simulation of the DULT application which interacts with the unwanted tracker (server)

### Install

```pip install bleak```

### Run

1. Run the server code present in https://github.com/dult-prototype/server (on a Ubuntu server).
2. Run the client code on a separate windows or Ubuntu device using the command ```python3 app.py```

### Functionality

![WhatsApp Image 2023-10-18 at 19 40 23](https://github.com/dult-prototype/client/assets/78913321/cd0940f9-489f-4c1d-bb88-e0b571d767aa)
1. The program initially request the server for the Prouct Data, Manufacturer Name, Model Name, Accessory Category and Accessory Capability.
2. These details requested are returned back to the client in the form of the indications.
3. The program provides 4 operations or types request - Start Sound, Stop Sound, Serial Number Lookup, and do nothing.
4. By clicking on the desired operations, he/she can perform those operations on the server device.
