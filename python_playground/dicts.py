addresses = {
    'Racicot': 'tighe.racicot@gmail.com',
    'Steve': 'steve@apple.com'
}

print ("Tighe's address is", addresses['Racicot'])

# Delete a key-value pair
del addresses['Racicot']

print('\nThere are {0} contact in the dictionary\n'.format(len(addresses)))

for name, address in addresses.items():
    print('Contact {0} at {1}'.format(name, address))

# Adding a new key-value
addresses['New'] = 'new@new.com'

if ('New' in addresses):
    print("Created new entry.")

addresses['New'] = 'new@new.com'

for name, address in addresses.items():
    print(name)
    print(address)
    print("Entry: {0} <{1}>".format(name, address))

for one, two in addresses.items():
    print(one, two)

print(len(addresses))