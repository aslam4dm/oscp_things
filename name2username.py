import itertools

def generate_usernames(first_name, last_name):
    first_initial = first_name[0]
    last_initial = last_name[0]
    
    combinations = [
        f"{first_name}.{last_initial}",
        f"{first_name}{last_initial}",
        f"{first_name}_{last_initial}",
        f"{last_initial}.{first_name}",
        f"{last_initial}{first_name}",
        f"{last_initial}_{first_name}",
        f"{first_initial}.{last_name}",
        f"{first_initial}{last_name}",
        f"{first_initial}_{last_name}",
        f"{first_name}.{last_name}",
        f"{first_name}{last_name}",
        f"{first_name}_{last_name}",
        f"{last_name}.{first_name}",
        f"{last_name}{first_name}",
        f"{last_name}_{first_name}"
    ]
    
    return combinations

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        names = [line.strip().split() for line in file.readlines()]
    return names

def write_output_file(output_path, username_list):
    with open(output_path, 'w') as file:
        for username in username_list:
            file.write(f"{username}\n")

if __name__ == "__main__":
    input_file = 'users.txt'  # Path to your input file with names
    output_file = 'valid_usernames.txt'  # Path to your output file
    
    # Read names from input file
    names = read_input_file(input_file)
    
    # Generate usernames for each name
    all_usernames = []
    for first_name, last_name in names:
        usernames = generate_usernames(first_name.lower(), last_name.lower())
        all_usernames.extend(usernames)
    
    # Write usernames to output file
    write_output_file(output_file, all_usernames)

    print("Usernames generated successfully.")
