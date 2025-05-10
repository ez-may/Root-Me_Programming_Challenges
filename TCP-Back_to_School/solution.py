import math
import socket
import sys
import time

#Challenge Variables
port = 52002
ip = socket.gethostbyname("challenge01.root-me.org")

try:
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

#receive the first message from the server and display it
msg = sock.recv(1024)
msg = msg.decode()
print(msg)

#parse the message to get the numbers
line = msg.split('\n')[-1].split(' ')
num1 = int(line[5])
num2 = int(line[9])

#calculate the result
result = round(math.sqrt(num1)*float(num2), 2)
result = str(result) + "\n"
print(f"Result of the sqrt of {num1} multiplied by {num2}: {result}")

#reply to the server with the result
sock.send(result.encode())

#end timer for server response and display it
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

#receive the final message from the server and display it
msg = sock.recv(1024)
msg = msg.decode()
print(msg)