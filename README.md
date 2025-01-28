# B+ Tree Visualization

A Python implementation of a B+ Tree data structure with an interactive GUI visualizer. This project provides a visual way to understand how B+ Trees work and perform various operations on them.


![B+ Tree GUI](screenshots/bplus.png)






## Features

- Interactive GUI built with CustomTkinter
- Visual representation of B+ Tree structure
- Support for the following operations:
  - Insert keys
  - Delete keys
  - Search keys
  - Clear tree
  - Adjust maximum degree (3-7)
- Real-time tree visualization updates
- Tree structure displayed using NetworkX and Matplotlib



## Requirements
- Python
- customtkinter
- matplotlib
- networkx
- pydot
- graphviz


## Installation
1. Clone this repository
2. Install the required dependencies:
pip install customtkinter matplotlib networkx pydot graphviz
3. Ensure Graphviz is installed on your system:
   - Windows: Download from [Graphviz Official Website](https://graphviz.org/download/)
   - Linux: `sudo apt-get install graphviz`
   - macOS: `brew install graphviz`



## Usage
Run the program:
python Bplus.py


### GUI Controls
- **Insert**: Enter a key value and click "Insert" to add it to the tree
- **Delete**: Enter a key value and click "Delete" to remove it from the tree
- **Search**: Enter a key value and click "Search" to find it in the tree
- **Clear**: Click to reset the tree
- **Max Keys**: Select the maximum degree (3-7) from the dropdown menu



