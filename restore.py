#!/usr/bin/env python3
"""
Python restoration of the C code operations
"""

def original_operation():
    """
    Simulate the original C code operation
    """
    # Initialize buffer s (20 bytes total based on s[18] access)
    s = bytearray(20)
    
    # Initial assignments from C code:
    # *s = 0xFC31A21269BD1F01LL;  (8 bytes at offset 0)
    # *&s[8] = 0x13226FC98E35F344LL;  (8 bytes at offset 8)  
    # *&s[16] = 0x5E16;  (2 bytes at offset 16)
    
    # Convert hex values to little-endian bytes
    val1 = 0xFC31A21269BD1F01
    val2 = 0x13226FC98E35F344
    val3 = 0x5E16
    
    # Pack into buffer (little-endian)
    for i in range(8):
        s[i] = (val1 >> (i * 8)) & 0xFF
    for i in range(8):
        s[8 + i] = (val2 >> (i * 8)) & 0xFF
    for i in range(2):
        s[16 + i] = (val3 >> (i * 8)) & 0xFF
    
    print("Initial buffer:")
    print(" ".join(f"{b:02x}" for b in s))
    
    # Set v157 = 20 initially (s[20] address)
    v157 = 0  # This will be the loop counter
    
    # The condition checks s[0] (first byte)
    if s[0] != 0:
        v157 = 0
        # Loop while v157 < 0x10 (16)
        while v157 < 0x10:
            # s[v157 + 2] ^= (v157 + 1) ^ s[1] ^ 0x10;
            if v157 + 2 < len(s):
                s[v157 + 2] ^= (v157 + 1) ^ s[1] ^ 0x10
            v157 += 1
        
        # Clear s[18] and s[0]
        if len(s) > 18:
            s[18] = 0
        s[0] = 0
    
    print("Final buffer after operations:")
    print(" ".join(f"{b:02x}" for b in s))
    
    return s

def reverse_operation():
    """
    Reverse the operations to restore original data
    """
    # Start with the final state (assuming we know s[0] was cleared)
    # We need to work backwards
    
    # Initialize with the same initial values
    s = bytearray(20)
    
    # Initial values
    val1 = 0xFC31A21269BD1F01
    val2 = 0x13226FC98E35F344
    val3 = 0x5E16
    
    for i in range(8):
        s[i] = (val1 >> (i * 8)) & 0xFF
    for i in range(8):
        s[8 + i] = (val2 >> (i * 8)) & 0xFF
    for i in range(2):
        s[16 + i] = (val3 >> (i * 8)) & 0xFF
    
    print("Starting with initial values:")
    print(" ".join(f"{b:02x}" for b in s))
    
    # Store original s[1] value before any modifications
    original_s1 = s[1]
    
    # Apply the XOR operations
    if s[0] != 0:  # This will be true initially
        for v157 in range(0x10):  # 0 to 15
            if v157 + 2 < len(s):
                s[v157 + 2] ^= (v157 + 1) ^ original_s1 ^ 0x10
        
        # Clear s[18] and s[0] as in original
        if len(s) > 18:
            s[18] = 0
        s[0] = 0
    
    print("After forward operation:")
    print(" ".join(f"{b:02x}" for b in s))
    
    # To reverse: we need to restore s[0] and apply inverse XOR
    s[0] = (val1 & 0xFF)  # Restore original s[0]
    
    # Reverse the XOR operations (XOR is its own inverse)
    for v157 in range(0x10):
        if v157 + 2 < len(s):
            s[v157 + 2] ^= (v157 + 1) ^ original_s1 ^ 0x10
    
    print("After reverse operation (restored):")
    print(" ".join(f"{b:02x}" for b in s))
    
    return s

def analyze_pattern():
    """
    Analyze what the XOR pattern does to each byte
    """
    print("XOR Pattern Analysis:")
    print("Position | XOR Value")
    print("-" * 20)
    
    # Assuming s[1] from initial value
    val1 = 0xFC31A21269BD1F01
    s1_original = (val1 >> 8) & 0xFF  # s[1] value
    
    for v157 in range(0x10):
        pos = v157 + 2
        xor_val = (v157 + 1) ^ s1_original ^ 0x10
        print(f"s[{pos:2d}]    | 0x{xor_val:02x} ({xor_val:3d})")

if __name__ == "__main__":
    print("=== Original Operation ===")
    result1 = original_operation()
    
    print("\n=== Reverse Operation ===")
    result2 = reverse_operation()
    
    print("\n=== Pattern Analysis ===")
    analyze_pattern()
    
    print("\n=== Summary ===")
    print("The C code initializes a buffer with specific values,")
    print("then XORs bytes 2-17 with a pattern based on position and s[1],")
    print("finally clearing s[0] and s[18].")
    print("To restore: set s[0] back to original, then apply same XOR (self-inverse).")