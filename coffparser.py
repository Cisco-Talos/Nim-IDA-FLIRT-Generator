###############################################################################################################################
#                                                                                                                             #
# COFF Parser to generate IDA signature pattern (.pat) files                                                                  #
#                                                                                                                             #
# Author: Holger Unterbrink (hunterbr@cisco.com)                                                                              #
#                                                                                                                             #
# Usage: python coffparser.py <OBJECT_FILENAME_TO_PARSE> <OUTPUT_SIGNATURE_FILENAME>                                          #
#                                                                                                                             #
# IMPORTANT:                                                                                                                  #
# This script assumes the object file is compiled with MinGW with --ffunction-sections parameter !!!                          #
#                                                                                                                             #
#                                                                                                                             #
# Copyright 2022 Cisco Systems, Inc. and its affiliates                                                                       #
#                                                                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License");                                                             #
# you may not use this file except in compliance with the License.                                                            #
# You may obtain a copy of the License at                                                                                     #
#                                                                                                                             #
#      http://www.apache.org/licenses/LICENSE-2.0                                                                             #
#                                                                                                                             #
# Unless required by applicable law or agreed to in writing, software                                                         #
# distributed under the License is distributed on an "AS IS" BASIS,                                                           #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                                    #
# See the License for the specific language governing permissions and                                                         #
# limitations under the License.                                                                                              #
#                                                                                                                             #
# SPDX-License-Identifier: Apache-2.0                                                                                         #
#                                                                                                                             #
###############################################################################################################################

import sys
import struct
import re
from pprint import pprint

SymbolTableStart  = 0
NumberOfSymbols   = 0
AuxiliaryCount    = '0x0'

# Main dictionary to store section infos in
sections = {}

# IMAGE_FILE_HEADER Characteristics
CharacteristicsList = ["IMAGE_FILE_RELOCS_STRIPPED",
                       "IMAGE_FILE_EXECUTABLE_IMAGE",
                       "IMAGE_FILE_LINE_NUMS_STRIPPED",
                       "IMAGE_FILE_LOCAL_SYMS_STRIPPED",
                       "IMAGE_FILE_AGGRESSIVE_WS_TRIM",
                       "IMAGE_FILE_LARGE_ADDRESS_ AWARE",
                       "IMAGE_FILE_UNKNOWN",
                       "IMAGE_FILE_BYTES_REVERSED_LO",
                       "IMAGE_FILE_32BIT_MACHINE",
                       "IMAGE_FILE_DEBUG_STRIPPED",
                       "IMAGE_FILE_REMOVABLE_RUN_FROM_SWAP",
                       "IMAGE_FILE_NET_RUN_FROM_SWAP",
                       "IMAGE_FILE_SYSTEM",
                       "IMAGE_FILE_DLL",
                       "IMAGE_FILE_UP_SYSTEM_ONLY",
                       "IMAGE_FILE_BYTES_REVERSED_HI"]

# ported from IDB2SIG plugin updated by TQN
# https://github.com/mandiant/flare-ida
CRC16_TABLE = [
  0x0, 0x1189, 0x2312, 0x329b, 0x4624, 0x57ad, 0x6536, 0x74bf, 0x8c48, 0x9dc1,
  0xaf5a, 0xbed3, 0xca6c, 0xdbe5, 0xe97e, 0xf8f7, 0x1081, 0x108, 0x3393, 0x221a,
  0x56a5, 0x472c, 0x75b7, 0x643e, 0x9cc9, 0x8d40, 0xbfdb, 0xae52, 0xdaed, 0xcb64,
  0xf9ff, 0xe876, 0x2102, 0x308b, 0x210, 0x1399, 0x6726, 0x76af, 0x4434, 0x55bd,
  0xad4a, 0xbcc3, 0x8e58, 0x9fd1, 0xeb6e, 0xfae7, 0xc87c, 0xd9f5, 0x3183, 0x200a,
  0x1291, 0x318, 0x77a7, 0x662e, 0x54b5, 0x453c, 0xbdcb, 0xac42, 0x9ed9, 0x8f50,
  0xfbef, 0xea66, 0xd8fd, 0xc974, 0x4204, 0x538d, 0x6116, 0x709f, 0x420, 0x15a9,
  0x2732, 0x36bb, 0xce4c, 0xdfc5, 0xed5e, 0xfcd7, 0x8868, 0x99e1, 0xab7a, 0xbaf3,
  0x5285, 0x430c, 0x7197, 0x601e, 0x14a1, 0x528, 0x37b3, 0x263a, 0xdecd, 0xcf44,
  0xfddf, 0xec56, 0x98e9, 0x8960, 0xbbfb, 0xaa72, 0x6306, 0x728f, 0x4014, 0x519d,
  0x2522, 0x34ab, 0x630, 0x17b9, 0xef4e, 0xfec7, 0xcc5c, 0xddd5, 0xa96a, 0xb8e3,
  0x8a78, 0x9bf1, 0x7387, 0x620e, 0x5095, 0x411c, 0x35a3, 0x242a, 0x16b1, 0x738,
  0xffcf, 0xee46, 0xdcdd, 0xcd54, 0xb9eb, 0xa862, 0x9af9, 0x8b70, 0x8408, 0x9581,
  0xa71a, 0xb693, 0xc22c, 0xd3a5, 0xe13e, 0xf0b7, 0x840, 0x19c9, 0x2b52, 0x3adb,
  0x4e64, 0x5fed, 0x6d76, 0x7cff, 0x9489, 0x8500, 0xb79b, 0xa612, 0xd2ad, 0xc324,
  0xf1bf, 0xe036, 0x18c1, 0x948, 0x3bd3, 0x2a5a, 0x5ee5, 0x4f6c, 0x7df7, 0x6c7e,
  0xa50a, 0xb483, 0x8618, 0x9791, 0xe32e, 0xf2a7, 0xc03c, 0xd1b5, 0x2942, 0x38cb,
  0xa50, 0x1bd9, 0x6f66, 0x7eef, 0x4c74, 0x5dfd, 0xb58b, 0xa402, 0x9699, 0x8710,
  0xf3af, 0xe226, 0xd0bd, 0xc134, 0x39c3, 0x284a, 0x1ad1, 0xb58, 0x7fe7, 0x6e6e,
  0x5cf5, 0x4d7c, 0xc60c, 0xd785, 0xe51e, 0xf497, 0x8028, 0x91a1, 0xa33a, 0xb2b3,
  0x4a44, 0x5bcd, 0x6956, 0x78df, 0xc60, 0x1de9, 0x2f72, 0x3efb, 0xd68d, 0xc704,
  0xf59f, 0xe416, 0x90a9, 0x8120, 0xb3bb, 0xa232, 0x5ac5, 0x4b4c, 0x79d7, 0x685e,
  0x1ce1, 0xd68, 0x3ff3, 0x2e7a, 0xe70e, 0xf687, 0xc41c, 0xd595, 0xa12a, 0xb0a3,
  0x8238, 0x93b1, 0x6b46, 0x7acf, 0x4854, 0x59dd, 0x2d62, 0x3ceb, 0xe70, 0x1ff9,
  0xf78f, 0xe606, 0xd49d, 0xc514, 0xb1ab, 0xa022, 0x92b9, 0x8330, 0x7bc7, 0x6a4e,
  0x58d5, 0x495c, 0x3de3, 0x2c6a, 0x1ef1, 0xf78]


# ported from IDB2SIG plugin updated by TQN
# https://github.com/mandiant/flare-ida
def crc16(data, crc):
    for byte in data:
        crc = (crc >> 8) ^ CRC16_TABLE[(crc ^ ord(byte)) & 0xFF]
    crc = (~crc) & 0xFFFF
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xffff


def GetCharacteristics(Characteristics):
    IntX = int(Characteristics,16)
    CharStr = ""
    for i in range(0,32):
        X = (IntX >> i) & 0x1
        if X != 0:
            CharStr += CharacteristicsList[i]
            CharStr += "|"
    return CharStr.rstrip("|")

def GetMachineType(Machine):
    if int(Machine,16) == 0x014c:
        return "IMAGE_FILE_MACHINE_I386"
    elif int(Machine,16) == 0x0200:
        return "IMAGE_FILE_MACHINE_IA64"
    elif int(Machine,16) == 0x8664:
        return "IMAGE_FILE_MACHINE_AMD64"
    else:
        return False

def print_fileheader(FileHeader):
    global SymbolTableStart
    global NumberOfSymbols

    Machine              = hex(struct.unpack("H",FileHeader[0:2])[0])  # H = unsigned short (size=2) WORD  
    NumberOfSections     = hex(struct.unpack("H",FileHeader[2:4])[0])
    TimeDateStamp        = hex(struct.unpack("I",FileHeader[4:8])[0])  # I = unsigned int (size=4) DWORD
    PointerToSymbolTable = hex(struct.unpack("I",FileHeader[8:12])[0])
    NumberOfSymbols      = hex(struct.unpack("I",FileHeader[12:16])[0])
    SizeOfOptionalHeader = hex(struct.unpack("H",FileHeader[16:18])[0])
    Characteristics      = hex(struct.unpack("H",FileHeader[18:20])[0])

    MachineType = GetMachineType(Machine)
    if MachineType == False:
        print("[ERROR] This is not a COFF File\n")
        exit(1)

    if SizeOfOptionalHeader != '0x0':
        print("[ERROR] This is file has an optional header, it is likly an PE file, not an COFF object file (.o)\n")
        exit(1)

    print(f"Machine              : {Machine} ({MachineType})")
    print(f"NumberOfSections     : {NumberOfSections}")
    print(f"TimeDateStamp        : {TimeDateStamp}")
    print(f"PointerToSymbolTable : {PointerToSymbolTable}")
    print(f"NumberOfSymbols      : {NumberOfSymbols}")
    print(f"SizeOfOptionalHeader : {SizeOfOptionalHeader}")
    print(f"Characteristics      : {Characteristics} ({GetCharacteristics(Characteristics)})\n")

    SymbolTableStart = int(PointerToSymbolTable,16)

    return NumberOfSections

def to_bytestring(seq):
    """
    convert sequence of chr()-able items to a str of
     their chr() values.
    in reality, this converts a list of uint8s to a
     bytestring.
    """
    return "".join(map(chr, seq))

def print_symbols(SymbolsTable, SymbolNumber):
    global AuxiliaryCount
    global StringTable
    global content
    global sections

    SymbolNumber = hex(SymbolNumber)

    LastAuxiliaryCount  = int(AuxiliaryCount,16)

    tab = ""
    if LastAuxiliaryCount > 0:
        tab="\t"

    SymbolName          = SymbolsTable[0:8]
    SymbolValue         = hex(struct.unpack("I",SymbolsTable[8:12])[0])
    SectionNumber       = hex(struct.unpack("H",SymbolsTable[12:14])[0])
    Type                = hex(struct.unpack("H",SymbolsTable[14:16])[0])
    StorageClass        = SymbolsTable[16:17].hex()
    AuxiliaryCount      = SymbolsTable[17:18].hex()

    if struct.unpack("I",SymbolsTable[0:4])[0] == 0:
        if LastAuxiliaryCount > 0:
            SymbolNameStr = ' '.join(hex(e) for e in list(SymbolName)) 
            SymbolNameStr = ''.join(c for c in SymbolNameStr if c.isprintable())
            print(f"{tab}SymbolName          = {SymbolNameStr} ({SymbolNumber})")
        else:
            StringTableOffset = hex(struct.unpack("I",SymbolsTable[4:8])[0])
            SymbolNameStr     = StringTable[int(StringTableOffset,16):].split(b'\x00')[0].decode('utf-8', 'ignore')
            print(f"{tab}SymbolName          = strtable offset:{StringTableOffset} \"{SymbolNameStr}\" ({SymbolNumber})")
    else:
        if LastAuxiliaryCount > 0:
            SymbolNameStr = ' '.join(hex(e) for e in list(SymbolName))
            SymbolNameStr = ''.join(c for c in SymbolNameStr if c.isprintable())
            print(f"{tab}SymbolName          = {SymbolNameStr} ({SymbolNumber})") 
        else:
            SymbolNameStr = SymbolName.decode('utf-8', 'ignore')
            SymbolNameStr = ''.join(c for c in SymbolNameStr if c.isprintable())
            print(f"{tab}SymbolName          = {SymbolNameStr} ({SymbolNumber})")

    print(f"{tab}SymbolValue         = {SymbolValue}")    
    print(f"{tab}SectionNumber       = {SectionNumber}")  

    isFunction = False  
    if Type == '0x20':
        print(f"{tab}Type                = {Type} IMAGE_SYM_DTYPE_FUNCTION") 
        isFunction = True
    else:
        print(f"{tab}Type                = {Type}")  

    print(f"{tab}StorageClass        = 0x{StorageClass}")    
    print(f"{tab}AuxiliaryCount      = 0x{AuxiliaryCount}") 

    if isFunction and not LastAuxiliaryCount:
        if int(SectionNumber,16) > 0:
            funcStart = int(sections[str(int(SectionNumber,16))]['PointerToSectionData'],16)
            funcEnd   = funcStart + int(sections[str(int(SectionNumber,16))]['SectionSize'],16) - 1
            print(f"Function start      = {hex(funcStart)}")
            print(f"Function end        = {hex(funcEnd)}")
            print(f"Functionbytes (raw) = {''.join('{:02x}'.format(x) for x in content[funcStart:funcEnd])}")

            relocs = sections[str(int(SectionNumber,16))]['Relocations']
            relocsList = []
            for rl in relocs:
                relocsList.append(int(relocs[rl]["VirtualAddress"],16))

            funcstr = ""
            for i,b in enumerate(content[funcStart:funcEnd]):
                if i in relocsList or i-1 in relocsList or i-2 in relocsList or i-3 in relocsList:
                    funcstr += ".."
                else:
                    funcstr += "{:02X}".format(b)

            # Remove NOP padding (0x90):
            funcstr = re.sub(r"(90)+$", "", funcstr)
            funcLen = int(len(funcstr)/2) 
            print(f"Functionbytes (pat) = {funcstr}")
            print(f"Function Length     = {funcLen} ({hex(funcLen)})")

            First32byte = funcstr[:64].ljust(64,'.') 
            print(f"First 32 bytes      = {First32byte}")

            # Getting CRC16 block

            # Find first occurence of a dynamic byte ('..')
            FirstVarOffset = funcstr[64:].find('..') + 64
            #CRC16 block should not be bigger than 255 byte
            MaxOffset = 255*2+32*2
            # If there is no dynamic byte and the CRC block is larger than 256 byte
            if FirstVarOffset > MaxOffset:
                FirstVarOffset = MaxOffset
            
            # Is there at least one byte to CRC 64 + 1
            if FirstVarOffset >=65:
                CRC16bytes = funcstr[64:FirstVarOffset]
            # CRC block doesn't contain any '..'
            elif FirstVarOffset == 63:
                CRC16bytes = funcstr[64:MaxOffset]
            else:
                CRC16bytes = "" 

            print(f"CRC16 bytes         = {CRC16bytes}")

            CRC16bytesLen  = int(len(CRC16bytes) / 2)
            CRC16bytearr   = bytearray.fromhex(CRC16bytes)
            CRC16          = crc16(to_bytestring(CRC16bytearr), crc=0xFFFF)
         
            print(f"First 32 bytes      = {First32byte}")
            print(f"CRC16 length        = {CRC16bytesLen} ({hex(CRC16bytesLen)})")
            print(f"CRC16 bytes         = {CRC16bytes}")
            print(f"CRC16               = {CRC16} ({hex(CRC16)})")

            TailBytes = funcstr[64 + CRC16bytesLen*2:]
            print(f"Tail bytes          = {TailBytes}")

            reloc = sections[str(int(SectionNumber,16))]['Relocations']

            called_func_dict = {}
            for r in reloc:
                vaddr    = "{:08X}".format(int(reloc[r]["VirtualAddress"],16))
                funcname = reloc[r]["SymbolName"]
                if '$' in funcname:
                    funcname = funcname.split('$')[1]
                called_func_dict.update({vaddr:funcname})
                
            called_func_dict = dict(sorted(called_func_dict.items()))

            called_func_str = ""
            for v in called_func_dict:
                called_func_str += f"^{v} {called_func_dict[v]} "

            sig_str = f"{First32byte} {CRC16bytesLen:02X} {CRC16:04X} {funcLen:04X} :00000000 {SymbolNameStr} {called_func_str}{TailBytes}"

            # Filter out too small modules (less than 4 constant bytes)
            num_staticbytes = int((len(First32byte)/2 - First32byte.count(".."))) + int((len(TailBytes)/2 - TailBytes.count("..")))
            if num_staticbytes < 4:
                print(f"[INFO] Function too small, has only {num_staticbytes} static bytes")
            else:
                print(f"Final Signature     = {sig_str}")

                # ---------------------------------- For debugging -----------------------------------
                #if First32byte == '89C881F9FFFF0000761381F9000000014819C94883E1F84883C118EB0E31C93D':
                #    exit(0)
                #if SymbolNameStr == 'TM__T8UX4uCLBe2k9c29b5ubzYSA_2':
                #    exit(0)

                # write signature to file
                file_out.write(f"{sig_str}\n")

    print('\n')

def print_relocations(relocationtable, SectionNumber, RelocationNumber):
    global sections
    global content
    global StringTable
    global SymbolTableStart

    VirtualAddress     = hex(struct.unpack("I",relocationtable[0:4])[0])
    SymbolIndex        = hex(struct.unpack("I",relocationtable[4:8])[0])
    TypeOfRelocation   = hex(struct.unpack("H",relocationtable[8:10])[0])

    SymbolsTable = content[SymbolTableStart + (int(SymbolIndex,16) * 18):] 
    SymbolType   = hex(struct.unpack("H",SymbolsTable[14:16])[0])
    SymbolName   = SymbolsTable[0:8]

    if struct.unpack("I",SymbolsTable[0:4])[0] == 0:
        StringTableOffset = hex(struct.unpack("I",SymbolsTable[4:8])[0])
        SymbolNameStr     = StringTable[int(StringTableOffset,16):].split(b'\x00')[0].decode('utf-8', 'ignore')
    else:
        SymbolNameStr = ''.join(c for c in SymbolName.decode('utf-8', 'ignore') if c.isprintable())
       
    print(f"VirtualAddress    : {VirtualAddress}")
    print(f"SymbolIndex       : {SymbolIndex} ")
    print(f"TypeOfRelocation  : {TypeOfRelocation}")
    print(f"SymbolsName       : {SymbolNameStr}")
    print(f"SymbolsTyp        : {SymbolType}")
    print(f"SymbolsFileOffset : {hex(SymbolTableStart + int(SymbolIndex,16) * 18)}\n")

    sections[str(SectionNumber)]["Relocations"].update({ f"{RelocationNumber}" : { 
                                                        "VirtualAddress"   : VirtualAddress,
                                                        "TypeOfRelocation" : TypeOfRelocation,
                                                        "SymbolIndex"      : SymbolIndex,
                                                        "SymbolName"       : SymbolNameStr,
                                                        "SymbolType"       : SymbolType } } )

def print_coff_section(SectionHeader, SectionNumber):
    global content
    global sections
    global StringTableDict

    SectionName          = SectionHeader[0:8]
    PhysicalAddress      = hex(struct.unpack("I",SectionHeader[8:12])[0])
    VirtualAddress       = hex(struct.unpack("I",SectionHeader[12:16])[0])
    SectionSize          = hex(struct.unpack("I",SectionHeader[16:20])[0]) 
    PointerToSectionData = hex(struct.unpack("I",SectionHeader[20:24])[0])
    PointerToRelocations = hex(struct.unpack("I",SectionHeader[24:28])[0])
    PointerToLinenumbers = hex(struct.unpack("I",SectionHeader[28:32])[0])
    NumberOfRelocations  = hex(struct.unpack("H",SectionHeader[32:34])[0])
    NumberOfLinenumbers  = hex(struct.unpack("H",SectionHeader[34:36])[0])
    Characteristics      = hex(struct.unpack("I",SectionHeader[36:40])[0])
    
    # check if section name start with a '/' = 0x2f to look up the name in the string table
    if SectionName[0] == 0x2f:
        #print(f"SectionNameHex       : {' '.join('{:02x}'.format(x) for x in SectionName) }")
        StrTableOffset = hex(int(''.join(c for c in SectionName[1:].decode('utf-8') if c.isprintable())))
        SectionName = StringTableDict[StrTableOffset]
    # Section name fits in the 8 bytes of the header field
    else:
        SectionName = ''.join(c for c in SectionName.decode('utf-8') if c.isprintable())

    print(f"SectionName          : {SectionName} ({SectionNumber})")
    print(f"PhysicalAddress      : {PhysicalAddress}") 
    print(f"VirtualAddress       : {VirtualAddress}")
    print(f"SectionSize          : {SectionSize}")
    print(f"PointerToSectionData : {PointerToSectionData}")
    print(f"PointerToRelocations : {PointerToRelocations}")
    print(f"PointerToLinenumbers : {PointerToLinenumbers}")
    print(f"NumberOfRelocations  : {NumberOfRelocations}")
    print(f"NumberOfLinenumbers  : {NumberOfLinenumbers}")
    print(f"Characteristics      : {Characteristics}\n")

    sections.update({f"{SectionNumber}": 
        {"SectionName"          : SectionName, 
         "PhysicalAddress"      : PhysicalAddress,
         "VirtualAddress"       : VirtualAddress,
         "SectionSize"          : SectionSize,
         "PointerToSectionData" : PointerToSectionData,
         "PointerToRelocations" : PointerToRelocations,
         "PointerToLinenumbers" : PointerToLinenumbers,
         "NumberOfRelocations"  : NumberOfRelocations,
         "NumberOfLinenumbers"  : NumberOfLinenumbers,
         "Characteristics"      : Characteristics,
         "Relocations"          : {}}
        })

    if int(NumberOfRelocations,16):
        print("Relocations:")
        relocationtable = content[int(PointerToRelocations,16):]
        for RelocationNumber in range(0,int(NumberOfRelocations,16)):
            print_relocations(relocationtable[RelocationNumber*10:], SectionNumber, RelocationNumber)




# --- Main ---

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <OBJECT_FILE_TO_PARSE> <OUTPUT_SIGNATURE_FILE>\n")
    print("[WARNING] This script assumes the object file is compiled with MinGW with --ffunction-sections parameter !")
    exit(1)

signature_file = sys.argv[2]

file_out = open(signature_file, "w")

with open(sys.argv[1], 'rb') as f:
    content = bytearray(f.read())

print(f"Fileheader:")
print(f"-----------")
NumberOfSections = int(print_fileheader(content),16)
SectionStart=20

StringTableOffsetStart = StringTableOffset = SymbolTableStart + int(NumberOfSymbols,16) * 18
StringTable            = content[StringTableOffset:]
StringtableSize        = hex(struct.unpack("I",StringTable[0:4])[0]) 

print(f"Stringtable:")
print(f"------------")
print(f"StringTableOffset = {hex(StringTableOffsetStart)}")
print(f"StringtableSize   = {StringtableSize}\n")

StringTableDict        = {} 
StringTableOffset += 4
stringlist=StringTable[4:].split(b'\x00')[:-1]
for i,s in enumerate(stringlist,1):
    ss = s.decode('utf-8')
    ss_len = len(ss)
    strtable_offset = hex(StringTableOffset-StringTableOffsetStart)
    print(f"{i}. \"{ss}\" (file offset:{hex(StringTableOffset)}) (strtable offset:{strtable_offset})")
    StringTableDict.update({f"{strtable_offset}" : f"{ss}"})
    StringTableOffset += ss_len + 1

print(f"\nSections:")
print(f"---------")
for SectionNumber in range(1,NumberOfSections+1):
    print_coff_section(content[SectionStart:], SectionNumber)
    SectionStart += 40

print(f"Symbols:")
print(f"--------")
SymbolTableOffset = SymbolTableStart
for SymbolNumber in range(1, int(NumberOfSymbols,16)+1):
    SymbolsTable = content[SymbolTableOffset:]
    print_symbols(SymbolsTable, SymbolNumber-1)
    SymbolTableOffset += 18

file_out.write('---\n')
file_out.close()

print("------------------------------------------------------------------------------------------------------------------")
print(f"Done. Wrote signature file: '{signature_file}'' to disk.")
print("------------------------------------------------------------------------------------------------------------------")
