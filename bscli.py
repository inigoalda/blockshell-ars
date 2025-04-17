# -*- coding: utf-8 -*-
# ===================================================
# ==================== META DATA ===================
# ==================================================
__author__ = "Daxeel Soni"
__url__ = "https://daxeel.github.io"
__email__ = "daxeelsoni44@gmail.com"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daxeel Soni"

# ==================================================
# ================= IMPORT MODULES =================
# ==================================================
import click
import urllib
import json
from blockchain.chain import Block, Blockchain

# ==================================================
# ===== SUPPORTED COMMANDS LIST IN BLOCKSHELL ======
# ==================================================
SUPPORTED_COMMANDS = [
    'dotx',
    'allblocks',
    'getblock',
    'help',
    'checkhash',
    'quit'
]

# Init blockchain
coin = Blockchain()

# Create group of commands
@click.group()
def cli():
    """
        Create a group of commands for CLI
    """
    pass

# ==================================================
# ============= BLOCKSHELL CLI COMMAND =============
# ==================================================
def print_banner():
    """
        Method to print the banner for BlockShell CLI
    """
    print("""
  ____    _                  _       _____   _              _   _
 |  _ \  | |                | |     / ____| | |            | | | |
 | |_) | | |   ___     ___  | | __ | (___   | |__     ___  | | | |
 |  _ <  | |  / _ \   / __| | |/ /  \___ \  | '_ \   / _ \ | | | |
 | |_) | | | | (_) | | (__  |   <   ____) | | | | | |  __/ | | | |
 |____/  |_|  \___/   \___| |_|\_\ |_____/  |_| |_|  \___| |_| |_|

 > A command line utility for learning Blockchain concepts.
 > Type 'help' to see supported commands.
 > Project by Daxeel Soni - https://daxeel.github.io

    """)

@cli.command()
def start():
    """Start BlockShell CLI and load existing blockchain"""
    print_banner()
    print("Loading existing blockchain...")
    coin.load()
    while True:
        cmd = input("[BlockShell] $ ")
        processInput(cmd)
    

@cli.command()
@click.option("--difficulty", default=3, help="Define difficulty level of blockchain.")
def init(difficulty):
    """Initialize local blockchain"""
    print_banner()
    print("Initializing new blockchain...")
    coin.chain = [coin.createGenesisBlock()]
    coin.difficulty = difficulty
    coin.writeBlocks()

    print("Blockchain initialized with difficulty level: " + str(difficulty))

    # Start blockshell shell
    while True:
        cmd = input("[BlockShell] $ ")
        processInput(cmd)

# Process input from Blockshell shell
def processInput(cmd):
    """
        Method to process user input from Blockshell CLI.
    """
    userCmd = cmd.split(" ")[0]
    if len(cmd) > 0:
        if userCmd in SUPPORTED_COMMANDS:
            globals()[userCmd](cmd)
        else:
            # error
            msg = "Command not found. Try help command for documentation"
            throwError(msg)


# ==================================================
# =========== BLOCKSHELL COMMAND METHODS ===========
# ==================================================
import os
def dotx(cmd):
    """
        Do Transaction - Method to perform new transaction on blockchain.
        If cmd points to a filename, it loads JSON objects from each line
        and adds a block for each.
    """
    txData = cmd.split("dotx ")[-1].strip()
    
    if os.path.isfile(txData):  # Check if txData is a valid file path
        print(f"Loading transactions from file: {txData}")
        with open(txData, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                try:
                    data = json.loads(line)
                    print("Doing transaction...")
                    coin.addBlock(Block(data=data))
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON line: {line} (error: {e})")
    else:
        if "{" in txData:
            try:
                txData = json.loads(txData)
            except json.JSONDecodeError:
                print("Invalid JSON provided.")
                return
        print("Doing transaction...")
        coin.addBlock(Block(data=txData))

def allblocks(cmd):
    """
        Method to list all mined blocks.
    """
    print("")
    for eachBlock in coin.chain:
        print(eachBlock.hash)
    print("")

def getblock(cmd):
    """
        Method to fetch the details of block for given hash.
    """
    blockHash = cmd.split(" ")[-1]
    for eachBlock in coin.chain:
        if eachBlock.hash == blockHash:
            print("")
            print(eachBlock.__dict__)
            print("")

def help(cmd):
    """
        Method to display supported commands in Blockshell
    """
    print("Commands:")
    print("   dotx <transaction data>    Create new transaction")
    print("   allblocks                  Fetch all mined blocks in blockchain")
    print("   getblock <block hash>      Fetch information about particular block")
    print("   checkhash                  Verify the integrity of the blockchain")
    print("   help                       Show this help message")

def throwError(msg):
    """
        Method to throw an error from Blockshell.
    """
    print("Error : " + msg)

def fixhash(i):
    """
        Method to fix the hash of the blocks from i to end of blockchain.
        This method is used to fix the hash of the block if it is not valid.
        It calculates the hash of the block and updates it in the blockchain.
        Then it goes through each block in the blockchain and updates its hash.
    """
    print("Fixing hashes...")
    for i in range(i, len(coin.chain)):
        print(f"Fixing hash for block {i}...")
        coin.chain[i].hash = coin.chain[i].calculateHash()
        if i < len(coin.chain) - 1:
            coin.chain[i + 1].previousHash = coin.chain[i].hash
    print("Hashes fixed.")
    # write to file
    with open("chain.txt", "w") as dataFile:
        chainData = []
        for eachBlock in coin.chain:
            chainData.append(eachBlock.__dict__)
        dataFile.write(json.dumps(chainData))
    print("Blockchain updated.")
    

def checkhash(cmd):
    """
        Method to check and optionally fix the hashes in the blockchain.
    """
    print("Checking hashes...")
    for idx in range(len(coin.chain)):
        block = coin.chain[idx]
        recalculated = block.calculateHash()
        if block.hash != recalculated:
            print("Hash mismatch found!")
            print(f" Block {idx} stored hash   : {block.hash}")
            print(f" Block {idx} recalculated   : {recalculated}")
            print(" Blockchain integrity compromised!")
            
            answer = input("Would you like to fix from this block onward? (y/n): ").strip().lower()
            if answer == 'y':
                fixhash(idx)      # re‑hashes and rewrites chain.txt
                print(f"Fixed hashes starting at block {idx}.")
            else:
                print("No changes made.")
            break
    else:
        print("All hashes are valid.")

def quit(cmd):
    """
        Method to exit from Blockshell.
    """
    print("Exiting BlockShell...")
    exit(0)

