#!/bin/bash

import sys

def generate_username_variations(input_file, output_file):
    with open(input_file, 'r') as file:
        usernames = file.read().splitlines()

    variations = ['password','Password','PASSWORD','admin','Admin','ADMIN']
    for username in usernames:
        # Basic variations
        variations.append(username.lower())       # bob
        variations.append(username.capitalize())  # Bob
        variations.append(username.upper())       # BOB
        
        # Variations with exclamation mark
        variations.append(username.lower() + '!')       # bob!
        variations.append(username.capitalize() + '!')  # Bob!
        variations.append(username.upper() + '!')       # BOB!
        
        # Variations with '1'
        variations.append(username.lower() + '1')       # bob1
        variations.append(username.capitalize() + '1')  # Bob1
        variations.append(username.upper() + '1')       # BOB1

    with open(output_file, 'w') as file:
        for variation in variations:
            file.write(variation + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = 'user2pass.out'
    generate_username_variations(input_file, output_file)
    print(f"Username variations saved to {output_file}")
