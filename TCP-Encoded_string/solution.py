import base64
import chardet
import re
import socket
import sys
import time

#Challenge Variables
port = 52023
ip = socket.gethostbyname("challenge01.root-me.org")

try:
    # connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
except socket.gaierror as err:
    # could not resolve the host
    print(f"There was an error resolving the host: {err}")
    sys.exit()
except socket.error as err:
    # could not connect to the server
    print(f"There was an error connecting to the server: {err}")
    sys.exit()

#start timer for server response to ensure program runs in under 2 seconds
start = time.time()

#receive the first message from the server
msg = sock.recv(1024)
possible_ecodings = chardet.detect_all(msg)
print(f"Possible encodings: {possible_ecodings}")

for encoding in possible_ecodings:
    try:
        # decode the message using the detected encoding
        decoded_msg = msg.decode(encoding['encoding'])
        print(f"Decoded message: {decoded_msg}")
        
        # use regex to extract the encrypyted string
        regex_pattern = re.compile("'[a-zA-Z0-9+/=]+'")
        encoded_str = regex_pattern.search(decoded_msg).group()
        encoded_str = encoded_str[1:-1]  # remove the quotes
        
        # attempt to decode the string using base64 encoding
        base64_bytes = encoded_str.encode(encoding['encoding'])
        string_bytes = base64.b64decode(base64_bytes)
        message = string_bytes.decode(encoding['encoding'])
        print(f"Decoded message: {message}")
        
        # send the decoded message back to the server
        sock.send((message + "\n").encode(encoding['encoding']))
        #end timer for server response and display it
        end = time.time()
        print(f"Time taken: {end - start:.2f} seconds")

        #receive the message from the server and display it
        response = sock.recv(1024)
        response = response.decode()
        print(response)

        success_pattern = re.compile("Good job")
        if success_pattern.search(response) != None:
            break
        else:
            print("Failed to decode the message correctly. Continuing to next encoding if possible.")
            continue
    except err:
        print(f"Error decoding message: {err}\nContinuing to next encoding if possible.")
        continue