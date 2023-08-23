###################################################################################
#                                                                                 # 
# Nim RTL parser                                                                  #                
#                                                                                 # 
# This script is parsing all important Nim run time library (RTL) files,          #                                                                        
# extracts the functions and builts a large Nim source code file, which           #                                                                       
# includes these functions and their functions calls.                             #                                                     
#                                                                                 # 
# Author: Holger Unterbrink (hunterbr@cisco.com)                                  #                                                
#                                                                                 #
# IMPORTANT:                                                                      # 
# Run this script in the '<Nim_install_dir>\lib\pure' directory and make sure     #                                                                             
# the 'nim' executable is in your PATH                                            #                                      
#                                                                                 # 
# Usage: nim_rtl_builder.py                                                       # 
#                                                                                 # 
#                                                                                 #
# Copyright 2023 Cisco Systems, Inc. and its affiliates                           #

#                                                                                 #
# Licensed under the Apache License, Version 2.0 (the "License");                 #
# you may not use this file except in compliance with the License.                #
# You may obtain a copy of the License at                                         #
#                                                                                 #
#      http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                                 #
# Unless required by applicable law or agreed to in writing, software             #
# distributed under the License is distributed on an "AS IS" BASIS,               #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.        #
# See the License for the specific language governing permissions and             #
# limitations under the License.                                                  #
#                                                                                 #
# SPDX-License-Identifier: Apache-2.0                                             #
#                                                                                 #
###################################################################################

import sys
import re
import os
import glob
import shutil
import subprocess
import pyparsing as pp
from inspect import currentframe, getframeinfo
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")

OBJ2PATFILE          = "C:\\tools\\Nim\\src\\obj2patfile.py"
MISSED_FUNC_FILENAME = f"missed_functions-{timestamp}"
NIM_CACHE_DIR        = 'HU_nim_cache'

DBG_LEVEL = 1

# --- Nothing needs to be changed below this line ---

# pyparsing vars
LPARANT, RPARANT, LBRACE, RBRACE, LBRACK, RBRACK, STAR, ORTOKEN, EQUAL = map(pp.Suppress, "(){}[]*|=")
T = pp.Suppress('T: ')

var_counter = 1
success_rate = {}
skipped_functions = {}

def print_debug(s, level, frameinfo):
    if level <= DBG_LEVEL:
        info = f"(Line: {frameinfo.lineno:04d}): "
        width = 13
        print(f"{info: <{width}}{s}")

def remove_from_strlist(l,s,filename):
    global skipped_functions
    ret = []
    for i in l:
        if bool(re.search('func <#.*?>', i)):
            print(f"Skipping (Reason: {s}): {i}")
            skipped_functions[filename].append(f"[Reason: {s}] " + i)
            continue
        if s in i:
            print(f"Skipping (Reason: {s}): {i}")
            skipped_functions[filename].append(f"[Reason: {s}] " + i)
            continue

        ret.append(i)

    return ret

def parse_t(gen):
    t = "[ERROR] wasn't able to split up T generic"
    if gen:
        if ':' in gen:
            t = gen.split(':')[1].lstrip()
            if '|' in t:
                t = t.split('|')[0].lstrip() 
        # We are replacing an unkown generic Type with int for now
        elif '[T]' in gen:                        
            t = 'int'
    # We are replacing an unkown generic Type with int for now
    else:
        print_debug(f"gen        : '{gen}'",1, getframeinfo(currentframe()))
        t = 'int'

    return t

def parse_basic_arg(argtype, gens=None):

    print_debug(f"argtype : {argtype}    gens : {gens}",1, getframeinfo(currentframe()))

    global var_counter

    argtype = argtype.replace("]", "").lstrip().rstrip()

    string_types = ["string", "cstring", "WideCString"]
    int_types    = ["cint","cuint32","csize","int","int8","int16","int32","int64","uint","uint8","uint16","uint32","uint64", "Natural", "Positive", "not string", "SomeInteger", "SomeNumber", "csize_t", "BiggestInt", "BiggestUInt"]
    float_types  = [ "float", "float32", "float64","cfloat", "cdouble", "SomeFloat", "BiggestFloat"]

    special_int = ["int8","int16","int32","int64","uint8","uint16","uint32","uint64"]

    argstr  = ""
    
    if argtype == 'char':
        argstr = f"var cha{var_counter}: {argtype} = 'A'" 
        var_counter += 1
    elif argtype == 'byte':
        argstr = f"var byt{var_counter}: {argtype} = byte('a')"
        var_counter += 1
    elif argtype == 'Rune':
        argstr = f"var rru{var_counter}: {argtype} = \"ä\".runeAt(0)"
        var_counter += 1
    elif argtype == 'bool':
        argstr = f"var boo{var_counter}: {argtype} = true"
        var_counter += 1
    elif argtype == 'WINBOOL':
        argstr = parse_basic_arg("int32", gens)
    elif any(argtype == t for t in int_types): 
        if any(argtype == t for t in special_int):
            int_size_str = pp.Suppress(pp.Word(pp.alphas)) + pp.Word(pp.nums)
            int_size     = int_size_str.parseString(argtype, parseAll=False)[0]
            if argtype.startswith('u'):
                int_type = 'u'
            else:
                int_type = 'i'
            argstr = f"var iii{var_counter}: {argtype} = 1'{int_type}{int_size}"
        else:
            argstr = f"var iii{var_counter}: {argtype} = 1"
        var_counter += 1
    elif any(argtype in t for t in float_types):
        argstr = f"var fff{var_counter}: {argtype} = 1.0"
        var_counter += 1
    elif argtype == 'FloatFormatMode':
        argstr = f"var ffm{var_counter}: {argtype} = ffDefault"
        var_counter += 1
    elif any(argtype in t for t in string_types):
        argstr = f"var sss{var_counter}: {argtype} = \"talos\""
        if argtype == 'WideCString': 
            argstr = f"var sss{var_counter}: {argtype} = newWideCString(\"talos\")"
        var_counter += 1
    elif argtype == 'pointer':
        argstr = f"var ppp{var_counter}: {argtype}"
        var_counter += 1
    elif argtype == 'File':  
        argstr = f"var fil{var_counter}: {argtype} = open(\"test.txt\", fmReadWrite)"
        var_counter += 1
    elif argtype == 'FileSeekPos':  
        argstr = f"var fse{var_counter}: {argtype} = fspSet"
        var_counter += 1
    elif argtype == 'FileMode':  
        argstr = f"var fmo{var_counter}: {argtype} = fmReadWrite"
        var_counter += 1
    elif  'Handle' in argtype:  
        if 'var ' in argtype:
            argtype = argtype.replace('var ', '')
        argstr = f"var fhd{var_counter}: {argtype} = getOsFileHandle(open(\"test.txt\", fmReadWrite))"
        var_counter += 1
    elif argtype == 'Process':
        argstr = f"var proz{var_counter}: {argtype} = startProcess(\"myprocess.exe\")"
        var_counter += 1
    elif argtype == 'FilePermission':  
        argstr = f"var fpe{var_counter}: {argtype} = fpUserExec"
        var_counter += 1
    elif argtype == 'Mode':
        argstr = f"var fff{var_counter}: {argtype} = 0o40000"
        var_counter += 1
    elif argtype == 'T':
        argstr = parse_basic_arg(parse_t(gens))    
    elif "var " in argtype:
        argtype = parse_basic_arg(argtype.replace("var ", ""), gens)
        argstr = f"{argtype}"
    elif argtype.startswith('set['):
        argtype = argtype.replace("set[", "").replace("]", "")
        argstr_set = parse_basic_arg(argtype, gens).split('=')[-1].lstrip().rstrip()
        argstr = f"var se{var_counter}: set[{argtype}] = " + '{' + f"{argstr_set}, {argstr_set}, {argstr_set}" + '}'
        var_counter += 1
    elif "openArray" in argtype:
        argtype += ']' # openArray[int8|uint8]
        if '|' in argtype:
            arg = pp.Suppress('openArray') + LBRACK + (pp.SkipTo(ORTOKEN) + ORTOKEN) 
        else:
            arg = pp.Suppress('openArray') + LBRACK + (pp.SkipTo(RBRACK) + RBRACK)   

        argtype = arg.parseString(argtype, parseAll=False)[0]
        if argtype == 'T':
            argtype = parse_t(gens)
        argstr_array = parse_basic_arg(argtype, gens).split('=')[-1].lstrip().rstrip()
        argstr = f"var openarr{var_counter}: seq[{argtype}] = @[{argstr_array}, {argstr_array}, {argstr_array}]"
    elif "varargs" in argtype:
        if ', `$`' in argtype:
            argtype = argtype.replace(', `$`','')
        argtype += ']'
        arg  = pp.Suppress('varargs') + LBRACK + pp.Optional(LPARANT) + pp.SkipTo(RBRACK) + RBRACK 
        args = arg.parseString(argtype, parseAll=False)[0]
        args = args.split(',')
        vararg_arg_str = ""
        for arg in args:
            arg = arg.lstrip().rstrip()
            vararg_arg_str_tmp = parse_basic_arg(arg, gens)
            vararg_arg_str += vararg_arg_str_tmp + '---'
        argstr = '>>>' + vararg_arg_str[:-3] + '<<<'
    else:
        print("[ERROR] basic type not found. <---------------------------------------------------------")
        print(f"argtype = '{argtype}'")
        print(f"gens = {gens}")
        print(f"parse_t_gens = {parse_t(gens)}")
        exit(1)
    
    return argstr

def parse_arg(fn_arg, gens=None):
    if ':' in fn_arg:
        if 'varargs' in fn_arg:
            # Assuming varargs is always at the end of a function
            arg =  pp.Word(pp.alphanums+'_') + ': ' +  pp.restOfLine
        else:
            arg =  pp.Word(pp.alphanums+'_') + ': ' +  pp.Word(pp.alphanums+' _[]|`$')

        parsed_arg = arg.parseString(fn_arg, parseAll=False)
        print_debug(f"parsed_arg  : {parsed_arg} <-",1, getframeinfo(currentframe()))
    else:
        parsed_arg = [fn_arg, ': ', 'not assigned']
        print_debug(f"parsed_arg  : {parsed_arg} <--",1, getframeinfo(currentframe()))

    argtype = parsed_arg[2].lstrip().rstrip()
    print_debug(f"argtype     : '{argtype}'",2, getframeinfo(currentframe()))

    argstr = parse_basic_arg(argtype, gens)

    return argstr

def parse_args(fn_args, gens=None):
    #f: var File, filehandle: FileHandle, mode: FileMode = fmRead
    #f: File, pos: int64, relativeTo: FileSeekPos = fspSet
    #arg = pp.OneOrMore((pp.Word(pp.alphanums+'_') + ':' + pp.Word(pp.alphanums+'_')) | (pp.Word(pp.alphanums+'_') + ',')) 
    #parsed_arg = arg.parseString(a, parseAll=False)

    #Function with noe arguments:
    if fn_args == "":
        print_debug("Function has no arguments.", 2, getframeinfo(currentframe()))
        return ""

    # split arguments to list
    if 'varargs' in fn_args:
        varg_str = re.search(r'(\w+(?:: varargs|:varargs)\[.*,*)', fn_args).group(1)
        fn_args = fn_args.replace(varg_str,"XXX_YYY_ZZZ")
        fn_args_list_tmp = re.split('[,;]', str(fn_args))
        fn_args_list = [s.replace('XXX_YYY_ZZZ', varg_str) for s in fn_args_list_tmp]
    else:
        fn_args_list = re.split('[,;]', str(fn_args))
    for a in fn_args_list:
        if 'doRaise' in a:
            del fn_args_list[fn_args_list.index(a)]

    print_debug(f"fn_args_list: {fn_args_list} <-",1, getframeinfo(currentframe()))

    # parse splitted arguments
    all_fn_args = ""
    for fn_arg in fn_args_list:
        # are there vargs in the function arguments ?
        if 'varargs' in fn_arg:
            fn_arg_index = fn_args_list.index(fn_arg)
            fn_args_list[fn_arg_index : fn_arg_index+2] = [''.join(fn_args_list[fn_arg_index : fn_arg_index+2])]
            print_debug(f"New fn_args_list = {fn_args_list}", 1, getframeinfo(currentframe()))
            fn_arg = fn_args_list[fn_arg_index]

        # check if we hav constructs like func(a,b = int)
        arg_type = ""
        if not ':' in fn_arg:
            fn_arg_index = fn_args_list.index(fn_arg)
            arg_type = 'type not found'
            for arg_w_type in fn_args_list[fn_arg_index:]:
                if ':' in arg_w_type:
                    fn_arg_w_type_index = fn_args_list.index(arg_w_type)
                    arg_type = fn_args_list[fn_arg_w_type_index].split(':')[1]
                    break

            fn_arg = fn_args_list[fn_arg_index] + ':' + arg_type

        print_debug(f"fn_arg      : {fn_arg} <=",1, getframeinfo(currentframe()))

        # Some special cases like: 
        # proc parseBin*[T: SomeInteger](s: string, number: var T, start = 0, maxLen = 0): int {.noSideEffect.}
        if arg_type == 'type not found':
            continue

        # Parse arguments
        argtypestr = parse_arg(fn_arg, gens)
        print_debug(f"argtypestr  : {argtypestr}",1,getframeinfo(currentframe()))
        all_fn_args += argtypestr + '---'

    return all_fn_args[:-3] 

def get_arg_name(fn_arg):
    fn = pp.Suppress('var ') + pp.Word(pp.alphanums) + pp.Suppress(':')
    parsed_var_name = fn.parseString(fn_arg, parseAll=False)
    print_debug(f"parsed_var_name: {parsed_var_name}",1,getframeinfo(currentframe()))
    return parsed_var_name[0]


def gen_function(f):
    # Examples: 
    #proc writeFile*(filename: string, content: openArray[byte]) {.since: (1, 1).}
    #func floorMod*[T: SomeNumber](x, y: T): T =
    #func sin*[T: float32|float64](x: T): T {.importc: "Math.sin", nodecl.}
    #func lcm*[T](x: openArray[T]): T {.since: (1, 1).}
    #func `^`*[T: SomeNumber](x: T, y: Natural): T =        
    #proc write*(f: File, a: varargs[string, `$`]) {.tags: [WriteIOEffect], benign.}
                                      #func multiReplace*(s: string, replacements: varargs[(string, string)]): string =
    fn = pp.oneOf(['proc ','func ']) + pp.Word(pp.alphanums+'_`^')("fn_name") + pp.Optional('*') \
                                     + pp.Optional('[T]')("fn_gen_empty") + pp.Optional('[T: ' + pp.SkipTo(RBRACK) + RBRACK)("fn_gen") \
                                     + pp.MatchFirst([pp.Combine(LPARANT + pp.SkipTo('varargs[' + 'varargs[' + pp.SkipTo(RBRACK))("fn_args") + RBRACK + pp.SkipTo(RPARANT) + RPARANT), \
                                                      LPARANT + pp.SkipTo(RPARANT)("fn_args") + RPARANT]) \
                                     + pp.Optional(':') + pp.Optional(pp.SkipTo(LBRACE|EQUAL))("rettype") \
                                     + pp.Optional(LBRACE)

    parsed_fn = fn.parseString(f, parseAll=False)

    print_debug(f"parsed_fn   : {parsed_fn}",1,getframeinfo(currentframe()))
    print_debug(f"fn_name     : {parsed_fn['fn_name']}",1,getframeinfo(currentframe()))
    print_debug(f"fn_args     : {parsed_fn['fn_args']}",1,getframeinfo(currentframe()))
    print_debug(f"fn_rettype  : {parsed_fn['rettype']}",1,getframeinfo(currentframe()))

    fn_rtype_found = False
    gen_found = False
    gen_found_empty = False
    try:
        fn_rtype       = parsed_fn['rettype'].lstrip().rstrip()
        if ':' in fn_rtype:

            fn_rtype = "".join(fn_rtype.split(':')[-1]).lstrip().rstrip()
        fn_rtype_found = True
    except:
        print_debug(f"[ERROR] Failed to parse return type of function.",1,getframeinfo(currentframe()))
        raise
    
    try:
        gens = "".join(parsed_fn['fn_gen'])
        gen_found = True
        print_debug(f"fn_gen     : {parsed_fn['fn_gen']}",1,getframeinfo(currentframe()))
        print_debug(f"gens       : {gens}",1,getframeinfo(currentframe()))
    except:
        pass

    try:
        gens_empty = "".join(parsed_fn['fn_gen_empty'])
        gen_found_empty = True
        print_debug(f"fn_gen_empty     : {parsed_fn['fn_gen_empty']}",1,getframeinfo(currentframe()))
    except:
        pass

    if fn_rtype_found:
        print_debug(f"Fn ret value: {fn_rtype}",1,getframeinfo(currentframe()))
    else:
        fn_rtype = ''

    if gen_found:
        all_fn_args = parse_args(parsed_fn['fn_args'], gens)
    elif gen_found_empty:
        all_fn_args = parse_args(parsed_fn['fn_args'], gens_empty)
    else:
        all_fn_args = parse_args(parsed_fn['fn_args'])
    
    print_debug(f"Generic     : No generics found.",1,getframeinfo(currentframe()))
    print_debug(f"all_fn_args : {all_fn_args}",1,getframeinfo(currentframe()))

    all_fn_args_splitted = all_fn_args.split('---')
    print_debug(f"all_fn_args_splitted   : {all_fn_args_splitted}",1,getframeinfo(currentframe()))

    var_str = ""
    arg_str = ""
    arg_name = ""
    if all_fn_args == '': 
        ret = "TBD <------------"
    else:
        for fn_arg in all_fn_args_splitted:
            if '>>>' in fn_arg or '<<<' in fn_arg:
                arg_name = get_arg_name(fn_arg.replace('>>>','').replace('<<<',''))
                if '>>>' in fn_arg:
                    arg_name = '(' + arg_name
                if '<<<' in fn_arg:
                    arg_name = arg_name + ')'
            else:
                arg_name = get_arg_name(fn_arg)
            print_debug(f"arg_name   : {arg_name}",1,getframeinfo(currentframe()))
            arg_str += arg_name + ','
            var_str += fn_arg + '\n'
            var_str = var_str.replace('>>>','').replace('<<<','')

    arg_str = arg_str[:-1]

    f = f.replace('\n','\n#')

    if fn_rtype == '':
        ret =  '#' + f + '\n' + var_str + parsed_fn['fn_name'] + '(' + arg_str + ')\n'
    else:
        ret = '#' + f + '\n' + var_str + 'discard ' + parsed_fn['fn_name'] + '(' + arg_str + ')\n' 

    print_debug(f"-----------------------------------------------------",1,getframeinfo(currentframe()))
    print_debug(f"Func call   : \n{ret}",1,getframeinfo(currentframe()))
    print_debug(f"-----------------------------------------------------",1,getframeinfo(currentframe()))
            
    return ret

def built_nim(filename_out, src_file, RTLfile):
    nim_cache_str = f"--nimcache:{NIM_CACHE_DIR}" 
    built_cmd = ["nim", "c", "-d:release", "--opt:size",  "--passC:-ffunction-sections" ,nim_cache_str, f"-o:{filename_out}", src_file]
    built_cmd_str = " ".join(built_cmd)
    print_debug(f"Built cmd: {built_cmd_str}",1,getframeinfo(currentframe()))
    #input("hit return")
    return_code = subprocess.call(built_cmd)

    if return_code == 0:
        print_debug(f"Command executed successfully.",1,getframeinfo(currentframe()))
    else:
        print_debug(f"Command failed with return code: {return_code}",1,getframeinfo(currentframe()))
        exit(1)

    return return_code

def parse_file(filename):
    global skipped_functions

    with open(filename, 'r', encoding="cp850" ) as f:
        lines = f.read()

    functions = re.findall(r"(?:proc|func) .*?\(.*?\).*?(?: =|\.\})", lines, re.DOTALL)
    functions_hits = len(functions)

    # Filter bad matches:

    # TBD: parseEnum, Slice, range, Process, Handle, tuple  <- not implemented yet, so we filter them
    # Process
    unwanted_functions = [ 'c_telli64',
                           'c_fsetpos',
                           'modeIsDir',
                           'Stat',
                           'isatty',
                           'transformLetters',
                           'c_ioctl',
                           'c_fgetpos',
                           'c_fcntl',
                           'c_memchr',
                           'generateGaussianNoise',
                           'toBitsImpl',
                           'truncImpl',
                           'jsSetSign',
                           'parseEnum',
                           'Slice', 
                           'SkipTable',
                           'range[',
                           'getPrefix',
                           'fromOct',
                           'fromBin',
                           'fromHex',
                           'jsRound',
                           'initOptParser',
                           'OptParser',
                           'CfgParser',
                           'Config',
                           'writeHelp',
                           'Stream',
                           'StringTableRef',
                           'writeVersion',
                           'PegKind',
                           ': Peg',
                           'PegLexer',
                           'PegParser',
                           'pegs',
                           'Rope',
                           'ptr cint',
                           'Argv',
                           'NonTerminal',
                           'NimNode',
                           'WIN32_FIND_DATA',
                           'proc isAdmin',
                           ': times',
                           'getSymlinkFileKind',
                           'getApplHaiku',
                           'getApplHeuristic',
                           'getApplFreebsd',
                           'getApplOpenBsd',
                           'getApplAux',
                           'find_path',
                           'normalizePathEnd',
                           'copyfile_state_alloc',
                           'StartProcessData',
                           'c_free',
                           'c_strlen',
                           'cuint32',
                           'RuneImpl',
                           'c_rename',
                           'findExe',
                           'inclFilePermissions',
                           'setFilePermissions',
                           'copyFileToDir',
                           'ptr ObjectWaitInfo',
                           'csystem',
                           'jsStartsWith',
                           'jsEndsWith',
                           'envToCStringArray',
                           'tuple',
                           'STARTUPINFO',
                           'open_osfhandle',
                           'flockfile',
                           'funlockfile',
                           'CmdLineKind' ]

    regex_mismatch_to_filter = [ 'proc is ',
                                 'proc to ',
                                 'proc that ',
                                 'proc for',
                                 'proc doesn',
                                 'proc(',
                                 'proc receives',
                                 'proc conforms',
                                 'proc will',
                                 'proc which',
                                 'proc for:',
                                 'func only',
                                 'func that',
                                 'func `%`*',
                                 'func strip',
                                 'func <#lcm,T,T>`_ for a version with two arguments',
                                 'func <#gcd,T,T>`_',
                                 'proc `$`*(dict',
                                 'func <#gcd,SomeInteger,SomeInteger>`_ for an integer version',
                                 'proc <#runeAtPos,string,int>',
                                 'proc <#toUTF8,Rune>',
                                 'proc <#rune',
                                 'proc <#runeReverseOffset,string,Positive>',
                                 'proc <#alignLeft,string,Natural>',
                                 'proc <#align,string,Natural>',
                                 'proc <#joinPath,string,string',
                                 'proc <#splitPath,string>',
                                 'proc <#parentDir,string>',
                                 'proc <#splitFile,string>',
                                 'proc <os',
                                 'proc <#readLines',
                                 'proc <#searchExtPos,string>',
                                 'proc <#dirExists,string>',
                                 'proc <#fileExists,string',
                                 'proc <#normalizedPath',
                                 'proc <#absolutePath',
                                 'proc <#createHardlink',
                                 'proc <#createSymlink',
                                 'proc <#copyDir',
                                 'proc <#copyFile',
                                 'proc <#getAppFilename',
                                 'proc <#getFileInfo',
                                 'proc <#sameFile',
                                 'proc <#resume',
                                 'proc <#suspend',
                                 'proc <#outputHandle',
                                 'proc <#inputHandle',
                                 'proc <#validate',
                                 'proc strip',
                                 'proc <#isLower',
                                 'proc `/../`*',
                                 'proc `*`',
                                 'proc <#$',
                                 'proc `<=%`',
                                 'proc `<%`',
                                 'proc `==`',
                                 'proc `$`',
                                 'proc `+`',
                                 'proc `-`',
                                 'seq[Process',
                                 'func createFactTable[N: static[int]]' ]

    strings_to_filter = [ 'inline',
                          'dynlib',
                          'android_log_print' ]

    strings_to_filter += regex_mismatch_to_filter + unwanted_functions

    
    skipped_functions[filename] = []
    for fs in strings_to_filter:
        functions = remove_from_strlist(functions,fs,filename) 

    all_fn_calls = []
    for i,f in enumerate(functions, 1):
        print_debug(f"Fn num      : {i}", 1, getframeinfo(currentframe()))
        print_debug(f"Fn def      : {f}", 1, getframeinfo(currentframe()))
        fn_call = gen_function(f)
        all_fn_calls.append(fn_call + '\n') 
        print('---')

    processed_functions = i 
    print_debug(f"Number of regex hits: {functions_hits} to {processed_functions} successfull processed functions\n", 1, getframeinfo(currentframe()))
    success_rate[filename] = {'functions_hits':functions_hits, 'processed_functions':processed_functions}

    all_uniq_fn_calls     = list(set(all_fn_calls))

    # check if we have functions with var arguments
    for f in all_uniq_fn_calls: 
        f_index = all_uniq_fn_calls.index(f)
        if 'varXXX' in f:
            new_f = parse_var_func(f)
            all_uniq_fn_calls[f_index] = new_f
        else:
            all_uniq_fn_calls[f_index] = f

 
    all_uniq_fn_calls_str = "".join(all_uniq_fn_calls)
    print("Function file content:")
    print("----------------------")
    print("".join(all_uniq_fn_calls_str))

    basename = os.path.basename(filename).split('.')[0]
    dirname  = os.path.dirname(filename)
    if not dirname == "":
        dirname += '\\'

    newfilename = dirname + basename + "_hu.nim" 
    print(f"Writing to file: {newfilename}")

    with open(newfilename, 'w', encoding="cp850") as f:
        f.write(lines)
        f.write("\n\n# ---------------------------------------- Start generated source code ----------------------------------------------\n\n")
        f.write(all_uniq_fn_calls_str)

    return functions_hits, processed_functions



# ------------------------ main ------------------------

# ToDo: pegs,times (excluded itm because of too many parser errors itm) 
RTLfiles = ['parseutils', 
            'strutils', 
            'parseopt', 
            'parsecfg', 
            'strtabs', 
            'unicode',  
            'ropes',  
            'os', 
            'osproc', 
            'cstrutils',
            'math',
            'browsers',
            '..\\system\\io']

argc = len(sys.argv)

# Option to hand over a single file for debugging
if argc == 2:
    RTLfiles = [ sys.argv[1] ]


for RTLfile in RTLfiles:
    if not os.path.isfile(RTLfile + '.nim'):
        print(f"\n[ERROR] File not found: {RTLfile + '.nim'}")
        print("[ERROR] Are you running this script in '<Nim_install_dir>\\lib\\pure' directory ?")
        exit(0)

for RTLfile in RTLfiles:
    print(f"========================================= Start {RTLfile} ===================================================")
    
    if RTLfile.endswith('.nim'):
        RTLfile = RTLfile[:-4]

    parse_file(RTLfile + '.nim')

    src_file     = RTLfile + '_hu.nim'
    filename_out = RTLfile + '_hu.exe'
    ret = 0
    # save and rename orginal 'os.nim' for compiling 'os_hu.nim'. 
    # 'os.nim' imports other files which check if the parent is os.nim
    if RTLfile == 'os':
        os.rename("os.nim", "os_org.nim")
        os.rename("os_hu.nim", "os.nim")
        src_file     = RTLfile + '.nim'
        ret = built_nim(filename_out, src_file, RTLfile)
        os.rename("os.nim", "os_hu.nim")
        os.rename("os_org.nim", "os.nim")
    else:
        ret = built_nim(filename_out, src_file, RTLfile)

    print(f"========================================= End {RTLfile} ===================================================\n")

    #input("Press Enter to continue...")

with open(MISSED_FUNC_FILENAME, 'w', encoding="cp850") as missed_f:
    missed_f.write("\nMissed Functions:\n")
    missed_f.write("-----------------\n\n")
    for key in skipped_functions:
        missed_f.write(f"\nFile: {key}\n")
        missed_f.write("------------------------------------\n")
        for f in skipped_functions[key]:
            f = ' '.join(f.split()).replace('\n','') + '\n'
            missed_f.write(f)

print(f"\nSuccess rate: (Missed functions can be found in file '.\\{MISSED_FUNC_FILENAME}'')")
for key in success_rate:
    print(key, '->', success_rate[key])

print("\n-----------------------------------------------------------------------------------------------------")
print(f"Done. Now change to nimcache directory 'cd {NIM_CACHE_DIR}' and run 'python {OBJ2PATFILE}'")
print("-----------------------------------------------------------------------------------------------------")

