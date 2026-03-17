# MiniQ

MiniQ is a lightweight scripting language designed for quick automation,
file interaction, and reactive programs.

The language focuses on simplicity and readability while still providing
powerful features like watchers, file operations, and modular scripts.

MiniQ programs use the `.mq` file extension.

IMPORTANT: This language is still in development updates will be recent and may bring more to the language.

------------------------------------------------
What makes MiniQ different
------------------------------------------------

MiniQ is designed to be easy to read and easy to write.

Some core ideas behind the language:

• Minimal syntax  
• Reactive programming through watchers  
• Built-in file manipulation  
• Simple scripting without complex setup  
• Modular scripts using imports  

Instead of requiring complex event systems, MiniQ allows programs
to react to changes in the program environment automatically.



------------------------------------------------
Example MiniQ program
------------------------------------------------

var count = 0

watch count == 5
    print "Reached five!"

loop count != 6
    print count
    var count = math(count + 1)


Output:

0
1
2
3
4
Reached five!
5



------------------------------------------------
Typical uses
------------------------------------------------

MiniQ works well for:

• automation scripts  
• quick command-line tools  
• file processing  
• logging systems  
• small utilities  
• reactive scripts that respond to variable changes  



------------------------------------------------
Project structure
------------------------------------------------

A simple MiniQ project might look like this:

main.mq
utils.mq
logs.txt



Example:

main.mq

import utils

run start



utils.mq

func start
    print "MiniQ program started"



------------------------------------------------
Running MiniQ
------------------------------------------------

Run a MiniQ file using the interpreter:

miniq program.mq



------------------------------------------------
Syntax highlighting
------------------------------------------------

MiniQ syntax highlighting in VSCode can be enabled using the
Highlight extension.

See the documentation file for setup instructions.



------------------------------------------------
Documentation
------------------------------------------------

The full MiniQ language documentation can be found in:

docs.txt

This document explains:

• language fundamentals
• control flow
• functions
• file operations
• built-in functions



------------------------------------------------
Design philosophy
------------------------------------------------

MiniQ was designed around three principles:

1. Scripts should be easy to read
2. Programs should react automatically to state changes
3. Useful features should be built into the language



------------------------------------------------
Status
------------------------------------------------

MiniQ is an experimental scripting language and is still evolving.

Features and syntax may change as the language grows.
