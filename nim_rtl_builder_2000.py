import sys
import re
import os
import glob
import shutil
import subprocess
import pyparsing as pp
from inspect import currentframe, getframeinfo
from datetime import datetime
from dataclasses import dataclass

from pprint import pprint

# Define filenames depending of your choice and local setup
filename_src    = "mynimfile.nim"
filename_base   = filename_src.rsplit('.', 1)[0]
filename_out    = filename_base + ".exe"
sigmake_dir     = "C:\\tools\\IDA\\flair82\\bin\\win"
sigmake_signame = "Nim-2000-release-opt-speed"
sigmake_bin     = "nim-2000-release-opt-speed.sig"
sigmake_pat     = filename_base + '.pat'
sigmake_exc     = sigmake_bin.rsplit('.', 1)[0] + '.exc'

manual_added_nim_functions_file = 'C:\\tools\\Nim\\src\\git\\dev\\Nim-IDA-FLIRT-Generator\\manual_added_nim_functions.nim'

# Change this if you want to built signature for other compiler flags
#nim_cache_str = f"--nimcache:{NIM_CACHE_DIR}" 
#built_cmd = ["nim", "c", "-d:release", "--opt:size", "-d:ssl"  , "--passC:-ffunction-sections" ,nim_cache_str, f"-o:{filename_out}", filename_src]
#built_cmd = ["nim", "c", "-d:release", "--opt:size", "-d:ssl"  , f"-o:{filename_out}", filename_src]
built_cmd = ["nim", "c", "-d:release", "--opt:speed", "-d:ssl"  , f"-o:{filename_out}", filename_src]

DBG_LEVEL = 1

func_exception_list = []
imported_modules_list = []

debug = 1
var_counter = 0
output = ""

def print_debug(s, level, frameinfo):
    if level <= DBG_LEVEL:
        info = f"(Line: {frameinfo.lineno:04d}): "
        width = 13
        print(f"{info: <{width}}{s}")

def get_args_list(args):
    args = args.replace(";",",")
    arg_list = args.split(",")
    ret_list = []
    #print(f"arg_list = {arg_list}")
    for a in arg_list:
        arg = a.lstrip().rstrip()
        if ':' in arg or '=' in a:
            ret_list.append(arg)
        else:
            idx=arg_list.index(a)
            for x in arg_list[idx+1:]:
                if ':' in x:
                    y = arg + ': ' + x.split(":")[1].lstrip().rstrip()
                    ret_list.append(y)
                    break
    #print(f"ret_list = {ret_list}")
    return ret_list

def parse_file(filename):
    global output
    global imported_modules_list

    funcs_list = []

    with open(filename, 'r', encoding="cp850" ) as f:
        lines = f.read()

    with open(filename, 'r', encoding='cp850') as f:
            for line in f:
                if line.startswith('import '):
                    imported_modules_list.append(line.strip())

    #print(lines)
    func_def_words = pp.oneOf(["proc ", "func "])

    nim_func_def = func_def_words +\
                   pp.Word(pp.alphas)("fn_name") +\
                   pp.Optional('*') +\
                   pp.Optional(pp.Regex(r"\[(.*?)\]")) +\
                   '(' + pp.SkipTo(')') +')' +\
                   pp.Optional(': ' + pp.Optional(pp.SkipTo(pp.Word('{='))))("fn_ret") +\
                   pp.Optional('{' + pp.SkipTo('}')("fn_compiler_opt") + '}') +\
                   pp.restOfLine

    nim_funcs = nim_func_def.searchString(lines)

    all_funcs = []
    for nim_func in nim_funcs:
        f = "".join(nim_func)
        all_funcs.append(f)

    nim_func_def = func_def_words +\
                   pp.Word(pp.alphas)("fn_name") +\
                   pp.Optional(pp.Suppress('*')) +\
                   pp.Optional(pp.Regex(r"\[(.*?)\]"))("fn_gen") +\
                   '(' + pp.SkipTo(')')("fn_para") +')' +\
                   pp.Optional(pp.Suppress(': ') + pp.Optional(pp.SkipTo(pp.Word('{='))))("fn_ret") +\
                   pp.Optional('{' + pp.SkipTo('}')("fn_compiler_opt") + '}') +\
                   pp.restOfLine("fn_rest")

    for func in all_funcs:
        func_dict = {'func_file' : '', 'func_org' : '', 'func_name' : '' , 'func_generic' : '', 'has_generics' : '',  
                            'func_args' : '', 'func_ret' : '',  'has_ret' : False, 'func_copt' : '' , 'func_rest' : '' }

        func = func.replace("\n", "")
        func = " ".join(func.split())
        #print(f"{func} ({filename})")
        parsed_fn = nim_func_def.parseString(func)


        #print(parsed_fn)

        func_dict["func_file"] = filename
        func_dict["func_org" ] = func
        func_dict["func_name"] = parsed_fn['fn_name']

        try:
            func_dict["func_generic"] = parsed_fn['fn_gen']
            func_dict["has_generics"] = True
        except:
            func_dict["has_generics"] = False
            pass

        try:
            args_list = get_args_list(parsed_fn['fn_para'])
            func_dict["func_args"] = args_list
        except:
            pass

        try:
            func_ret = "".join(parsed_fn['fn_ret']).lstrip().rstrip()
            func_dict["func_ret"] = func_ret
            func_dict["has_ret"] = True
        except:
            func_dict["has_ret"] = False
            pass

        try:
            func_copt = "".join(parsed_fn['fn_compiler_opt']).lstrip().rstrip()[1:-1]
            func_dict["func_copt"] = func_copt
        except:
            pass

        try:
            func_rest = "".join(parsed_fn['fn_rest']).lstrip().rstrip()
            func_dict["func_rest"] = func_rest
        except:
            pass

        #if "toOpenArray" in func_dict["func_name"]:
        #    print(f"---> func_dict = {func_dict} <-----")

        excluded_function = ['addFiles', 'newStringTable',  'getValue', 'sendFile', 'body', 'generateHeaders', 'format', 
                             'printToken', 'cmdLineRest', 'remainingArgs', 'ignoreMsg', 'getKeyValPair', 'writeConfig', 
                             'writeConfig', 'nextTry', 'nextTry', 'clear', 'translate', 'translate', 'toTime', 
                             'setLastModificationTime', 'round', 'new', 'arrGet', 'arrPut', 'len', 'len', 'chr', 'add', 'add', 
                             'insert', 'abs', 'addQuitProc', 'isNil', 'isNil', 'find', 'cstringArrayToSeq', 'cstringArrayToSeq', 
                             'deallocCStringArray', 'setControlCHook', 'getStackTrace', 'getDiscriminant', 'selectBranch', 
                             'setCurrentException', 'rawProc', 'rawEnv', 'finished', 'varargsLenImpl', 'draw', 'addSysExitProc', 
                             'addSep', 'execCmdEx', 'contains', 'toOpenArray', 'multiReplace', 'getSectionValue', 'binarySearch', 
                             'high', 'low', 'initSkipTable', 'handleShortOption', 'next', 'rawGetTok', 'getEscapedChar', 'getString', 
                             'getSymbol', 'rawGetTok', 'setSectionKey', 'delSection', 'delSectionKey', 'rawInsert', 'createAllPipeHandles', 
                             'select', 'createFdSet', 'pruneProcessSet', 'pruneProcessSet', 'select', 'cumsum', 'internalNew', 'unsafeNew', 
                             'newSeq', 'setLen', 'del', 'pop', 'delete', 'shallow', 'clamp', 'zeroDefault', 'default', 'fastSubstr',
                             'toLower', 'integerOutOfRangeError', 'rawParseInt', 'rawParseUInt', 'substrEq','split', 'splitWhitespace', 
                             'toHexImpl', 'fromBin', 'fromOct', 'fromHex', 'generateHexCharToValueMap', 'parseEnum', 'align', 'alignLeft',
                             'dedent', 'memmem', 'getPrefix', 'findNormalized', 'invalidFormatString', 'strin', 'addf', 'strip', 'asyncProc',
                             'onProgressChanged', 'contentLength', 'httpError', 'fileError', 'getDefaultSSL', 'parseUri', 'newMultipartData',
                             'getBoundary', 'getNewLocation', 'newHttpClient', 'newAsyncHttpClient', 'reportProgress', 'recvFull', 'parseChunks',
                             'parseBody', 'parseResponse', 'newConnection', 'readFileSizes', 'override', 'requestAux', 'responseContent', 
                             'downloadFileEx', 'parseWord', 'writeHelp', 'writeVersion', 'handleDecChars', 'handleCRLF', 'skip', 'replace',
                             'myhash', 'myCmp', 'mustRehash', 'rawGet', 'enlarge', 'raiseFormatException', 'substr', 'wordToNumber', 'stringHasSep',
                             'newRope', 'initRope', 'initRope', 'splay', 'insertInCache', 'sysctl', 'getApplFreebsd', 'getApplAux', 
                             'getApplOpenBsd', 'getApplHeuristic', 'getApplHaiku', 'GetCurrentProcessId', 'execProcess', 'startProcess',
                             'execProcesses', 'closeHandleCheck', 'fileClose', 'hsClose', 'hsAtEnd', 'hsReadData', 'hsWriteData', 
                             'newFileHandleStream', 'buildCommandLine', 'buildEnv', 'myDup', 'createPipeHandles', 'closeThreadAndProcessHandle',
                             'isExitStatus', 'envToCStringArray', 'startProcessAuxSpawn', 'startProcessAuxFork', 'StartProcessData', 
                             'toLowerAscii', 'startProcessAfterFork', 'startProcessFail', 'waitFor', 'waitForObjects', 'createStream',
                             'csystem', 'jsStartsWith', 'jsEndsWith', 'generateGaussianNoise', 'toBitsImpl', 'jsSetSign', 'truncImpl',
                             'jsRound', 'prepare', 'openDefaultBrowserImplPrep', 'openDefaultBrowserImpl', 'typeof', 'myFoo', 'shallowCopy',
                             'alignof', 'offsetOfDotExpr', 'offsetOf', 'sizeof', 'newSeqOfCap', 'newSeqUninitialized', 'bar', 'ord', 'test',
                             'nimProfile', 'addChar', 'tester', 'handleOOM', 'echo', 'debugEcho', 'nimToCStringConv', 'likelyProc', 'unlikelyProc',
                             'initGC', 'initStackBottom', 'initStackBottomWith', 'zeroMem', 'copyMem', 'moveMem', 'equalMem', 'cmpMem', 
                             'ctrlc', 'nimBorrowCurrentException', 'testLocals', 'procCall', 'strcmp', 'raiseEIO', 'echoBinSafe', 'CFilePtr',
                             'flockfile', 'funlockfile', 'writeWindows', 'arrayWith', 'deepCopy']

        if any(func_dict['func_name'].lower() == ef.lower() for ef in excluded_function): 
            #output += f"# {func_dict['func_file']}: {func_dict['func_org']}\n"
            output += f"# {func_dict['func_org']}\n"
        else:
            funcs_list.append(func_dict)

    return funcs_list


string_types = ["string", "cstring", "WideCString", "NimString", "untyped"]
int_types    = ["cint","cuint32","csize","int","int8","int16","int32","int64","uint","uint8","uint16","uint32","uint64", 
                "Natural", "Positive", "SomeInteger", "SomeNumber", "csize_t", "BiggestInt", "BiggestUInt", 
                "clonglong", "clong", "Ordinal"]
float_types  = [ "float", "float32", "float64","cfloat", "cdouble", "SomeFloat", "BiggestFloat"]

def parse_t(gen):
    t = "[ERROR] wasn't able to split up T generic"
    if gen:
        if ':' in gen:
            t = gen.split(':')[1].lstrip()
            if '|' in t:
                t = t.split('|')[0].lstrip() 
            if t.endswith(']'):
                t = t[:-1]
        # We are replacing an unkown generic Type with int for now
        elif '[T]' in gen:                        
            t = 'int'
    # We are replacing an unkown generic Type with int for now
    else:
        t = 'int'

    return t

def get_type_value(left, right, f):

    global var_counter

    if f['has_generics'] and right.startswith('T'):
        right = parse_t(f['func_generic'])
        #input(f"Generic ({left}) resolved to: {right}")
    #else:
    #    print(f"No generic found: left:{left}  right:{right}")

    if any(right.lower() in t.lower() for t in string_types):
        typeval = "\"talos\""
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif any(right.lower() in t.lower() for t in int_types) or 'not string' in right.lower():
        typeval = "10"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif any(right.lower() in t.lower() for t in float_types):
        typeval = "10.0"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'char'.lower():
        typeval = "'A'"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'Rope'.lower():
        typeval = "\"Hello\".rope()"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'byte'.lower():
        typeval = "byte('a')"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'Rune'.lower():
        typeval = "\"R\".runeAt(0)"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'bool'.lower():
        typeval = "true"
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'AsyncHttpClient'.lower():
        typeval = "newAsyncHttpClient()"
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'File'.lower():
        typeval = "open(\"test.txt\", fmReadWrite)"
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif 'Handle'.lower() in right.lower():
        typeval = "getOsFileHandle(open(\"test.txt\", fmReadWrite))"
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'HttpMethod'.lower():
        typeval =  f"HttpGet"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }    
    elif right.lower() == 'HttpHeaders'.lower():
        typeval =  f"newHttpHeaders()"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }  
    elif right.lower() == 'HttpClient'.lower():
        typeval =  f"newHttpClient()"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }  
    elif right.lower() == 'Response'.lower():
        typeval =  f"Response()"
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval } 
    elif right.lower() == 'Socket'.lower():
        typeval =  f"newSocket()"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'MultipartData'.lower():
        typeval =  f"newMultipartData()"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'MultipartEntries'.lower():
        typeval =  f"newMultipartData().entries"
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'CfgParser'.lower():
        typeval =  f"CfgParser"
        res = { "var_init" : f"var {left}{var_counter} : {typeval}" , "typeval" : typeval }  
    elif right.lower() == 'FileMode'.lower():
        typeval =  f"{right} = fmReadWrite"
        res = { "var_init" : f"var {left}{var_counter}: {typeval}" , "typeval" : typeval }
    elif right.lower() == 'FilePermission'.lower():
        typeval =  f"fpUserExec" 
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval } 
    elif right.lower() == 'CFilePtr'.lower():
        typeval = 'fopen("file.txt", "r")'
        res = { "var_init" : f"var {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'static int'.lower():
        typeval = '10'
        res = { "var_init" : f"let {left}{var_counter}: {right} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'Uri'.lower():
        typeval = 'parseUri("http://www.example.com:80/path?query=param#fragment")'
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'Stream'.lower():
        typeval = 'newFileStream("example.txt", fmRead)'
        res = { "var_init" : f"let {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'StringTableRef'.lower():
        typeval = 'newStringTable()'
        res = { "var_init" : f"var {left}{var_counter} = {typeval}" , "typeval" : typeval }
    elif right.lower() == 'StartProcessData'.lower():
        typeval = 'startProcess("echo")'
        res = { "var_init" : f"let procData{var_counter} = startProcess(\"echo\")" , "typeval" : typeval }
    elif right.lower() == 'Process'.lower():
        typeval = 'startProcess("echo")'
        res = { "var_init" : f"let {left}{var_counter} = startProcess(\"echo\")" , "typeval" : typeval }
    elif right.lower() == 'ObjectWaitInfo'.lower():
        typeval = 'waitFor(sleepAsync(100))'
        res = { "var_init" : f"let waitInfo{var_counter} = waitFor(sleepAsync(100))" , "typeval" : typeval }
    elif right.lower() == 'pointer'.lower():
        typeval = "newString(\"Hallo Welt\")"
        res = { "var_init" : f"var {left}{var_counter} = newString(10)" , "typeval" : typeval }
    elif right.lower().startswith('typedesc'.lower()):
        typeval = "float"
        res = { "var_init" : f"{typeval}" , "typeval" : typeval }
    else:
        res = { "var_init" : "UNKOWN_TYPE_ERROR" , "typeval" : f"UNKOWN_TYPE_ERROR: left:{left} right:{right}" }
        res = { "var_init" : "UNKOWN_TYPE_ERROR" , "typeval" : f"UNKOWN_TYPE_ERROR: right:{right} -- {f['func_org']}" }
        res = { "var_init" : "UNKOWN_TYPE_ERROR" , "typeval" : f"UNKOWN_TYPE_ERROR: right:{right}" }
        res = { "var_init" : "UNKOWN_TYPE_ERROR" , "typeval" : f"UNKOWN_TYPE_ERROR: {f['func_name']}" }
        global func_exception_list
        func_exception_list.append({"org" : f['func_org'], "name" : f['func_name']})

    res["var_left"] = f"{left}{var_counter}"

    var_counter += 1

    return res 

def get_var_syntax(left, right, f):
    global var_counter
    #gt = get_type_value(left, right[4:],f)["typeval"]
    #res = { "var_init" : f"var {left}{var_counter}: = {gt}" }
    res = get_type_value(left, right[4:],f)
    res["var_left"] = f"{left}{var_counter-1}"
    #var_counter += 1
    return res

def get_openarray_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[10:-1],f)["typeval"]
    res = { "var_init" : f"let {left}{var_counter} = [{gt},{gt},{gt}]" }
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def get_uncheckedarray_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[15:-1],f)["typeval"]
    res = { "var_init" : f"let {left}{var_counter} = [{gt},{gt},{gt}]" }
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def get_set_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[4:-1],f)["typeval"]
    res = { "var_init" : f"var {left}{var_counter}: set[{right[4:-1]}] = " + '{' + f"{gt},{gt},{gt}" + '}'}
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def get_ptr_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[4:],f)['var_init']
    print(gt)
    print(var_counter)
    res = { "var_init" : f"{gt}\nvar {left}{var_counter}: ptr {right[4:]} = addr({left}{var_counter-1})" }
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    print(res["var_init"])
    return res

def get_slice_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[6:-1],f)["typeval"]
    res = { "var_init" : f"var {left}{var_counter}: set[{right[4:-1]}] = [{gt},{gt},{gt}]"}
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def get_seq_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[4:-1],f)["typeval"]
    res = { "var_init" : f"var {left}{var_counter} = @[{gt},{gt},{gt}]"}
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def get_varargs_syntax(left, right, f):
    global var_counter
    gt = get_type_value(left, right[8:-1],f)["typeval"]
    res = { "var_init" : f"var {left}{var_counter}: {right[8:-1]} = {gt}"}
    res["var_left"] = f"{left}{var_counter}"
    var_counter += 1
    return res

def translate_arg_colon(arg,f):
    arg_split  = arg.split(":")
    left  = arg_split[0].lstrip().rstrip()
    right = arg_split[1].split("|")[0].lstrip().rstrip()  # drop right side if there are muliple options e.g. 'Uri | string'

    #print(f"left: {left}  right: {right}")
    #print(f"right: {right}")

    if '=' in right:
        #print(f"Default value set. We don't need this argument: {right}")
        #print(f"Org.Function {f['func_file']}  {f['func_org']}")
        s = "DefaultValueDefined"
    else:
        if right.lower().startswith("var "):
            # "var string" argument. Genrated syntax: var myString: cstring = "Talos"
            s = get_var_syntax(left, right, f)
            #print(f"{f['func_file']}  {f['func_org']}")
            #print(f"Generated syntax (var): {s}  --  {f['func_org']}\n")
            #print(f"Generated syntax (var): {s}\n")
        elif right.lower().startswith("openarray"):
            # "openarray" argument. Genrated syntax: let myStrings = ["Hallo", "World"]
            s = get_openarray_syntax(left, right, f)
            #print(f"{f['func_file']}  {f['func_org']}")
            #print(f"Generated syntax (openarray): {s}  --  {f['func_org']}\n")
            #print(f"Generated syntax (openarray): {s}\n")
        elif "uncheckedarray" in right.lower():
            s = get_uncheckedarray_syntax(left, right, f)
            #print(f"Generated syntax (uncheckedarray): {s}\n")
        elif right.lower().startswith("set["):
            s = get_set_syntax(left, right, f)
            #print(f"Generated syntax (set): {s}\n")
        elif right.lower().startswith("slice["):
            s = get_slice_syntax(left, right, f)
            #print(f"Generated syntax (set): {s}\n")
        elif right.lower().startswith("seq["):
            s = get_seq_syntax(left, right, f)
            #print(f"Generated syntax (seq): {s}\n")
        elif right.lower().startswith("varargs["):
            s = get_varargs_syntax(left, right, f)
            #print(f"Generated syntax (varargs): {s}\n")
        elif right.lower().startswith("ptr "):
            s = get_ptr_syntax(left, right, f) 
        else:
            if right.endswith("]") and not right.startswith('typedesc['):
                #right = right[:-1]
                print(f['func_org'])
                print(f"[ERROR] Found unkown keyword: {right}")
                exit(0)
            s = get_type_value(left, right,f)
            #print(f"Generated syntax (default): {s}  --  {f['func_org']}\n")
            #print(f"Generated syntax (default): {s}\n")
    #print(f"ret = {s}")
    return s

def translate_arg(arg,f): 
    if re.match(r"^\w+ *\:", arg):
        # Match lines starting with "variable: ..."
        # print(f"Colon: {arg}")
        s = translate_arg_colon(arg,f)
        # print(f"{s}")
        return s

    elif re.match(r"^\w+ *\=", arg):
        # Match lines starting with "variable= ..."
        # These args have a default value, we are skipping them
        s = 'DefaultValueDefined'
        #print("DefaultValueDefined")
        return s
    else:
        print(f"[ERROR] Found non-expected function argument : {arg}")
        exit(1)

def gen_srccode(func_list):
    global output

    for n,f in enumerate(all_func_list):
        if (debug == 6):
            print(f"{n}. {f['func_file']}  {f['func_org']}")
            print(f"Function name          : {f['func_name']}")
            print(f"Function generics      : {f['func_generic']}")
            for arg in f['func_args']:
                print(f"Function arg           : {arg}")
            print(f"Function returnval     : {f['func_ret']}")
            print(f"Function compiler opts : {f['func_copt']}")
            print()

        gen_args_list = []
        gen_args_init_list = []
        output += f"\n# {f['func_file']}: {f['func_org']}\n"

        for arg in f['func_args']:
            s = translate_arg(arg,f)
            if s == 'DefaultValueDefined':
                continue
            gen_args_list.append(s["var_left"])
            gen_args_init_list.append(s["var_init"])

        for s_var_init in gen_args_init_list:
            output += f"{s_var_init}\n"

        if f["has_ret"] == True:
            output += f"discard {f['func_name']}({','.join(gen_args_list)})\n"
        else:
            output += f"{f['func_name']}({','.join(gen_args_list)})\n"


def build_nim():
    built_cmd_str = " ".join(built_cmd)
    print(f"\nBuilding Nim executable.\nBuild cmd: {built_cmd_str}\n")
    input("Hit return to proceed")
    return_code = subprocess.call(built_cmd)

    if return_code == 0:
        print_debug(f"Command executed successfully.",1,getframeinfo(currentframe()))
    else:
        print_debug(f"Command failed with return code: {return_code}",1,getframeinfo(currentframe()))
        exit(1)

    return return_code


# --------------------------------------------- Main ---------------------------------------------

all_func_list = []

RTLfiles = ['parseutils', 
            'strutils', 
            'httpclient',
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
            '..\\system']

# Parse most Nim runtime library files and extract the functions
output += f"# Excluded Functions (not parsed and generated):\n"
output += f"# ----------------------------------------------\n"

for RTLfile in RTLfiles:
    if not os.path.isfile(RTLfile + '.nim'):
        print(f"\n[ERROR] File not found: {RTLfile + '.nim'}")
        print("[ERROR] Are you running this script in '<Nim_install_dir>\\lib\\pure' directory ?")
        exit(0)

    funcs_list = parse_file(RTLfile + '.nim')
    all_func_list += funcs_list

#for imported in imported_modules_list:
#    print(imported)
#exit(0)

output += f"\n\n# -------------------------- Found and parsed {len(all_func_list)} functions -----------------------------------------\n\n"

for RTLfile in RTLfiles:
    output += f"import {RTLfile}\n"

output += "import uri\n"
output += "import streams\n"
output += "import posix\n"
output += "import bitops, fenv\n"
output += "import os\n"
output += "import parseutils\n"
output += "import std/cmdline\n"
output += "import std/enumutils\n"
output += "import std/envvars\n"
output += "import std/oserrors\n"
output += "import std/private/[since, jsutils]\n"
output += "import std/private/decode_helpers\n"
output += "import std/private/osappdirs\n"
output += "import std/private/oscommon\n"
output += "import std/private/osdirs\n"
output += "import std/private/osfiles\n"
output += "import std/private/ospaths2\n"
output += "import std/private/osseps\n"
output += "import std/private/ossymlinks\n"
output += "import std/private/since\n"
output += "import std/private/strimpl\n"
output += "import std/strbasics\n"
output += "import lexbase, tables\n"
output += "import pathnorm\n"
output += "import system/coro_detection\n"
output += "import system/ctypes\n"
output += "import system/dollars\n"
output += "import system/iterators\n"

gen_srccode(all_func_list)

print(output)

if func_exception_list:
    print("[WARNING] Unparsed functions found:")
    funcnameonly_list = []
    for ef in func_exception_list:
        print(f"{ef['org']}")
        funcnameonly_list.append(ef['name'])

    print()
    print(funcnameonly_list)

# Write generated source code to file
with open(filename_src, 'w', encoding="cp850") as f:
    f.write(output)  

# read manual added Nim functions and code
with open(manual_added_nim_functions_file, 'r', encoding="cp850" ) as f:
        manual_added_nim_functions = f.read()

# add it to our generated source code file
with open(filename_src, 'a+', encoding="cp850") as f:
    f.write(manual_added_nim_functions)  

print("Added manualy generated functions to the source code file.")

# Built executable
build_nim()

print(f"\n") 
print(f"Building {filename_out} done.\n") 
print(f"1. Now load '{filename_out}' into IDA, run the Flare 'Create PAT from the database' (idb2pat) plugin to generate the '{filename_base}.pat' file.\n" )
print(f"2. Open the generated '{filename_base}.pat' file in a text editor and delete the broken 'NimMainModule' signature, because sigmake can't handle it.")
print(f"   This is usually from where the broken 'NimMainModule' signature starts to the second valid 'NimMain' signature.")
print(f"   The broken 'NimMainModule' signature start line number can be found by running the sigmake command below.")
print(f"   This will cause a 'Bad xdigit' error, which includes the line number. Step 2. is only neccessary if you run into the 'Bad xdigit' error\n")
print(f"3. Then run: {sigmake_dir}\\sigmake.exe -n\"{sigmake_signame}\" {sigmake_pat} {sigmake_bin}\n")
print(f"4. If there are collision (there will be), delete the comments (first four lines) in the '{sigmake_exc}' file and re-run the sigmake command\n")
print(f"5. Copy the {sigmake_bin} file over to your IDA signature directory, e.g <IDA-INSTALL-DIR>\\sig\\pc.\n")
print(f"6. Load your Nim malware into IDA and load the generated Nim signature via the 'File/Load File/FLIRT Signature file' menu. Done.")
print(f"\n")


