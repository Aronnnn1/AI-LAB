# Simple Vacuum Cleaner Example

# Initial environment (you can change these)
environment = {'A': 'Dirty', 'B': 'Clean'}
vacuum_location = 'A'

def vacuum_cleaner(env, location):
    print(f"Vacuum is in {location}")
    if env[location] == 'Dirty':
        print(f"{location} is Dirty. Cleaning...")
        env[location] = 'Clean'
    else:
        print(f"{location} is already Clean.")

    # Move to the next room
    next_location = 'B' if location == 'A' else 'A'
    print(f"Moving to {next_location}...\n")
    return next_location

# Run the cleaner for 2 steps
for _ in range(2):
    vacuum_location = vacuum_cleaner(environment, vacuum_location)

print("Final Environment State:", environment)
