###############################################################################################################################
#                                                                                                                             #
# Objectfile(.o) to pattern file (.pat) generator                                                                             #
#                                                                                                                             #
# This script finds all object files built by the nim_rtl_builder.py script and uses the coffparser.script to generate        #
# IDA .pat files which can be consumed by the IDA SDK sigmake tool                                                            #
#                                                                                                                             #
# Author: Holger Unterbrink (hunterbr@cisco.com)                                                                              #
#                                                                                                                             #
# (c) 2023 Cisco Talos / Primary License: BSD (except code from external sources)                                             #
#                                                                                                                             #
# Usage: python obj2patfile.py                                                                                                 #
#                                                                                                                             #
#                                                                                                                             #
###############################################################################################################################

import glob
import os
import subprocess

NIM_SIGNAME = "nim-1612"                                        # signature filename - no underscores or blanks are allowed
COFFPARSER  = "C:\\tools\\Nim\\src\\coffparser.py"              # Path to coffparser.py script    
SIGMAKE     = "C:\\tools\\IDA\\flair82\\bin\\win\\sigmake.exe"  # Path to HexRays SDK sigmake executable

# --- Nothing needs to be changed below this line ---

# maybe for later automation, not used itm
# os.chdir("/mydir")

pat_files_str = ""
for obj_filename in glob.glob("*.o"):
    pat_filename = os.path.splitext(obj_filename)[0]
    pat_filename = pat_filename.split("@")[-1] + '.pat'
    pat_files_str += pat_filename + '+'
    exec_cmd = ['python', COFFPARSER, obj_filename, pat_filename]
    exec_cmd_str = " ".join(exec_cmd)
    print(f"Built cmd: {exec_cmd_str}")
    return_code = subprocess.call(exec_cmd)

    if return_code == 0:
        print(f"Command executed successfully.")
    else:
        print(f"Command failed with return code: {return_code}")
        exit(1)

    #input("Press Enter to continue...")

sigmake = SIGMAKE + f' -n"{NIM_SIGNAME}" '
sigout  = f' {NIM_SIGNAME}.sig'
pat_files_str = pat_files_str[:-1]

print("----------------------------------------------------------------------------------------------------------------------")
print("Done. Now execute:")
print(sigmake + pat_files_str + sigout)
print(f"\nIf you see COLLISIONS, just delete the comment lines in the head of the generated {NIM_SIGNAME}.exc file and run the")
print("command above again. Read the IDA SKD docs for more details")
print(f"Once generated, copy '{NIM_SIGNAME}.sig' to IDA signature folder e.g. 'C:\\Program Files\\IDA Pro 8.2\\sig\\pc'")
print("----------------------------------------------------------------------------------------------------------------------")

