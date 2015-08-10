import zlib

MAGIC_FIRSTBYTE = 222
MAGIC_SECONDBYTE = 173

ENCODE_NONE = 0
ENCODE_DEFLATE = 1

def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
            compresslevel,
            zlib.DEFLATED
    )
    deflated = compress.compress(str(data))
    deflated += compress.flush()
    return bytearray(deflated)

DEFAULT_CHUNK_SIZE = 1024

def encode(data, mode="AUTO", messageId=0):
    if mode=="NONE":
        return [encode_NONE(data, messageId=messageId)]
    if mode=="DEFLATE":
        return [encode_DEFLATE(data, messageId=messageId)]

    dataArray = []

    left = 0
    right = min(DEFAULT_CHUNK_SIZE,len(data))
    while left<right:
        dataArray.append(data[left:right])
        left+=DEFAULT_CHUNK_SIZE;
        right=min(left+DEFAULT_CHUNK_SIZE,len(data));

    packetCount = len(dataArray)
    for i in range(0,packetCount):
        dataArray[i] = bytearray(encode_DEFLATE(bytearray(dataArray[i]), messageId=messageId, packetCount = packetCount, packetId=i+1))

    return dataArray

def encode_header(messageId, packetCount, packetId, encodeMode):
	return bytearray([MAGIC_FIRSTBYTE, MAGIC_SECONDBYTE, messageId, packetCount, packetId, encodeMode])

def encode_DEFLATE(data, messageId=0, packetCount=1, packetId=1):
	dataSize = len(data)
	headerDeflate = bytearray([ (dataSize>>8)&0xFF, dataSize&0xFF])
	return bytearray(encode_header(messageId,packetCount,packetId,ENCODE_DEFLATE)+headerDeflate+deflate(data))

def encode_NONE(data, messageId=0, packetCount=1, packetId=1):
	return bytearray(encode_header(messageId,packetCount,packetId,ENCODE_NONE)+data)
