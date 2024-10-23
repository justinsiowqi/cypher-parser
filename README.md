# Cypher Parser

This repository integrates the **libcypher-parser** library, a powerful C-based parser for the Cypher query language, with a Python interface designed for extracting and manipulating Cypher statements. 

## About Libcypher Parser

This project leverages the excellent work done by the contributors of the libcypher-parser.
For more details on the original parser, please visit the [libcypher-parser GitHub repository](https://github.com/cleishm/libcypher-parser).

## Getting Started

### Install for Debian

Step 1: Update System + Install Dependencies
```bash
sudo apt-get update

sudo apt-get install -y build-essential autoconf automake libtool pkg-config wget
sudo apt-get install -y libsqlite3-dev
```

Step 2: Install Pre-Built Libcypher
```bash
wget https://github.com/cleishm/libcypher-parser/releases/download/v0.6.2/libcypher-parser-0.6.2.tar.gz

tar zxvpf libcypher-parser-0.6.2.tar.gz
rm libcypher-parser-0.6.2.tar.gz

cd libcypher-parser-0.6.2
./configure --prefix=/usr/local CFLAGS='-fPIC'
```

Step 3: Build and Test
```bash
make clean check

sudo make install

cd ..
rm -rf libcypher-parser-0.6.2
```