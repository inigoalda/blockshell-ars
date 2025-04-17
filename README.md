# BlockShell

A command‑line & web‑based utility to learn the fundamentals of blockchain: chaining, hashing, proof‑of‑work, and block exploration.

## 📖 Overview

BlockShell lets you:
- Spin up a **local blockchain** (persisted in `chain.txt`).
- **Mine** blocks with configurable difficulty via proof‑of‑work.
- **Explore** your chain from the CLI or a built‑in web explorer.

---

## ✨ Features

1. **CLI Shell** (`blockshell`):
   - `init [--difficulty N]` – create a new chain with a genesis block.
   - `start` – load & interact with your existing chain.
   - `dotx <data|file>` – add & mine new block(s).
   - `allblocks` – list all block hashes.
   - `getblock <hash>` – display block details.
   - `checkhash` – verify (and optionally fix) chain integrity.
   - `quit` – exit the shell.

2. **Web Explorer** (`web.py`):
   - Browse all blocks: [templates/blocks.html](templates/blocks.html)
   - View block details: [templates/blockdata.html](templates/blockdata.html)

3. **Persistence**  
   Every mined block is appended to `chain.txt` via [`Blockchain.writeBlocks()`](blockchain/chain.py).

---

## 🚀 Installation

Installed and tested on Debian 12 (Bookworm) with Python 3.11.4. All commands need to be run as `root` or with `sudo`.

```bash
# 1. Install dependencies
apt install python3 python3-pip imagemagick jq

# 2. Clone repo
git clone https://github.com/daxeel/blockshell.git
cd blockshell

# 3. Install editable package
pip install --editable .

# 4. Run via
blockshell
```

---

## ⚙️ CLI Usaage

After installation, run:

```bash
lockshell init --difficulty 4
# → initializes [chain.txt](http://_vscodecontentref_/1) with genesis block and PoW difficulty 4

blockshell start
# → loads existing chain.txt; enter interactive shell
#   [BlockShell] $ dotx '{"foo": "bar"}'
#   [BlockShell] $ allblocks
#   [BlockShell] $ getblock <hash>
#   [BlockShell] $ checkhash
#   [BlockShell] $ quit
```

## 🌐 Web Explorer

Start the web server:

```python
python web.py
```

Then visit:

- All blocks: [http://localhost:5000/](http://localhost:5000/)
- Block details: [http://localhost:5000/block/<hash>](http://localhost:5000/)
