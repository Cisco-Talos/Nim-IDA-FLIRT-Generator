import idautils
import ida_segment
import ida_bytes
import ida_struct
import idc
import ida_nalt

MAX_STR_LENGTH = 30

seg_name  = '.rdata'
seg_start = ida_segment.get_segm_by_name(seg_name).start_ea
seg_end   = ida_segment.get_segm_by_name(seg_name).end_ea

print(f"Segment {seg_name}: start: 0x{seg_start:x}  end:0x{seg_end:x}")

def get_str_len(str_start):
    for c, ea in enumerate(range(str_start, str_start+30)):
        b = ida_bytes.get_byte(ea)
        if b == 0:
            return c 
    return 0


def create_NIM_str_struct():
    name = "NIM_string"
    struct_id = ida_struct.get_struc_id(name)
    if struct_id == ida_idaapi.BADADDR:
        struct_id = idc.add_struc(0, name, 0)
        print(f"[INFO] Created struct \"{name}\" with id: {struct_id}")
        idc.import_type(-1, name)  
        idc.add_struc_member(struct_id, "length", -1, ida_bytes.FF_QWORD|ida_bytes.FF_DATA, -1, 8) 
        idc.add_struc_member(struct_id, "unknown", -1, ida_bytes.FF_QWORD|ida_bytes.FF_DATA, -1, 8) 
        idc.add_struc_member(struct_id, "cstr", -1, ida_bytes.FF_STRLIT|ida_bytes.FF_DATA, ida_nalt.STRTYPE_TERMCHR, 0)
        print(f"[INFO] Added structure members")
        return True
    else:
        print(f"[WARNING] Struct \"{name}\" already exists (id: {struct_id})")
        return False

    
def apply_NIM_str_struct(ea):
    struct_id = ida_struct.get_struc_id("NIM_string")
    str_ea    = ea + 16
    strlength = get_str_len(str_ea)
    if strlength:
        length    = ida_struct.get_struc_size(struct_id) + strlength 
        create_struct(ea, length, "NIM_string")
    else:
        print(f"[WARNING] Failed to apply structure at {ea}")


# --- Main ---
create_NIM_str_struct()

for ea in range(seg_start, seg_end):
    seg_xrefs = XrefsTo(ea, 0)
    for xref in seg_xrefs:
        str_ea = ea + 16
        str_bytes = ida_bytes.get_bytes(str_ea, MAX_STR_LENGTH)
        str_offset_len = ida_bytes.get_dword(ea)
        str_strlen_len = get_str_len(str_ea)
        
        # Did we find a real string (lenght field in the structure is equal to the calculated string length and not 0) ?
        try:
            if (str_offset_len == str_strlen_len) and (str_offset_len != 0):
                apply_NIM_str_struct(ea)
                b = idaapi.get_bytes(str_ea, str_strlen_len)
                orgstr   = str(b[:MAX_STR_LENGTH],'utf-8')
                shortstr = ''.join(filter(str.isalnum, orgstr))
                print(f"Address:{hex(ea)} xref:{hex(xref.frm)} Len:{str_offset_len} strlen: {str_strlen_len} s: {shortstr} str:{orgstr}")
                ida_bytes.create_strlit(str_ea, 0, ida_nalt.STRTYPE_TERMCHR)
                idc.set_cmt(xref.frm, orgstr,0)
                idaapi.set_name(ea, '_a' + shortstr, idaapi.SN_NOWARN | idaapi.SN_NOCHECK)
        except:
            print(f"[Exception] Failed to decode string. xref from = {hex(xref.frm)} to {hex(xref.to)}")  

print("----- done -----")

#ea = idaapi.find_binary(ea + 1, seg.endEA, "4E 80 00 20", 16, idaapi.SEARCH_DOWN)

