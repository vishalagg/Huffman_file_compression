from functools import total_ordering
import heapq
import os,sys

@total_ordering
class Node:
    def __init__(self,char,freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __eq__(self,other):
            if(other==None):
                return False
            elif(isinstance(other,Node)):
                return self.freq == other.freq
            else:
                return False
    def __lt__(self,other):
            return self.freq < other.freq
        
class HuffmanCode:
    def __init__(self,path):
        self.path = path
        self.minHeap = []
        self.codes = {}
        self.revCodes = {}
        self.pad = 0
        
    def getFrequency(self,text):
        freq = {}
        for x in text :
            if not x in freq :
                freq[x] = 1
            freq[x] += 1
        return freq
    
    def buildHeap(self,freq):
        for key in freq :
            node = Node(key,freq[key])
            heapq.heappush(self.minHeap,node)
            
    def merge(self):
        while(len(self.minHeap)>1):
            node1 = heapq.heappop(self.minHeap)
            node2 = heapq.heappop(self.minHeap)
            merged = Node(None,node1.freq+node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.minHeap,merged)
            
    def getCodeRecursive(self,root,code):
        if(root == None):
            return
        if(root.char != None):
            self.codes[root.char] = code
            self.revCodes[code] = root.char
            return
        self.getCodeRecursive(root.left,code + "0")
        self.getCodeRecursive(root.right,code + "1")

    def getCode(self):
        root = heapq.heappop(self.minHeap)
        code = ""
        self.getCodeRecursive(root,code)
        
    def encod(self,text):
        encoded = ""
        for character in text:
            encoded += self.codes[character]
        return encoded
    
    def padding(self, encoded):
        self.pad = 8 - len(encoded) % 8
        for i in range(self.pad):
            encoded += "0"
        extra = format(self.pad, "08b")
        encoded = extra + encoded
        return encoded

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        bin_file = filename + ".bin"

        with open(self.path, 'r+') as file, open(bin_file, 'wb') as output:
            text = file.read()
            text = text.rstrip()
            frequency = self.getFrequency(text)
            self.buildHeap(frequency)
            self.merge()
            self.getCode()

            encoded = self.encod(text)
            encod_padding = self.padding(encoded)

            ba = bytearray()
            for i in range(0, len(encod_padding), 8):
                byte = encod_padding[i:i+8]
                ba.append(int(byte, 2))
            output.write(bytes(ba))

file_path = "C:/Users/vishal/Desktop/huffman_code/text.txt"

x = HuffmanCode(file_path)

x.compress()
#print(x.revCodes)
f = open("key.bin",'w')
x.revCodes['pad'] = x.pad
f.write(str(x.revCodes))

#print(sys.getsizeof(h.revCodes))
#print(h.pad)