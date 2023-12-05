

# ------------------------------------------------------------------
# Functions and code which we want to add to the auto-generated code
# This gets appended to the auto-generated file 
# Needs to be compiled with -d:ssl
# ------------------------------------------------------------------

import parseutils
import strutils
import httpclient
import parseopt
import parsecfg
import strtabs
import unicode
import ropes
import os
import json
import osproc
import cstrutils
import math
import browsers
import system
import uri
import streams
import posix
import bitops, fenv
import os
import parseutils
import mimetypes
import asyncdispatch
import std/strtabs
import std/net
import std/cmdline
import std/enumutils
import std/envvars
import std/oserrors
import std/private/[since, jsutils]
import std/private/decode_helpers
import std/private/osappdirs
import std/private/oscommon
import std/private/osdirs
import std/private/osfiles
import std/private/ospaths2
import std/private/osseps
import std/private/ossymlinks
import std/private/since
import std/private/strimpl
import std/times
import std/strbasics
import std/sequtils
import std/asyncdispatch
import lexbase, tables
import pathnorm
import system/coro_detection
import system/ctypes
import system/dollars
import system/iterators
import sugar

# parseutils.nim: proc toLower(c: char): char {.inline.} =
let myNimVarString = "Hello, World!"
echo myNimVarString.toLower()

# parseutils.nim: proc skip*(s, token: openArray[char]): int {.inline.} =
# parseutils.nim: proc fastSubstr(s: openArray[char]; token: var string; length: int)=
# parseutils.nim: proc integerOutOfRangeError(){.noinline.} =
# parseutils.nim: proc rawParseInt(s: openArray[char], b: var BiggestInt): int =
# parseutils.nim: proc rawParseUInt(s: openArray[char], b: var BiggestUInt): int =
# parseutils.nim: func toLowerAscii(c: char): char =
# parseutils.nim: proc skip*(s, token: string, start = 0): int {.inline.} =

var myNimVarDict = newConfig()
myNimVarDict.setSectionKey("","charset", "utf-8")
myNimVarDict.setSectionKey("Package", "name", "hello")
myNimVarDict.setSectionKey("Package", "--threads", "on")
myNimVarDict.setSectionKey("Author", "name", "nim-lang")
myNimVarDict.setSectionKey("Author", "website", "nim-lang.org")
myNimVarDict.writeConfig("my_nim_config.ini")

myNimVarDict = loadConfig("my_nim_config.ini")
let myNimVarCharset = myNimVarDict.getSectionValue("","charset")
let myNimVarThreads = myNimVarDict.getSectionValue("Package","--threads")
let myNimVarPname = myNimVarDict.getSectionValue("Package","name")
let myNimVarName = myNimVarDict.getSectionValue("Author","name")
let myNimVarWebsite = myNimVarDict.getSectionValue("Author","website")
myNimVarDict.setSectionKey("Author", "myNimVarName", "nim-lang")
myNimVarDict.delSectionKey("Author", "myNimVarWebsite")
myNimVarDict.writeConfig("config.ini")

# strutils.nim: func toLowerAscii*(c: char): char {.rtl, extern: "nsuToLowerAsciiChar".} =
# strutils.nim: func toLowerAscii*(s: string): string {.rtl, extern: "nsuToLowerAsciiStr".} =
echo myNimVarString.toLowerAscii()

# strutils.nim: func substrEq(s: string, pos: int, substr: string): bool =
# strutils.nim: func split*(s: string, sep: char, maxsplit: int = -1): seq[string] {.rtl, extern: "nsuSplitChar".} =
# strutils.nim: func split*(s: string, seps: set[char] = Whitespace, maxsplit: int = -1): seq[ string] {.rtl, extern: "nsuSplitCharSet".} =
# strutils.nim: func split*(s: string, sep: string, maxsplit: int = -1): seq[string] {.rtl, extern: "nsuSplitString".} =
let myNimVarString2 = "Nim,is; very-versatile"
let myNimVarWords  = myNimVarString2.split({';', ',', '-'})
for word in myNimVarWords:
    echo word

# strutils.nim: func splitWhitespace*(s: string, maxsplit: int = -1): seq[string] {.rtl, extern: "nsuSplitWhitespace".} =
echo strutils.splitWhitespace("test test test")

# strutils.nim: func toHexImpl(x: BiggestUInt, len: Positive, handleNegative: bool): string =
echo "A".toHex() 

# strutils.nim: func fromBin*[T: SomeInteger](s: string): T =
var myNimVar_s = "0b_0100_1000_1000_1000_1110_1110_1001_1001"
var myNimVar_a = fromBin[int](myNimVar_s)
echo myNimVar_a.toBin(8)

# strutils.nim: func fromOct*[T: SomeInteger](s: string): T =
myNimVar_s = "0o_123_456_777"
myNimVar_a = fromOct[int](myNimVar_s)
echo myNimVar_a

# strutils.nim: func fromHex*[T: SomeInteger](s: string): T =
myNimVar_s = "0x_1235_8df6"
myNimVar_a = fromHex[int](myNimVar_s)
echo myNimVar_a

# strutils.nim: func generateHexCharToValueMap(): string =

# strutils.nim: func parseEnum*[T: enum](s: string): T =
# strutils.nim: func parseEnum*[T: enum](s: string, default: T): T =
type
  myNimVar_MyEnum = enum
    first = "1st",
    second,
    third = "3rd"

echo parseEnum[myNimVar_MyEnum]("1_st")

# strutils.nim: func align*(s: string, count: Natural, padding = ' '): string {.rtl, extern: "nsuAlignString".} =
echo strutils.align("abc", 4)

# strutils.nim: func alignLeft*(s: string, count: Natural, padding = ' '): string =
echo strutils.alignLeft("abc", 4)

# strutils.nim: func dedent*(s: string, count: Natural = indentation(s)): string {.rtl,
let myNimVar_x = """
      Hello
        There
    """.dedent()

echo myNimVar_x

# strutils.nim: func delete*(s: var string, slice: Slice[int])=
# strutils.nim: func delete*(s: var string, first, last: int){.rtl, extern: "nsuDelete", deprecated: "use `delete(s, first..last)`".} =
var myNimVar_a3 = "abracadabra"
myNimVar_a3.delete(4, 5)

# strutils.nim: func addSep*(dest: var string, sep = ", ", startLen: Natural = 0){.inline.} =
var myNimVar_arr = "["
for myNimVar_x2 in items([2, 3, 5, 7, 11]):
  addSep(myNimVar_arr, startLen = len("["))
  add(myNimVar_arr, $myNimVar_x2)
add(myNimVar_arr, "]")
echo myNimVar_arr 

# strutils.nim: func initSkipTable*(a: var SkipTable, sub: string){.rtl, extern: "nsuInitSkipTable".} =
# strutils.nim: func initSkipTable*(sub: string): SkipTable {.noinit, rtl, extern: "nsuInitNewSkipTable".} =

let myNimVar_mainString = "This is a simple Nim example."
let myNimVar_pattern    = "simple"
let myNimVar_skipTable  = initSkipTable(myNimVar_pattern)
var myNimVar_foundPos   = find(myNimVar_skipTable, myNimVar_mainString, myNimVar_pattern )

if myNimVar_foundPos != -1:
    echo "Pattern found at position: ", myNimVar_foundPos
else:
    echo "Pattern not found."

# strutils.nim: func find*(a: SkipTable, s, sub: string, start: Natural = 0, last = -1): int {. rtl, extern: "nsuFindStrA".} =
# strutils.nim: func find*(s: string, sub: char, start: Natural = 0, last = -1): int {.rtl, extern: "nsuFindChar".} =
# strutils.nim: func find*(s: string, chars: set[char], start: Natural = 0, last = -1): int {. rtl, extern: "nsuFindCharSet".} =
# strutils.nim: func find*(s, sub: string, start: Natural = 0, last = -1): int {.rtl, extern: "nsuFindStr".} =
myNimVar_foundPos = find(myNimVar_mainString, "Nim")
if myNimVar_foundPos != -1:
    echo "Pattern found at position: ", myNimVar_foundPos
else:
    echo "Pattern not found."

# strutils.nim: proc memmem(haystack: pointer, haystacklen: csize_t, needle: pointer, needlelen: csize_t): pointer {.importc, header: """#define _GNU_SOURCE#include <string.h>""".}
# strutils.nim: proc memmem(haystack: pointer, haystacklen: csize_t, needle: pointer, needlelen: csize_t): pointer {.importc, header: "#include <string.h>".}
# strutils.nim: func contains*(s, sub: string): bool =
# strutils.nim: func contains*(s: string, chars: set[char]): bool =
echo "Hello".contains("he")

# strutils.nim: func replace*(s, sub: string, by = ""): string {.rtl, extern: "nsuReplaceStr".} =
# strutils.nim: func replace*(s: string, sub, by: char): string {.rtl, extern: "nsuReplaceChar".} =
echo "Hello".replace("He", "Hi")

# strutils.nim: func multiReplace*(s: string, replacements: varargs[(string, string)]): string =
echo "Hello world".multiReplace([("He", "lo")])

# strutils.nim: func getPrefix(exp: int): char =
# strutils.nim: func findNormalized(x: string, inArray: openArray[string]): int =
# strutils.nim: func invalidFormatString(formatstr: string){.noinline.} =
# strutils.nim: func addf*(s: var string, formatstr: string, a: varargs[string, `$`]){.rtl, extern: "nsuAddf".} =
var myNimVar_message3 = "The results are: "
let myNimVar_a4 = 10
let myNimVar_b3 = 20
let myNimVar_sum3 = myNimVar_a4 + myNimVar_b3

# Using addf to append formatted text to 'message'
myNimVar_message3.addf("%d + %d = %d", myNimVar_a4, myNimVar_b3, myNimVar_sum3)

echo myNimVar_message3

# strutils.nim: func format*(formatstr: string, a: varargs[string, `$`]): string {.rtl, extern: "nsuFormatVarargs".} =
echo "$1 eats $2." % ["The cat", "fish"]
echo format("$1 eats $2.", ["The cat", "fish"])
# strutils.nim: func strip*(s: string, leading = true, trailing = true, chars: set[char] = Whitespace): string {.rtl, extern: "nsuStrip".} =


# httpclient.nim: proc asyncProc(): Future[string] {.async.} =
# httpclient.nim: proc onProgressChanged(total, progress, speed: BiggestInt){.async.} =
# httpclient.nim: proc asyncProc(){.async.} =
# httpclient.nim: proc contentLength*(response: Response | AsyncResponse): int =
# httpclient.nim: proc body*(response: Response): string =
# httpclient.nim: proc body*(response: AsyncResponse): Future[string] {.async.} =
# httpclient.nim: proc httpError(msg: string)=
# httpclient.nim: proc fileError(msg: string)=
# httpclient.nim: proc getDefaultSSL(): SslContext =
# httpclient.nim: proc add*(p: MultipartData, name, content: string, filename: string = "", contentType: string = "", useStream = true)=
# httpclient.nim: proc add*(p: MultipartData, xs: MultipartEntries): MultipartData {.discardable.} =
# httpclient.nim: proc newMultipartData*(xs: MultipartEntries): MultipartData =
# httpclient.nim: proc addFiles*(p: MultipartData, xs: openArray[tuple[name, file: string]], mimeDb = newMimetypes(), useStream = true):
# httpclient.nim: proc getBoundary(p: MultipartData): string =
# httpclient.nim: proc sendFile(socket: Socket | AsyncSocket, entry: MultipartEntry){.multisync.} =
# httpclient.nim: proc getNewLocation(lastURL: Uri, headers: HttpHeaders): Uri =
# httpclient.nim: proc generateHeaders(requestUrl: Uri, httpMethod: HttpMethod, headers: HttpHeaders, proxy: Proxy): string =
# httpclient.nim: proc newHttpClient*(userAgent = defUserAgent, maxRedirects = 5, sslContext = getDefaultSSL(), proxy: Proxy = nil,
# httpclient.nim: proc newAsyncHttpClient*(userAgent = defUserAgent, maxRedirects = 5, sslContext = getDefaultSSL(), proxy: Proxy = nil,
# httpclient.nim: proc asyncProc(): Future[string] {.async.} =
# httpclient.nim: proc reportProgress(client: HttpClient | AsyncHttpClient, progress: BiggestInt){.multisync.} =
# httpclient.nim: proc recvFull(client: HttpClient | AsyncHttpClient, size: int, timeout: int, keep: bool): Future[int] {.multisync.} =
# httpclient.nim: proc parseChunks(client: HttpClient | AsyncHttpClient): Future[void] {.multisync.} =
# httpclient.nim: proc parseBody(client: HttpClient | AsyncHttpClient, headers: HttpHeaders, httpVersion: string): Future[void] {.multisync.} =
# httpclient.nim: proc parseResponse(client: HttpClient | AsyncHttpClient, getBody: bool): Future[Response | AsyncResponse] {.multisync.} =
# httpclient.nim: proc newConnection(client: HttpClient | AsyncHttpClient, url: Uri){.multisync.} =
# httpclient.nim: proc readFileSizes(client: HttpClient | AsyncHttpClient, multipart: MultipartData){.multisync.} =
# httpclient.nim: proc format(entry: MultipartEntry, boundary: string): string =
# httpclient.nim: proc format(client: HttpClient | AsyncHttpClient, multipart: MultipartData): Future[seq[string]] {.multisync.} =
# httpclient.nim: proc override(fallback, override: HttpHeaders): HttpHeaders =
# httpclient.nim: proc requestAux(client: HttpClient | AsyncHttpClient, url: Uri, httpMethod: HttpMethod, body = "", headers: HttpHeaders = nil, multipart: MultipartData = nil): Future[Response | AsyncResponse] {.multisync.} =
# httpclient.nim: proc responseContent(resp: Response | AsyncResponse): Future[string] {.multisync.} =
# httpclient.nim: proc delete*(client: HttpClient | AsyncHttpClient, url: Uri | string): Future[Response | AsyncResponse] {.multisync.} =
# httpclient.nim: proc downloadFileEx(client: AsyncHttpClient, url: Uri | string, filename: string): Future[void] {.async.} =
var myNimVar_client = newHttpClient()
try:
  echo myNimVar_client.getContent("http://google.com")
finally:
  myNimVar_client.close()

var myNimVar_client2 = newAsyncHttpClient()
try:
    discard myNimVar_client2.getContent("http://google.com")
finally:
    myNimVar_client2.close()

var myNimVar_data = newMultipartData()
myNimVar_data["output"] = "soap12"
myNimVar_data["uploaded_file"] = ("test.html", "text/html",
  "<html><head></head><body><p>test</p></body></html>")
try:
  echo myNimVar_client.postContent("http://validator.w3.org/check", multipart=myNimVar_data)
finally:
  myNimVar_client.close()

let myNimVar_mimes = newMimetypes()
myNimVar_data.addFiles({"uploaded_file": "test.html"}, mimeDb = myNimVar_mimes)
try:
  echo myNimVar_client.postContent("http://validator.w3.org/check", multipart=myNimVar_data)
finally:
  myNimVar_client.close()

myNimVar_client.headers = newHttpHeaders({ "Content-Type": "application/json" })
let myNimVar_body = %*{
    "myNimVar_data": "some text"
}
try:
  let myNimVar_response = myNimVar_client.request("http://some.api", httpMethod = HttpPost, body = $myNimVar_body)
  echo myNimVar_response.status
finally:
  myNimVar_client.close()

proc onProgressChanged(total, progress, speed: BiggestInt) {.async.} =
  echo("Downloaded ", progress, " of ", total)
  echo("Current rate: ", speed div 1000, "kb/s")

proc asyncProc() {.async.} =
  var myNimVar_client3 = newAsyncHttpClient()
  myNimVar_client3.onProgressChanged = onProgressChanged
  try:
    discard await myNimVar_client3.getContent("http://speedtest-ams2.digitalocean.com/100mb.test")
  finally:
    myNimVar_client3.close()

waitFor asyncProc()

var myNimVar_client3 = newHttpClient(sslContext=newContext(verifyMode=CVerifyPeer))

let myNimVar_myProxy = newProxy("http://myproxy.network", auth="user:password")
let myNimVar_client4 = newHttpClient(proxy = myNimVar_myProxy, timeout = 2, maxRedirects = 0)

var myNimVar_url4 = getEnv("http_proxy")

# parseopt.nim: proc printToken(kind: CmdLineKind, key: string, val: string)=
# parseopt.nim: proc parseWord(s: string, i: int, w: var string, delim: set[char] = {'\t', ' '}): int =
# parseopt.nim: proc handleShortOption(p: var OptParser; cmd: string)=
# parseopt.nim: proc next*(p: var OptParser){.rtl, extern: "npo$1".} =
# parseopt.nim: proc cmdLineRest*(p: OptParser): string {.rtl, extern: "npo$1".} =
# parseopt.nim: proc remainingArgs*(p: OptParser): seq[string] {.rtl, extern: "npo$1".} =
# parseopt.nim: proc writeHelp()= discard
# parseopt.nim: proc writeVersion()= discard
# parseopt.nim: proc writeHelp()= discard
# parseopt.nim: proc writeVersion()= discard
# parsecfg.nim: proc rawGetTok(c: var CfgParser, tok: var Token){.gcsafe.}
# parsecfg.nim: proc handleDecChars(c: var CfgParser, xi: var int)=
# parsecfg.nim: proc getEscapedChar(c: var CfgParser, tok: var Token)=
# parsecfg.nim: proc handleCRLF(c: var CfgParser, pos: int): int =
# parsecfg.nim: proc getString(c: var CfgParser, tok: var Token, rawMode: bool)=
# parsecfg.nim: proc getSymbol(c: var CfgParser, tok: var Token)=
# parsecfg.nim: proc skip(c: var CfgParser)=
# parsecfg.nim: proc rawGetTok(c: var CfgParser, tok: var Token)=
# parsecfg.nim: proc ignoreMsg*(c: CfgParser, e: CfgEvent): string {.rtl, extern: "npc$1".} =
# parsecfg.nim: proc getKeyValPair(c: var CfgParser, kind: CfgEventKind): CfgEvent =
# parsecfg.nim: proc next*(c: var CfgParser): CfgEvent {.rtl, extern: "npc$1".} =
# parsecfg.nim: proc replace(s: string): string =
# parsecfg.nim: proc writeConfig*(myNimVarDict: Config, stream: Stream)=
# parsecfg.nim: proc writeConfig*(myNimVarDict: Config, filename: string)=
# parsecfg.nim: proc getSectionValue*(myNimVarDict: Config, section, key: string, defaultVal = ""): string =
# parsecfg.nim: proc setSectionKey*(myNimVarDict: var Config, section, key, value: string)=
# parsecfg.nim: proc delSection*(myNimVarDict: var Config, section: string)=
# parsecfg.nim: proc delSectionKey*(myNimVarDict: var Config, section, key: string)=

let myNimVar_configFile = "example.ini"
var myNimVar_f = newFileStream(myNimVar_configFile, fmRead)
assert myNimVar_f != nil, "cannot open " & myNimVar_configFile
var myNimVar_p: CfgParser
open(myNimVar_p, myNimVar_f, myNimVar_configFile)
while true:
  var myNimVar_e = next(myNimVar_p)
  case myNimVar_e.kind
  of cfgEof: break
  of cfgSectionStart:   ## a `[section]` has been parsed
    echo "new section: " & myNimVar_e.section
  of cfgKeyValuePair:
    echo "key-value-pair: " & myNimVar_e.key & ": " & myNimVar_e.value
  of cfgOption:
    echo "command: " & myNimVar_e.key & ": " & myNimVar_e.value
  of cfgError:
    echo myNimVar_e.msg
close(myNimVar_p)

var myNimVar_dict5 = newConfig()
myNimVar_dict5.setSectionKey("","charset", "utf-8")
myNimVar_dict5.setSectionKey("Package", "name", "hello")
myNimVar_dict5.setSectionKey("Package", "--threads", "on")
myNimVar_dict5.setSectionKey("Author", "name", "nim-lang")
myNimVar_dict5.setSectionKey("Author", "website", "nim-lang.org")
assert $myNimVar_dict5 == """
charset=utf-8
[Package]
name=hello
--threads:on
[Author]
name=nim-lang
website=nim-lang.org
"""

let myNimVar_dict7 = loadConfig("config.ini")
let myNimVar_charset7 = myNimVar_dict7.getSectionValue("","charset")
let myNimVar_threads7 = myNimVar_dict7.getSectionValue("Package","--threads")
let myNimVar_pname7 = myNimVar_dict7.getSectionValue("Package","name")
let myNimVar_name7 = myNimVar_dict7.getSectionValue("Author","name")
let myNimVar_website7 = myNimVar_dict7.getSectionValue("Author","website")
echo myNimVar_pname & "\n" & myNimVar_name & "\n" & myNimVar_website

var myNimVar_dict8 = loadConfig("config.ini")
myNimVar_dict8.setSectionKey("Author", "name", "nim-lang")
myNimVar_dict8.delSectionKey("Author", "website")
myNimVar_dict8.writeConfig("config.ini")

# strtabs.nim: proc myhash(t: StringTableRef, key: string): Hash =
# strtabs.nim: proc myCmp(t: StringTableRef, a, b: string): bool =
# strtabs.nim: proc mustRehash(length, counter: int): bool =
# strtabs.nim: proc nextTry(h, maxHash: Hash): Hash {.inline.} =
# strtabs.nim: proc rawGet(t: StringTableRef, key: string): int =
# strtabs.nim: proc len*(t: StringTableRef): int {.rtlFunc, extern: "nst$1".} =
# strtabs.nim: proc contains*(t: StringTableRef, key: string): bool =
# strtabs.nim: proc rawInsert(t: StringTableRef, data: var KeyValuePairSeq, key, val: string)=
# strtabs.nim: proc enlarge(t: StringTableRef)=
# strtabs.nim: proc newStringTable*(mode: StringTableMode): owned(StringTableRef) {. rtlFunc, extern: "nst$1", noSideEffect.} =
# strtabs.nim: proc newStringTable*(keyValuePairs: varargs[string], mode: StringTableMode): owned(StringTableRef) {. rtlFunc, extern: "nst$1WithPairs", noSideEffect.} =
# strtabs.nim: proc newStringTable*(keyValuePairs: varargs[tuple[key, val: string]], mode: StringTableMode = modeCaseSensitive): owned(StringTableRef) {. rtlFunc, extern: "nst$1WithTableConstr", noSideEffect.} =
# strtabs.nim: proc raiseFormatException(s: string)=
# strtabs.nim: proc getValue(t: StringTableRef, flags: set[FormatFlag], key: string): string =
# strtabs.nim: proc clear*(s: StringTableRef, mode: StringTableMode){. rtlFunc, extern: "nst$1".} =
# strtabs.nim: proc clear*(s: StringTableRef){.since: (1, 1).} =
# strtabs.nim: proc del*(t: StringTableRef, key: string)=
var myNimVar_t8 = newStringTable()
myNimVar_t8["name"] = "John"
myNimVar_t8["city"] = "Monaco"
echo myNimVar_t8.len()
echo myNimVar_t8.contains("test")
echo myNimVar_t8["name"]

# unicode.nim: proc substr(s: openArray[char] , first, last: int): string =
# unicode.nim: proc add*(s: var string; c: Rune)=
# unicode.nim: proc binarySearch(c: RuneImpl, tab: openArray[int], len, stride: int): int =
# unicode.nim: proc toLower*(c: Rune): Rune {.rtl, extern: "nuc$1".} =
# unicode.nim: proc toLower*(s: openArray[char]): string {.noSideEffect, rtl, extern: "nuc$1Str".} =
# unicode.nim: proc translate*(s: openArray[char], replacements: proc(key: string): string): string {. rtl, extern: "nuc$1", effectsOf: replacements.} =
# unicode.nim: proc wordToNumber(s: string): string =
# unicode.nim: proc stringHasSep(s: openArray[char], index: int, seps: openArray[Rune]): bool =
# unicode.nim: proc stringHasSep(s: openArray[char], index: int, sep: Rune): bool =
# unicode.nim: proc splitWhitespace*(s: openArray[char]): seq[string] {.noSideEffect, rtl, extern: "ncuSplitWhitespace".} =
# unicode.nim: proc split*(s: openArray[char], seps: openArray[Rune] = unicodeSpaces, maxsplit: int = -1):
# unicode.nim: proc split*(s: openArray[char], sep: Rune, maxsplit: int = -1): seq[string] {.noSideEffect, rtl, extern: "nucSplitRune".} =
# unicode.nim: proc strip*(s: openArray[char], leading = true, trailing = true, runes: openArray[Rune] = unicodeSpaces): string {.noSideEffect, rtl, extern: "nucStrip".} =
# unicode.nim: proc align*(s: openArray[char], count: Natural, padding = ' '.Rune): string {. noSideEffect, rtl, extern: "nucAlignString".} =
# unicode.nim: proc alignLeft*(s: openArray[char], count: Natural, padding = ' '.Rune): string {. noSideEffect.} =
# unicode.nim: proc toLower*(s: string): string {.noSideEffect, inline.} =
# unicode.nim: proc translate*(s: string, replacements: proc(key: string): string): string {.effectsOf: replacements, inline.} =
# unicode.nim: proc wordToNumber(s: string): string =
# unicode.nim: proc splitWhitespace*(s: string): seq[string] {.noSideEffect, inline.}=
# unicode.nim: proc split*(s: string, seps: openArray[Rune] = unicodeSpaces, maxsplit: int = -1):
# unicode.nim: proc split*(s: string, sep: Rune, maxsplit: int = -1): seq[string] {.noSideEffect, inline.} =
# unicode.nim: proc strip*(s: string, leading = true, trailing = true, runes: openArray[Rune] = unicodeSpaces): string {.noSideEffect, inline.} =
# unicode.nim: proc align*(s: string, count: Natural, padding = ' '.Rune): string {.noSideEffect, inline.} =
# unicode.nim: proc alignLeft*(s: string, count: Natural, padding = ' '.Rune): string {.noSideEffect, inline.} =
var myNimVar_someString = "öÑ"
var myNimVar_someRunes = toRunes(myNimVar_someString)
echo $myNimVar_someRunes == myNimVar_someString
let
  myNimVar_a44 = "ú".runeAt(0)
  myNimVar_b44 = "ü".runeAt(0)
doAssert myNimVar_a44 <% myNimVar_b44

let myNimVar_s5 = "Hänsel  ««: 10,00€"
doAssert(runeSubStr(myNimVar_s5, 0, 2) == "Hä")

var myNimVar_s2 = "abc"
let myNimVar_c2 = "ä".runeAt(0)
myNimVar_s2.add(myNimVar_c2)
doAssert myNimVar_s2 == "abcä"

let myNimVar_a10 = "\táñyóng   "
doAssert unicode.strip(myNimVar_a10) == "áñyóng"
echo unicode.strip(myNimVar_a10) 

let myNimVar_a11 = toRunes "aá"
doAssert size(myNimVar_a11[0]) == 1

doAssert capitalize("βeta") == "Βeta"
let myNimVar_a7 = "añyóng"
doAssert myNimVar_a7.graphemeLen(1) == 2
let myNimVar_a8 = "ñ".runeAt(0)
doAssert myNimVar_a8.repeat(5) == "ñññññ"
assert reversed("Reverse this!") == "!siht esreveR"

let myNimVar_a9 = "añyóng"
doAssert myNimVar_a9.runeLen == 6
doAssert myNimVar_a9.runeLenAt(0) == 1
doAssert myNimVar_a9.runeOffset(1) == 1

assert unicode.align("abc", 4) == " abc"
assert unicode.alignLeft("abc", 4) == "abc "
doAssert unicode.capitalize("βeta") == "Βeta"
echo "ä".runeAt(0).islower() 
echo "ä".runeAt(0).isAlpha() 
echo "ä".runeAt(0).isTitle() 
echo "ä".runeAt(0).isWhiteSpace() 
echo "ä".runeAt(0).isCombining() 
echo "ä".runeAt(0).isUpper()

doAssert swapCase("Αlpha Βeta Γamma") == "αLPHA βETA γAMMA"
doAssert title("αlpha βeta γamma") == "Αlpha Βeta Γamma"
doAssert toLower("ABΓ") == "abγ"
doAssert toUpper("abγ") == "ABΓ"
let myNimVar_a13 = "añyóng"
doAssert myNimVar_a13.runeAt(1).toUTF8 == "ñ"

let myNimVar_a12 = toRunes("aáä")
doAssert myNimVar_a12 == @["a".runeAt(0), "á".runeAt(0), "ä".runeAt(0)]

proc wordToNumber(s: string): string =
  case s
  of "one": "1"
  of "two": "2"
  else: s
let myNimVar_a14 = "one two three four"
doAssert myNimVar_a14.translate(wordToNumber) == "1 2 three four"

assert toSeq(unicode.split("hÃllo\lthis\lis an\texample\l是")) ==
  @["hÃllo", "this", "is", "an", "example", "是"]

# ropes.nim: proc len*(a: Rope): int {.rtl, extern: "nro$1".} =
# ropes.nim: proc newRope(): Rope = new(result)
# ropes.nim: proc newRope(data: string): Rope =
# ropes.nim: proc splay(s: string, tree: Rope, cmpres: var int): Rope =
# ropes.nim: proc insertInCache(s: string, tree: Rope): Rope =
# ropes.nim: proc add*(a: var Rope, b: Rope){.rtl, extern: "nro$1Rope".} =
# ropes.nim: proc add*(a: var Rope, b: string){.rtl, extern: "nro$1Str".} =
# ropes.nim: proc addf*(c: var Rope, frmt: string, args: openArray[Rope]){.rtl, extern: "nro$1".} =

let myNimVar_r1 = "$1 $2 $3" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $myNimVar_r1 == "Nim is a great language"

let myNimVar_r2 = "$# $# $#" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $myNimVar_r2 == "Nim is a great language"

let myNimVar_r3 = "${1} ${2} ${3}" % [rope("Nim"), rope("is"), rope("a great language")]
doAssert $myNimVar_r3 == "Nim is a great language"

# os.nim: proc toTime(ts: Timespec): times.Time {.inline.} =

# os.nim: proc sysctl(name: ptr cint, namelen: cuint, oldp: pointer, oldplen: ptr csize_t, newp: pointer, newplen: csize_t): cint {.importc: "sysctl",header: """#include <sys/types.h> #include <sys/sysctl.h>""".}
# os.nim: proc getApplFreebsd(): string =
# os.nim: proc getApplAux(procPath: string): string =
# os.nim: proc getApplOpenBsd(): string =
# os.nim: proc getApplHeuristic(): string =
# os.nim: proc getApplHaiku(): string =
# os.nim: proc getCurrentProcessId*(): int {.noWeirdTarget.} =
var myNimVar_p11 = getCurrentProcessId()
# os.nim: proc GetCurrentProcessId(): DWORD {.stdcall, dynlib: "kernel32", importc: "GetCurrentProcessId".}
# os.nim: proc setLastModificationTime*(file: string, t: times.Time){.noWeirdTarget.} =
setLastModificationTime("test.txt", getTime())

# osproc.nim: proc execProcess*(command: string, workingDir: string = "", args: openArray[string] = [], env: StringTableRef = nil, options: set[ProcessOption] = {poStdErrToStdOut, poUsePath, poEvalCommand}):
let myNimVar_outp_shell = execProcess("nim c -r mytestfile.nim")

# osproc.nim: proc startProcess*(command: string, workingDir: string = "", args: openArray[string] = [], env: StringTableRef = nil, options: set[ProcessOption] = {poStdErrToStdOut}):
let myNimVar_outp_shell2 = startProcess("nim c -r mytestfile.nim")

# osproc.nim: proc execProcesses*(cmds: openArray[string], options = {poStdErrToStdOut, poParentStreams}, n = countProcessors(),
let myNimVar_outp_shell3 = execProcesses(["mytestfile.exe"])

# osproc.nim: proc hsClose(s: Stream)=
# osproc.nim: proc hsAtEnd(s: Stream): bool = return FileHandleStream(s).atTheEnd
# osproc.nim: proc hsReadData(s: Stream, buffer: pointer, bufLen: int): int =
# osproc.nim: proc hsWriteData(s: Stream, buffer: pointer, bufLen: int)=
# osproc.nim: proc newFileHandleStream(handle: Handle): owned FileHandleStream =
# osproc.nim: proc buildCommandLine(a: string, args: openArray[string]): string =
# osproc.nim: proc buildEnv(env: StringTableRef): tuple[str: cstring, len: int] =
# osproc.nim: proc myDup(h: Handle; inherit: WINBOOL = 1): Handle =
# osproc.nim: proc createAllPipeHandles(si: var STARTUPINFO; stdin, stdout, stderr: var Handle; hash: int)=
# osproc.nim: proc createPipeHandles(rdHandle, wrHandle: var Handle)=
# osproc.nim: proc startProcess(command: string, workingDir: string = "", args: openArray[string] = [], env: StringTableRef = nil, options: set[ProcessOption] = {poStdErrToStdOut}):
# osproc.nim: proc closeThreadAndProcessHandle(p: Process)=
# osproc.nim: proc select(readfds: var seq[Process], timeout = 500): int =
# osproc.nim: proc isExitStatus(status: cint): bool =
# osproc.nim: proc envToCStringArray(t: StringTableRef): cstringArray =
# osproc.nim: proc envToCStringArray(): cstringArray =
# osproc.nim: proc startProcessAuxSpawn(data: StartProcessData): Pid {. raises: [OSError], tags: [ExecIOEffect, ReadEnvEffect, ReadDirEffect, RootEffect], gcsafe.}
# osproc.nim: proc startProcessAuxFork(data: StartProcessData): Pid {. raises: [OSError], tags: [ExecIOEffect, ReadEnvEffect, ReadDirEffect, RootEffect], gcsafe.}
# osproc.nim: proc startProcessAfterFork(data: ptr StartProcessData){. raises: [OSError], tags: [ExecIOEffect, ReadEnvEffect, ReadDirEffect, RootEffect], cdecl, gcsafe.}
# osproc.nim: proc startProcess(command: string, workingDir: string = "", args: openArray[string] = [], env: StringTableRef = nil, options: set[ProcessOption] = {poStdErrToStdOut}):
# osproc.nim: proc startProcessAuxSpawn(data: StartProcessData): Pid =
# osproc.nim: proc startProcessAuxFork(data: StartProcessData): Pid =
# osproc.nim: proc startProcessFail(data: ptr StartProcessData)=
# osproc.nim: proc startProcessAfterFork(data: ptr StartProcessData)=
# osproc.nim: proc waitForObjects(infos: ptr ObjectWaitInfo, numInfos: cint, flags: uint32, timeout: int64): clong {.importc: "wait_for_objects_etc", header: "OS.h".}
# osproc.nim: proc createStream(handle: var FileHandle, fileMode: FileMode): owned FileStream =
# osproc.nim: proc csystem(cmd: cstring): cint {.nodecl, importc: "system", header: "<stdlib.h>".}
# osproc.nim: proc createFdSet(fd: var TFdSet, s: seq[Process], m: var int)=
# osproc.nim: proc pruneProcessSet(s: var seq[Process], fd: var TFdSet)=
# osproc.nim: proc select(readfds: var seq[Process], timeout = 500): int =
# osproc.nim: proc execCmdEx*(command: string, options: set[ProcessOption] = { poStdErrToStdOut, poUsePath}, env: StringTableRef = nil, workingDir = "", input = ""): tuple[ output: string, exitCode: int] {.raises: [OSError, IOError], tags: [ExecIOEffect, ReadIOEffect, RootEffect], gcsafe.} =
let myNimVar_errC = execCmd("nim c -r mytestfile.nim")
var myNimVar_result3 = execCmdEx("nim r --hints:off -", options = {}, input = "echo 3*4")

# cstrutils.nim: func jsStartsWith(s, prefix: cstring): bool {.importjs: "#.startsWith(#)".}
# cstrutils.nim: func jsEndsWith(s, suffix: cstring): bool {.importjs: "#.endsWith(#)".}
# math.nim: proc generateGaussianNoise(mu: float = 0.0, sigma: float = 1.0): (float, float) =
# math.nim: proc toBitsImpl(x: float): array[2, uint32] =
# math.nim: proc jsSetSign(x: float, sgn: bool): float =
# math.nim: func truncImpl(f: float64): float64 =
# math.nim: func truncImpl(f: float32): float32 =
# math.nim: func round*[T: float32|float64](x: T): T =
# math.nim: func round*(x: float32): float32 {.importc: "roundf", header: "<math.h>".}
# math.nim: func round*(x: float64): float64 {.importc: "round", header: "<math.h>".} =
# math.nim: func round*(x: float): float {.importc: "Math.round", nodecl.}
# math.nim: func jsRound(x: float): float {.importc: "Math.round", nodecl.}
# math.nim: func round*[T: float64 | float32](x: T): T =
# math.nim: func round*[T: float32|float64](x: T, places: int): T =
doAssert round(3.4) == 3.0
# math.nim: func cumsum*[T](x: var openArray[T])=
var myNimVar_a15 = [1, 2, 3, 4]
cumsum(myNimVar_a15)

# math.nim: func clamp*[T](val: T, bounds: Slice[T]): T {.since: (1, 5), inline.} =
assert clamp(10, 1 .. 5) == 5

# browsers.nim: proc prepare(s: string): string =
# browsers.nim: proc openDefaultBrowserImplPrep(url: string)=
# browsers.nim: proc openDefaultBrowserImpl(url: string)=
openDefaultBrowser("https://nim-lang.org")

# ..\system.nim: func zeroDefault*[T](_: typedesc[T]): T {.magic: "ZeroDefault".} =
assert (int, float).default == (0, 0.0)
assert (int, float).zeroDefault == (0, 0.0)

# ..\system.nim: proc typeof*(x: untyped; mode = typeOfIter): typedesc {. magic: "TypeOf", noSideEffect, compileTime.} =
echo typeof(int)

# ..\system.nim: proc myFoo(): float = 0.0
# ..\system.nim: proc internalNew*[T](a: var ref T){.magic: "New", noSideEffect.}
# ..\system.nim: proc new*[T](a: var ref T, finalizer: proc (x: ref T){.nimcall.}) {.
var myNimVar_a16 = new(int)

# ..\system.nim: proc high*[T: Ordinal|enum|range](x: T): T {.magic: "High", noSideEffect, deprecated: "Deprecated since v1.4; there should not be `high(value)`. Use `high(type)`.".}
# ..\system.nim: proc high*[T: Ordinal|enum|range](x: typedesc[T]): T {.magic: "High", noSideEffect.}
# ..\system.nim: proc high*[T](x: openArray[T]): int {.magic: "High", noSideEffect.}
# ..\system.nim: proc high*[I, T](x: array[I, T]): I {.magic: "High", noSideEffect.}
# ..\system.nim: proc high*[I, T](x: typedesc[array[I, T]]): I {.magic: "High", noSideEffect.}
# ..\system.nim: proc high*(x: cstring): int {.magic: "High", noSideEffect.}
# ..\system.nim: proc high*(x: string): int {.magic: "High", noSideEffect.}
var myNimVar_a17 = "test".high
# ..\system.nim: proc low*[T: Ordinal|enum|range](x: T): T {.magic: "Low", noSideEffect, deprecated: "Deprecated since v1.4; there should not be `low(value)`. Use `low(type)`.".}
# ..\system.nim: proc low*[T: Ordinal|enum|range](x: typedesc[T]): T {.magic: "Low", noSideEffect.}
# ..\system.nim: proc low*[T](x: openArray[T]): int {.magic: "Low", noSideEffect.}
# ..\system.nim: proc low*[I, T](x: array[I, T]): I {.magic: "Low", noSideEffect.}
# ..\system.nim: proc low*[I, T](x: typedesc[array[I, T]]): I {.magic: "Low", noSideEffect.}
# ..\system.nim: proc low*(x: cstring): int {.magic: "Low", noSideEffect.}
# ..\system.nim: proc low*(x: string): int {.magic: "Low", noSideEffect.}
var myNimVar_a18 = "test".low
# ..\system.nim: proc shallowCopy*[T](x: var T, y: T){.noSideEffect, magic: "ShallowCopy".}
# ..\system.nim: proc arrGet[I: Ordinal;T](a: T; i: I): T {. noSideEffect, magic: "ArrGet".}
# ..\system.nim: proc arrPut[I: Ordinal;T,S](a: T; i: I; x: S){.noSideEffect, magic: "ArrPut".}
# ..\system.nim: proc unsafeNew*[T](a: var ref T, size: Natural){.magic: "New", noSideEffect.}
type
  myNimVar_Obj = object
    b: bool
    a: UncheckedArray[byte]

var myNimVar_o: ref myNimVar_Obj
unsafeNew(myNimVar_o, sizeof(myNimVar_Obj) + 512)
zeroMem(addr myNimVar_o.a, 512)

# ..\system.nim: proc sizeof*[T](x: T): int {.magic: "SizeOf", noSideEffect.}
echo sizeof(int)

# ..\system.nim: proc alignof*[T](x: T): int {.magic: "AlignOf", noSideEffect.}
# ..\system.nim: proc alignof*(x: typedesc): int {.magic: "AlignOf", noSideEffect.}
echo alignof(int)

# ..\system.nim: proc offsetOfDotExpr(typeAccess: typed): int {.magic: "OffsetOf", noSideEffect, compileTime.}
# ..\system.nim: proc offsetOf*(memberaccess: typed): int {.magic: "OffsetOf", noSideEffect.}
# ..\system.nim: proc sizeof*(x: typedesc): int {.magic: "SizeOf", noSideEffect.}
# ..\system.nim: proc newSeq*[T](s: var seq[T], len: Natural){.magic: "NewSeq", noSideEffect.}
# ..\system.nim: proc newSeq*[T](len = 0.Natural): seq[T] =
var myNimVar_inputStrings3 = newSeq[string](3)
# ..\system.nim: proc newSeqOfCap*[T](cap: Natural): seq[T] {. magic: "NewSeqOfCap", noSideEffect.} =
var myNimVar_x11 = newSeqOfCap[int](5)
# ..\system.nim: proc newSeqUninitialized*[T: SomeNumber](len: Natural): seq[T] =
var myNimVar_inputStrings4 = newSeqUninitialized[int](3)
# ..\system.nim: func len*[TOpenArray: openArray|varargs](x: TOpenArray): int {.magic: "LengthOpenArray".} =
echo len("test")
# ..\system.nim: proc bar[T](a: openArray[T]): int = len(a)
# ..\system.nim: func len*(x: string): int {.magic: "LengthStr".} =
# ..\system.nim: proc len*(x: cstring): int {.magic: "LengthStr", noSideEffect.} =
# ..\system.nim: func len*(x: (type array)|array): int {.magic: "LengthArray".} =
# ..\system.nim: func len*[T](x: seq[T]): int {.magic: "LengthSeq".} =
# ..\system.nim: func ord*[T: Ordinal|enum](x: T): int {.magic: "Ord".} =
assert ord('A') == 65
# ..\system.nim: func chr*(u: range[0..255]): char {.magic: "Chr".} =
doAssert chr(65) == 'A'
# ..\system.nim: proc contains*[U, V, W](s: HSlice[U, V], value: W): bool {.noSideEffect, inline.} =
var myNimVar_s13: set[range['a'..'z']] = {'a'..'c'}
assert myNimVar_s13.contains('c')

# ..\system.nim: proc test[T](a: T): int =
# ..\system.nim: proc new*[T](a: var owned(ref T)) {.magic: "New", noSideEffect.}
# ..\system.nim: proc new*(t: typedesc): auto =
# ..\system.nim: proc new*[T](a: var ref T){.magic: "New", noSideEffect.}
# ..\system.nim: proc new*(t: typedesc): auto =
# ..\system.nim: proc default*[T](_: typedesc[T]): T {.magic: "Default", noSideEffect.} =
# ..\system.nim: proc setLen*[T](s: var seq[T], newlen: Natural){. magic: "SetLengthSeq", noSideEffect.}
# ..\system.nim: proc setLen*(s: var string, newlen: Natural){. magic: "SetLengthStr", noSideEffect.}
var myNimVar_x14 = @[10, 20]
myNimVar_x14.setLen(5)
# ..\system.nim: proc add*(x: var string, y: char){.magic: "AppendStrCh", noSideEffect.}
# ..\system.nim: proc add*(x: var string, y: string){.magic: "AppendStrStr", noSideEffect.} =
var myNimVar_tmp3 = ""
myNimVar_tmp3.add('a')
# ..\system.nim: proc nimProfile(){.compilerproc, noinline.}
# ..\system.nim: proc align(address, alignment: int): int =
# ..\system.nim: proc addChar(s: NimString, c: char): NimString {.compilerproc, benign.}
# ..\system.nim: proc add*[T](x: var seq[T], y: sink T){.magic: "AppendSeqElem", noSideEffect.}
# ..\system.nim: proc add*[T](x: var seq[T], y: sink openArray[T]){.noSideEffect.} =
# ..\system.nim: proc add*[T](x: var seq[T], y: openArray[T]){.noSideEffect.} =
var myNimVar_tmp3_a15 = @[10, 11, 12, 13, 14]
myNimVar_tmp3_a15.add(3)
# ..\system.nim: proc del*[T](x: var seq[T], i: Natural){.noSideEffect.} =
myNimVar_tmp3_a15.del(2)

# ..\system.nim: proc insert*[T](x: var seq[T], item: sink T, i = 0.Natural){.noSideEffect.} =
var myNimVar_a28 = "abc"
myNimVar_a28.insert("zz", 0)

# ..\system.nim: proc high*(T: typedesc[SomeFloat]): T = Inf
echo high(4)
# ..\system.nim: proc low*(T: typedesc[SomeFloat]): T = NegInf
echo low(4)
# ..\system.nim: proc abs*[T: float64 | float32](x: T): T {.noSideEffect, inline.} =
# ..\system.nim: func abs*(x: int): int {.magic: "AbsI", inline.} =
# ..\system.nim: func abs*(x: int8): int8 {.magic: "AbsI", inline.} =
# ..\system.nim: func abs*(x: int16): int16 {.magic: "AbsI", inline.} =
# ..\system.nim: func abs*(x: int32): int32 {.magic: "AbsI", inline.} =
# ..\system.nim: func abs*(x: int64): int64 {.magic: "AbsI", inline.} =
echo abs(4)

# ..\system.nim: proc addQuitProc*(quitProc: proc(){.noconv.}) {.
proc stopLog {.noconv.} =
    echo "Bye"

addQuitProc stopLog

# ..\system.nim: proc len*[U: Ordinal; V: Ordinal](x: HSlice[U, V]): int {.noSideEffect, inline.} =
# ..\system.nim: proc isNil*[T](x: ref T): bool {.noSideEffect, magic: "IsNil".}
# ..\system.nim: proc isNil*[T](x: ptr T): bool {.noSideEffect, magic: "IsNil".}
# ..\system.nim: proc isNil*(x: pointer): bool {.noSideEffect, magic: "IsNil".}
# ..\system.nim: proc isNil*(x: cstring): bool {.noSideEffect, magic: "IsNil".}
# ..\system.nim: proc isNil*[T: proc | iterator {.closure.}](x: T): bool {.noSideEffect, magic: "IsNil".}
# ..\system.nim: proc tester(pos: int): int =
# ..\system.nim: proc find*[T, S](a: T, item: S): int {.inline.}=
var myNimVar_str12 = "Hello World!"
echo myNimVar_str12.find("World")

# ..\system.nim: proc contains*[T](a: openArray[T], item: T): bool {.inline.}=
echo myNimVar_str12.contains("World")

# ..\system.nim: proc pop*[T](s: var seq[T]): T {.inline, noSideEffect.} =
var myNimVar_a23 = @[1, 3, 5, 7]
let myNimVar_a24 = pop(myNimVar_a23)

# ..\system.nim: proc handleOOM()=
# ..\system.nim: proc add*(x: var string, y: cstring){.asmNoStackFrame.} =
# ..\system.nim: proc add*(x: var cstring, y: cstring){.magic: "AppendStrStr".} =
# ..\system.nim: proc add*(x: var string, y: cstring)=
add(myNimVar_str12, "xxx")
# ..\system.nim: proc echo*(x: varargs[typed, `$`]){.magic: "Echo", benign, sideEffect.}
echo "Hello"
# ..\system.nim: proc debugEcho*(x: varargs[typed, `$`]){.magic: "Echo", noSideEffect, tags: [], raises: [].}
debugEcho("Hello")
# ..\system.nim: proc nimToCStringConv(s: NimString): cstring {.compilerproc, inline.} =
# ..\system.nim: proc likelyProc(val: bool): bool {.importc: "NIM_LIKELY", nodecl, noSideEffect.}
# ..\system.nim: proc unlikelyProc(val: bool): bool {.importc: "NIM_UNLIKELY", nodecl, noSideEffect.}
# ..\system.nim: proc delete*[T](x: var seq[T], i: Natural){.noSideEffect, auditDelete.} =
myNimVar_a23.delete(2)

# ..\system.nim: proc initGC(){.gcsafe, raises: [].}
# ..\system.nim: proc initStackBottom(){.inline, compilerproc.} =
# ..\system.nim: proc initStackBottomWith(locals: pointer){.inline, compilerproc.} =
# ..\system.nim: proc zeroMem(p: pointer, size: Natural)=
zeroMem(addr myNimVar_str12, 2)

# ..\system.nim: proc copyMem(dest, source: pointer, size: Natural)=
copyMem(addr myNimVar_str12, addr myNimVar_str12, 2)

# ..\system.nim: proc moveMem(dest, source: pointer, size: Natural)=
moveMem(addr myNimVar_str12, addr myNimVar_str12, 2)

# ..\system.nim: proc equalMem(a, b: pointer, size: Natural): bool =
discard equalMem(addr myNimVar_str12, addr myNimVar_str12, 2)

# ..\system.nim: proc cmpMem(a, b: pointer, size: Natural): int =
discard cmpMem(addr myNimVar_str12, addr myNimVar_str12, 2)

# ..\system.nim: proc cstringArrayToSeq*(a: cstringArray, len: Natural): seq[string] =
# ..\system.nim: proc cstringArrayToSeq*(a: cstringArray): seq[string] =

var cstrarray = allocCStringArray(["bar"])
var seqrarray = cstringArrayToSeq(cstrarray)
# ..\system.nim: proc deallocCStringArray*(a: cstringArray)=
deallocCStringArray(cstrarray)

# ..\system.nim: proc setControlCHook*(hook: proc (){.noconv.})
# ..\system.nim: proc ctrlc(){.noconv.} =
# ..\system.nim: proc getStackTrace*(): string {.gcsafe.}
# ..\system.nim: proc getStackTrace*(e: ref Exception): string {.gcsafe.}
# ..\system.nim: proc getDiscriminant(aa: pointer, n: ptr TNimNode): uint =
# ..\system.nim: proc selectBranch(aa: pointer, n: ptr TNimNode): ptr TNimNode =
# ..\system.nim: proc nimBorrowCurrentException(): ref Exception {.compilerRtl, inl, benign, nodestroy.} =
# ..\system.nim: proc setCurrentException*(exc: ref Exception){.inline, benign.} =
# ..\system.nim: proc rawProc*[T: proc {.closure.} | iterator {.closure.}](x: T): pointer {.noSideEffect, inline.} =
# ..\system.nim: proc rawEnv*[T: proc {.closure.} | iterator {.closure.}](x: T): pointer {.noSideEffect, inline.} =
# ..\system.nim: proc finished*[T: iterator {.closure.}](x: T): bool {.noSideEffect, inline, magic: "Finished".} =
# ..\system.nim: proc shallow*[T](s: var seq[T]){.noSideEffect, inline.} =
# ..\system.nim: proc shallow*(s: var string){.noSideEffect, inline.} =
# ..\system.nim: proc varargsLenImpl(x: NimNode): NimNode {.magic: "LengthOpenArray", noSideEffect.}
# ..\system.nim: proc insert*(x: var string, item: string, i = 0.Natural){.noSideEffect.} =
# ..\system.nim: proc testLocals()=
# ..\system.nim: proc deepCopy*[T](x: var T, y: T){.noSideEffect, magic: "DeepCopy".} =
# ..\system.nim: proc deepCopy*[T](y: T): T =
# ..\system.nim: proc procCall*(x: untyped){.magic: "ProcCall", compileTime.} =
# ..\system.nim: proc strcmp(a, b: cstring): cint {.noSideEffect, importc, header: "<string.h>".}
# ..\system.nim: proc draw(t: Triangle)=
# ..\system.nim: proc substr*(s: openArray[char]): string =
# ..\system.nim: proc substr*(s: string, first, last: int): string = # A bug with `magic: Slice` requires this to exist this way
# ..\system.nim: proc substr*(s: string, first = 0): string =
let myNimVar_a30 = "abcdefgh"
assert myNimVar_a30.substr(2, 5) == "cdef"
# ..\system.nim: proc toOpenArray*[T](x: ptr UncheckedArray[T]; first, last: int): openArray[T] {. magic: "Slice".}
# ..\system.nim: proc toOpenArray*(x: cstring; first, last: int): openArray[char] {. magic: "Slice".}
# ..\system.nim: proc toOpenArray*[T](x: seq[T]; first, last: int): openArray[T] {. magic: "Slice".}
# ..\system.nim: proc toOpenArray*[T](x: openArray[T]; first, last: int): openArray[T] {. magic: "Slice".}
# ..\system.nim: proc toOpenArray*[I, T](x: array[I, T]; first, last: I): openArray[T] {. magic: "Slice".}
# ..\system.nim: proc toOpenArray*(x: string; first, last: int): openArray[char] {. magic: "Slice".}
var myNimVar_a31 = @["a1", "a2"]
myNimVar_a31.add(["b1", "b2"])
assert myNimVar_a31 == @["a1", "a2", "b1", "b2"]
var myNimVar_c14 = @["c0", "c1", "c2", "c3"]
myNimVar_a31.add(myNimVar_c14.toOpenArray(1, 2))
assert myNimVar_a31 == @["a1", "a2", "b1", "b2", "c1", "c2"]
# ..\system.nim: proc addSysExitProc(quitProc: proc(){.noconv.}) {.importc: "atexit", header: "<stdlib.h>".}
# ..\system.nim: proc raiseEIO(msg: string){.noinline, noreturn.} =
# ..\system.nim: proc echoBinSafe(args: openArray[string]){.compilerproc.} =
echo "Hello World"
# ..\system.nim: proc flockfile(f: CFilePtr){.importc, nodecl.}
# ..\system.nim: proc funlockfile(f: CFilePtr){.importc, nodecl.}
# ..\system.nim: proc writeWindows(f: CFilePtr; s: string; doRaise = false)=
# ..\system.nim: proc arrayWith*[T](y: T, size: static int): array[size, T] {.raises: [].} =
var myNimVar_xx22: int
var myNimVar_xx23= arrayWith(myNimVar_xx22, 10)

var raw_guess = readLine(stdin)

proc myadd(a: int, b: int): int =  
  return a + b

proc test_func(): int =
    var 
      s = "Hello World"
      i:int = 1
      child: tuple[name: string, age: int]
      drinks: seq[string]

    let
      l = 200

    echo "Nim Version = ", NimVersion
    echo s

    child = (name: "Rudiger", age: 2)
    drinks = @["Water", "Juice", "Chocolate"]
    drinks.add("Milk")

    if "Milk" in drinks:
      echo "We have Milk and ", drinks.len - 1, " other drinks"

    echo "Read any good books lately?"
    case readLine(stdin)
    of "no", "No":
      echo "Go to your local library."
    of "yes", "Yes":
      echo "Carry on, then."
    else:
      echo "That's great; I assume."

    echo "I'm thinking of a number between 41 and 43. Guess which!"
    let number: int = 42
    var
      raw_guess: string
      guess: int
    while guess != number:
      raw_guess = readLine(stdin)
      if raw_guess == "": continue # Skip this iteration
      guess = strutils.parseInt(raw_guess)
      if guess == 1001:
        echo("AAAAAAGGG!")
        break
      elif guess > number:
        echo("Nope. Too high.")
      elif guess < number:
        echo(guess, " is too low")
      else:
        echo("Yeeeeeehaw!")

    let a = 1
    let b = 1
    var c: int

    c = myadd(a,b)
    echo c

    return 1

var xxxx4 = test_func()