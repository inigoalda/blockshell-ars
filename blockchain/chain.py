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
import hashlib
import datetime
import json
from colorama import Fore, Back, Style
import time
import sys

# ==================================================
# =================== BLOCK CLASS ==================
# ==================================================
class Block:
    """
        Create a new block in chain with metadata
    """
    def __init__(self, data, index=0):
        self.index = index
        self.previousHash = ""
        self.data = data
        self.timestamp = str(datetime.datetime.now())
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        """
            Method to calculate hash from metadata
        """
        hashData = str(self.index) + str(self.data) + self.timestamp + self.previousHash + str(self.nonce)
        return hashlib.sha256(hashData.encode('utf-8')).hexdigest()

    def mineBlock(self, difficulty):
        """
            Method for Proof of Work
        """
        print(Back.RED + "\n[Status] Mining block (" + str(self.index) + ") with PoW ...")
        startTime = time.time()

        while self.hash[:difficulty] != "0"*difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()

        endTime = time.time()
        print(Back.BLUE + "[ Info ] Time Elapsed : " + str(endTime - startTime) + " seconds.")
        print(Back.BLUE + "[ Info ] Mined Hash : " + self.hash)
        print(Style.RESET_ALL)

# ==================================================
# ================ BLOCKCHAIN CLASS ================
# ==================================================
class Blockchain:
    """
        Initialize blockchain
    """
    def __init__(self):
        # if chain.txt file exists

        self.chain = [self.createGenesisBlock()]
        self.difficulty = 3

    def load(self):
        # Load existing blockchain from file chain.txt
        try:
            self.chain = []
            with open("chain.txt", "r") as dataFile:
                chainData = json.loads(dataFile.read())
                for eachBlock in chainData:
                    block = Block(eachBlock['data'], eachBlock['index'])
                    block.previousHash = eachBlock['previousHash']
                    block.timestamp = eachBlock['timestamp']
                    block.nonce = eachBlock['nonce']
                    block.hash = eachBlock['hash']
                    self.chain.append(block)
        except FileNotFoundError:
            print("[Info] No existing blockchain found. Creating a new one.")
            self.chain = [self.createGenesisBlock()]
        except json.JSONDecodeError:
            print("[Error] Failed to decode blockchain data. Creating a new one.")
            self.chain = [self.createGenesisBlock()]
        except Exception as e:
            print(f"[Error] An unexpected error occurred: {e}")
            self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        """
            Method create genesis block
        """
        blockData = {
            'uid_epita': "1000",
            'email_epita': "genesis@epita.fr",
            'nom': "Genesis",
            'prenom': "Genesis",
            'image': ""
        }
        return Block(blockData)

    def addBlock(self, newBlock):
        """
            Method to add new block from Block class
        """
        newBlock.index = len(self.chain)
        newBlock.previousHash = self.chain[-1].hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)
        self.writeBlocks()

    def writeBlocks(self):
        """
            Method to write new mined block to blockchain
        """
        dataFile = open("chain.txt", "w")
        chainData = []
        for eachBlock in self.chain:
            chainData.append(eachBlock.__dict__)
        dataFile.write(json.dumps(chainData, indent=4))
        dataFile.close()
