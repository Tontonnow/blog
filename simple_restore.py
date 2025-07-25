#!/usr/bin/env python3
"""
Simplified restoration function for the C code
"""

def restore_buffer(modified_buffer=None):
    """
    Restore the original buffer from the C code
    
    Args:
        modified_buffer: If provided, assumes this is the buffer after C operations
                        If None, demonstrates with the original values
    
    Returns:
        tuple: (original_buffer, modified_buffer)
    """
    
    # Original initialization values from C code
    val1 = 0xFC31A21269BD1F01  # *s = 0xFC31A21269BD1F01LL
    val2 = 0x13226FC98E35F344  # *&s[8] = 0x13226FC98E35F344LL  
    val3 = 0x5E16              # *&s[16] = 0x5E16
    
    # Create original buffer (20 bytes)
    original = bytearray(20)
    
    # Pack values in little-endian format
    for i in range(8):
        original[i] = (val1 >> (i * 8)) & 0xFF
    for i in range(8):
        original[8 + i] = (val2 >> (i * 8)) & 0xFF
    for i in range(2):
        original[16 + i] = (val3 >> (i * 8)) & 0xFF
    
    # Store s[1] for XOR calculations (needed before any modifications)
    s1_value = original[1]
    
    if modified_buffer is None:
        # Simulate the C operations to show the transformation
        modified = bytearray(original)
        
        # Apply the C code transformations
        if modified[0] != 0:  # if (s[0])
            # XOR loop: s[v157 + 2] ^= (v157 + 1) ^ s[1] ^ 0x10
            for v157 in range(0x10):  # while (v157 < 0x10)
                if v157 + 2 < len(modified):
                    modified[v157 + 2] ^= (v157 + 1) ^ s1_value ^ 0x10
            
            # Clear values: s[18] = 0; s[0] = 0;
            if len(modified) > 18:
                modified[18] = 0
            modified[0] = 0
    else:
        modified = bytearray(modified_buffer)
    
    # To restore from modified buffer:
    restored = bytearray(modified)
    
    # Restore s[0] to original value
    restored[0] = original[0]
    
    # Reverse the XOR operations (XOR is self-inverse)
    for v157 in range(0x10):
        if v157 + 2 < len(restored):
            restored[v157 + 2] ^= (v157 + 1) ^ s1_value ^ 0x10
    
    return original, modified, restored

def print_buffer(buf, name):
    """Helper function to print buffer in hex format"""
    print(f"{name}: {' '.join(f'{b:02x}' for b in buf)}")

if __name__ == "__main__":
    print("C Code Buffer Restoration")
    print("=" * 40)
    
    # Demonstrate the restoration
    original, modified, restored = restore_buffer()
    
    print_buffer(original, "Original ")
    print_buffer(modified, "Modified ")
    print_buffer(restored, "Restored ")
    
    # Verify restoration worked
    if original == restored:
        print("\n✅ Restoration successful! Original buffer recovered.")
    else:
        print("\n❌ Restoration failed!")
    
    print(f"\nKey insight: s[1] = 0x{original[1]:02x} is used in XOR pattern")
    print("XOR pattern: (position+1) ^ s[1] ^ 0x10 applied to bytes 2-17")