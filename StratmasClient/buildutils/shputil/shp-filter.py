#!/bin/python

import array
import struct
import sys

defaultbyteorder="little"

def putInt(f, v, byteorder=defaultbyteorder):
    if byteorder == "little":
        fmt = "<i"
    elif byteorder == "big":
        fmt = ">i"
    else:
        raise Exception("bad endian")
    return f.write(struct.pack(fmt, v))

def putInts(f, vs, byteorder=defaultbyteorder):
    if byteorder == "little":
        fmt = "<i"
    elif byteorder == "big":
        fmt = ">i"
    else:
        raise Exception("bad endian")
    for v in vs:
        f.write(struct.pack(fmt, v))
        

def putDoubles(f, vs, byteorder=defaultbyteorder):
    if byteorder == "little":
        fmt = "<d"
    elif byteorder == "big":
        fmt = ">d"
    else:
        raise Exception("bad endian")
    for v in vs:
        f.write(struct.pack(fmt, v))

def getInt(f, byteorder=defaultbyteorder, signed=True):
    return int.from_bytes(f.read(4), byteorder=byteorder, signed=signed)

def getInts(f, no, byteorder=defaultbyteorder):
    ar = array.array('i', f.read(no*4))
    if byteorder != sys.byteorder:
        ar.byteswap()
    return ar.tolist()

def getDoubles(f, no, byteorder=defaultbyteorder):
    ar = array.array('d', f.read(no*8))
    if byteorder != sys.byteorder:
        ar.byteswap()
    return ar.tolist()

def getNull(f, rlen):
    return None

def getPoint(f, rlen):
    return tuple(getDoubles(f, 2))

def getMultiPoint(f, rlen):
    box = getDoubles(f, 4)
    numPoints = getInt(f)
    points = []
    for i in range(0,numPoints):
        p = getPoint(f, 2*8)
        points.append(p)
    return (box, numPoints, points)

def getPolyline(f, rlen):
    box = getDoubles(f, 4)
    numParts = getInt(f)
    numPoints = getInt(f)
    parts = getInts(f, numParts)
    points = []
    for i in range(0,numPoints):
        p = getPoint(f,  2*8)
        points.append(p)
    return (box, numParts, numPoints, parts, points)

def getPolygon(f, rlen):
    box = getDoubles(f, 4)
    numParts = getInt(f)
    numPoints = getInt(f)
    parts = getInts(f, numParts)
    points = []
    for i in range(0,numPoints):
        p = getPoint(f,  2*8)
        points.append(p)
    return (box, numParts, numPoints, parts, points)

def getPointZ(f, rlen):
    return tuple(getDoubles(f, 4))

def getPolygonZ(f, rlen):
    box = getDoubles(f, 4)
    numParts = getInt(f)
    numPoints = getInt(f)
    parts = getInts(f, numParts)
    points = []
    for i in range(0,numPoints):
        p = getPoint(f,  2*8)
        points.append(p)
    zrange = getDoubles(f, 2)
    zarray = getDoubles(f, numPoints)
    mrange = getDoubles(f, 2)
    marray = getDoubles(f, numPoints)
    return (box, numParts, numPoints, parts, points, zrange, zarray, mrange, marray)

#def getPolylineZ(f, rlen):
#def getMultiPointZ(f, rlen):
#def getPointM(f, rlen):
#def getPolylineM(f, rlen):
#def getPolygonM(f, rlen):
#def getMultiPointM(f, rlen):
#def getMultiPatch(f, rlen):

rtypes_gets = {
        0 : getNull,
        1 : getPoint,
        3 : getPolyline,
        5 : getPolygon,
        8 : getMultiPoint,
        11: getPointZ,
        #13: getPolylineZ,
        15: getPolygonZ,
        #18: getMultiPointZ,
        #21: getPointM,
        #23: getPolylineM,
        #25: getPolygonM,
        #28: getMultiPointM,
        #31: getMultiPatch
}

def getType(f, rtype, rlen):
    return rtypes_gets[rtype](f, rlen)

def putPoint(f, rdata):
    putDoubles(f, list(rdata))

def putPolygon(f, rdata):
    box = rdata[0]
    numParts = rdata[1]
    numPoints = rdata[2]
    parts = rdata[3]
    points = rdata[4]

    putDoubles(f, box)
    putInt(f, numParts)
    putInt(f, numPoints)
    putInts(f, parts)
    for p in points:
        putPoint(f, p)

rtypes_puts = {
        #0 : putNull,
        1 : putPoint,
        #3 : putPolyline,
        5 : putPolygon,
        #8 : putMultiPoint,
        #11: putPointZ,
        #13: putPolylineZ,
        #15: putPolygonZ,
        #18: putMultiPointZ,
        #21: putPointM,
        #23: putPolylineM,
        #25: putPolygonM,
        #28: putMultiPointM,
        #31: putMultiPatch
}


def putType(f, rtype, rdata):
    rtypes_puts[rtype](f, rdata)

def filterShpFile(infile, outfile):
    with open(outfile, "wb") as o:
        with open(infile, "rb") as f:
            fcode = getInt(f, byteorder="big")
            funused = getInts(f, 5, byteorder="big")
            flen = getInt(f, byteorder="big")
            fver = getInt(f, byteorder="little")
            fshptype = getInt(f, byteorder="little")
            print("fcode =", fcode)
            print("funused =", funused)
            print("flen =", flen)
            print("fver =", fver)
            print("fshptype =", fshptype)

            putInt(o, fcode, byteorder="big")
            putInts(o, funused, byteorder="big")
            putInt(o, flen, byteorder="big")
            putInt(o, fver, byteorder="little")
            putInt(o, fshptype, byteorder="little")

            fmbr = getDoubles(f, 4)
            fZr = getDoubles(f, 2)
            fMr = getDoubles(f, 2);
            print("fmbr =", fmbr)
            print("fZr =", fZr)
            print("fMr =", fMr)

            putDoubles(o, fmbr)
            putDoubles(o, fZr)
            putDoubles(o, fMr)

            hlen = 100
            flen = flen * 2 # 16-bit words to 8-bit words
            flen = flen - hlen

            while flen > 0:
                print() # separator

                rno = getInt(f, byteorder="big")
                rlen = getInt(f, byteorder="big")
                print("rno =", rno)
                print("rlen =", rlen)

                rtype = getInt(f, byteorder="little")
                print("rtype =", rtype)

                if rtype not in rtypes_gets:
                    print("unimplemented type ==> dying")
                    sys.exit(1)

                rdata = getType(f, rtype, rlen)
                print("rdata =", rdata)

                if rtype == 15: # PolygonZ
                    rtype = 5 # Polygon  (no Z)
                    rdata = tuple(rdata[0:5])
                putInt(o, rno, byteorder="big")
                putInt(o, rlen, byteorder="big")
                putInt(o, rtype, byteorder="little")
                putType(o, rtype, rdata)

                flen = flen - 2*(2*2 + rlen)

filterShpFile(sys.argv[1], sys.argv[2])
