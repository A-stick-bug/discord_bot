# weak transposition cipher (temporary)

async def split_len(s, key):
    split_s = []
    for i in range(0, len(s), key):
        split_s.append(s[i:i + key])
        i += key

    last_length = len(split_s[-1])
    if last_length < key:
        split_s[-1] += (key - last_length) * " "
    return split_s


async def encrypt(message, key):
    s = await split_len(message, key)
    encrypted = list(zip(*s))
    encrypted = list(map(lambda x: "".join(x), encrypted))

    return "".join(encrypted)


# made by ChatGPT with slight changes
async def decrypt(message, num_columns):
    # Calculate the number of rows needed to hold the message
    num_rows = len(message) // num_columns
    if len(message) % num_columns > 0:
        num_rows += 1

    # Create a list of empty strings to hold the rows of the transposition table
    table = ['' for _ in range(num_rows)]

    # Fill in the table with the encrypted message
    for i in range(len(message)):
        row = i % num_rows
        col = i // num_rows
        index = col * num_rows + row
        table[row] += message[index]

    # Concatenate the rows of the table to get the decrypted message
    decrypted_message = ''.join(table)

    return decrypted_message
