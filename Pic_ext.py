# pic variable
pic = "bird.jpeg"
size = 29162797 # File size
 
# new files var
f_count =  0 # Incremental 
 
# vars to handle bytes extracted
byte_stream = []
bit_toextract = 2

# extraction vars
SOI = 0xFFD8 # Start Of Image
EOI = 0xFFD9 # End Of Image
SOI_index = []
EOI_index = []

csoi = 0
ceoi = 0

# log file
log = open('log', 'a')
tmp_log = '' 

##################################################

# main func to control embeded jpg extraction logic
def extract():
    global SOI_index, EOI_index, f_count
    # copy pic to stream (each byte encoded to hex)
    stream_cpy()

    # pic extraction logic (for each hex byte)
    for byte in range(len(byte_stream)):  

        # check for SOI/EOI bytes
        chk_bytes(byte)   

    # copy every possible outcome of file by saved (EOI/SOI) indexs
    # copy by bytes from stream[] only if you are in the ranges of EOI/SOI
    for x in range(len(SOI_index)):
        for y in range(len(EOI_index)):
            # extract all new files by current indexes
            f_name = '/home/bruce/Desktop/tmp/pics/' + (str(f_count)) + '.jpg'
            if ((EOI_index[y] > SOI_index[x])):
                new_file(SOI_index[x], EOI_index[y], f_name)
                f_count += 1
                
    return None

# sets the SOI/EOI index variables if found
def chk_bytes(byte):
    global SOI_index, EOI_index, csoi, ceoi

    # if the current 2 bytes = SOI ==> save index of SOI
    if ((byte_stream[byte] == ('ff')) and (byte_stream[byte + 1] == 'd8')):

        # debug
        tmp_log = '\nchk_bytes()\n-------\nSOI byte num : {s}'.format(s = byte)
        log.writelines(tmp_log)

        SOI_index.append(byte)
        csoi += 1

    # if the current 2 bytes = EOI ==> save index of EOI
    elif ((byte_stream[byte] == 'ff') and (byte_stream[byte + 1] == 'd9')):

        # debug
        tmp_log = '\nEOI byte num : {s}\n'.format(s=byte)
        log.writelines(tmp_log)

        EOI_index.append(byte)
        ceoi += 1

# extracts the embeded picture (by indexes) & save in a new file
def new_file(x, y, f_name):
    # x = address of cuurent SOI_index[] index
    # y = address of cuurent EOI_index[] index
    # SOI_index[] / EOI_index[] = value of array index from byte_stream[]
    # byte_stream[] = copy of file encoded by hex
    global byte_stream, f_count
    tmp_stream = []

    # debug
    tmp_log = '\nnew_file()\n---------\nSOI byte num: {s} || EOI byte num: {e}\nfile name: {n}\nfile count: {c}\nx: {x}\ny: {y}\n\n'.format(s=x, e=y ,n=f_name, c=f_count, x=x, y=y)
    log.writelines(tmp_log)

    with open(f_name, 'wb') as file:
        for z in range(len(byte_stream)):
            # everything between the ranges
            if((z >= x) and (z <= y)):
                # copy byte to tmp stream as int (for bytearray())
                tmp_stream.append(int(byte_stream[z], 16))

        # bytearray() retrieves an bytes array (made of int array [tmp_stream])
        file.write(bytearray(tmp_stream))

# append all byte (& encode them to hex) to stream
def stream_cpy():    
    with open(pic, 'rb') as in_f:
        for byte in in_f.read(size):
            byte_stream.append(byte.encode('hex'))

# byte_stream[] hex dump
def print_all(file):
    for i in range (len(byte_stream)):   
        print(byte_stream[i])

##################################################

extract()
log.writelines(("\n\nSOI Bytes count: " + str(csoi)))
log.writelines("EOI Bytes count: " + str(ceoi))
log.writelines("number of pictures extracted: " + str(f_count))
log.writelines('\n\n' + str(SOI_index) + '\n\n' + str(EOI_index))
log.close()
#print_all()
 
