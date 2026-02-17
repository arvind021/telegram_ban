#!/usr/bin/env python3
"""
Account Farming Helper
Generate phone numbers for SMS services
"""

import random

def generate_indian_numbers(count=50):
    """Generate realistic Indian numbers"""
    numbers = []
    prefixes = ['7', '8', '9']
    
    for _ in range(count):
        prefix = random.choice(prefixes)
        number = f"+91{prefix}{random.randint(0, 999999999):09d}"
        numbers.append(number)
    
    return numbers

def save_numbers(numbers, filename="phones.txt"):
    """Save to file"""
    with open(filename, 'w') as f:
        for i, num in enumerate(numbers, 1):
            f.write(f"{i:2d}. {num}\n")
    print(f"💾 Saved {len(numbers)} numbers to {filename}")

if __name__ == "__main__":
    count = int(input("How many numbers? (default 50): ") or 50)
    numbers = generate_indian_numbers(count)
    
    print("\n📱 Generated Numbers:")
    for num in numbers:
        print(num)
    
    save = input("\n💾 Save to phones.txt? (y/n): ").lower() == 'y'
    if save:
        save_numbers(numbers)
    
    print("\n💡 Use these on: SMS-Activate.org | 5sim.net")
