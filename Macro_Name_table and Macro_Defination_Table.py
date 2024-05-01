input_data = [
    "MACRO ABC &ARG1,&ARG2",
    "MOV A,&ARG1",
    "ADD A,&ARG2",
    "MOV &RESULT,A",
    "MEND",
    "ADD X,Y",
    "MACRO XYZ &ARG1,&ARG2",
    "MOV B,&ARG1",
    "SUB B,&ARG2",
    "MOV &RESULT,B",
    "MEND",
    "SUB Z,W"
]

line_no = 1
mntc = 1
mdtc = 1
mnt_table = {}
mdt_table = {}
output = []
index = 0

while index < len(input_data):
    elements = input_data[index].split()

    if elements and elements[0] == 'MACRO':
        index += 1

        # store macro arguments (for use in numbering)
        macro_arguments = []
        if index < len(input_data):
            macro_arguments = input_data[index].split(',')
            macro_arguments = [arg.strip('& ') for arg in macro_arguments]

        mnt_table[mntc] = {'name': elements[1], 'mdt_index': mdtc}
        mdt_table[mdtc] = {'line': input_data[index], 'arguments': {}}

        mntc += 1
        mdtc += 1

        # Increment index to read next line
        index += 1

        while index < len(input_data) and (not elements or elements[0] != 'MEND'):
            # prepare string to be written
            string_to_write = f"{mdtc}\t{input_data[index]}"

            for arg_index, arg in enumerate(macro_arguments):
                if arg in input_data[index]:
                    string_to_write += f"#{arg_index + 1}"

            mdt_table[mdtc] = {'line': string_to_write, 'arguments': {}}
            mdtc += 1

            # Increment index to read next line
            index += 1

            if index < len(input_data):
                elements = input_data[index].split()

        if index < len(input_data) and elements and elements[0] == 'MEND':
            mdt_table[mdtc] = {'line': input_data[index]}
            mdtc += 1

            # Increment index to read next line
            index += 1

    else:
        # write to output
        output.append(input_data[index])
        index += 1

# Display the MNT and MDT tables
print("Macro Name Table (MNT):")
print("MNTC\tMacro Name\tMDT Index")
for key, value in mnt_table.items():
    print(f"{key}\t{value['name']}\t\t{value['mdt_index']}")

print("\nMacro Definition Table (MDT):")
print("MDTC\tLine")
for key, value in mdt_table.items():
    print(f"{key}\t{value['line']}")

print("\nOutput:")
for line in output:
    print(line)