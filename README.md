## Client for DULT

This is a CLI simulation of the DULT application which interacts with the unwanted tracker (server)

### Install

```pip install bleak```

### Run

1. Run the server code present in https://github.com/dult-prototype/server (on a Ubuntu server).
2. Run the client code on a separate windows or Ubuntu device using the command ```python3 app.py```

### Functionality

![WhatsApp Image 2023-10-18 at 19 40 23](https://github.com/dult-prototype/client/assets/78913321/cd0940f9-489f-4c1d-bb88-e0b571d767aa)
1. The app scans for nearby bluetooth devices and displays a list. The user can connect to any device. (We assume the device connected to is an unwanted tracker and implements the GATT operations specified in the draft, otherwise the app simply returns an error).
2. The app initially requests from the accessory (server) its Prouct Data, Manufacturer Name, Model Name, Accessory Category and Accessory Capability.
3. These details requested are returned in the form of the indications and are displayed appropriately.
4. Then, the app provides 3 choices
    - Start sound - Starts playing sound on the accessory
    - Stop sound - Stops playing sound on the accessory
    - Get Serial Number - Fetches the serial number of the accessory (assumed to be encrypted) and displays the tracker network server URL for the decryption (to be opened in a browser).

### Note
1. The results of operations (such as a success for sound start) might not be displayed immediately due to python not flushing the output.
2. Another machine must be used to run the server.

### Yet to be implemented
1. The application should read the near owner bit from the accessory advertisement and ignore if it is in the near-owner state. Since there have been issues in implementing the near-owner bit, this is not implemented.
2. The URL of the tracker network server is hard-coded for demonstration. This will be implemented once we are clear about how it is to be fetched (one of the questions asked by us about the draft). One possible way could be to fetch it from the product data registry given the product data of the accessory.

### Improvements
1. Making a mobile app for the same would be more suitable


