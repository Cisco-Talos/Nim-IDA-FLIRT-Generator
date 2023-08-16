# Nim-IDA-FLIRT-Generator
Nim-IDA-FLIRT-Generator

Adversaries are increasingly writing malware in programming languages such as Go, Rust, or Nim, likely because these languages present challenges to investigators using reverse engineering tools designed to work best against the C family of languages. It’s often difficult for reverse engineers examining non-C languages to differentiate between the malware author’s code and the language’s standard library code. In the vast majority of cases, HexRay’s Interactive Disassembler (IDA) has the out-of-the-box capability to identify library functions or generate custom Fast Library Identification and Recognition Technology (FLIRT) signatures and solve the issue. But for Nim, generating signatures is distinctly more difficult. With all this in mind we decided to start a project to find an automated way to generate custom FLIRT signatures for IDA, which led to a talk at Recon.cx 2023 and a guest blog on Hexrays. This Blog {TBD: add link} describes the technical details of our research and how to use these POC scripts. Happy reversing Nim binaries. 




