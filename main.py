import xml.etree.ElementTree as ET
import os

NAMESPACE = {'ns': 'http://db.softcomputer.com/configuration/db'}


def parse_xml(file_path):
    """Parse XML file and return the root element."""
    print(f"Parsing XML file: {file_path}")
    tree = ET.parse(file_path)
    return tree.getroot()


def print_xml_structure(element, level=0):
    """Recursively print XML structure starting from the given element."""
    indent = '  ' * level
    print(f"{indent}<{element.tag} {element.attrib}>")
    if element.text and element.text.strip():
        print(f"{indent}  {element.text.strip()}")
    for child in element:
        print_xml_structure(child, level + 1)


def extract_table_elements(root):
    """Extract all <Table> elements and their attributes."""
    print("Extracting <Table> elements.")
    tables = root.findall('.//ns:Table', NAMESPACE)
    table_data = {}
    for table in tables:
        name = table.get('Name')
        if name:
            table_data[name] = {
                'Category': table.get('Category'),
                'SubCategory': table.get('SubCategory'),
                'Product': table.get('Product'),
                'Attributes': table.attrib
            }
    print(f"Table data extracted: {table_data}")
    return table_data


def compare_tables(data1, data2, file1_name, file2_name):
    """Compare table attributes from two XML files and provide detailed differences."""
    print("Comparing table attributes.")
    differences = []

    all_names = set(data1.keys()).union(set(data2.keys()))
    print(f"All table names to compare: {all_names}")

    for name in all_names:
        attrs1 = data1.get(name)
        attrs2 = data2.get(name)

        if attrs1 is None:
            differences.append(f"Table '{name}' is missing in {file1_name}.")
            print(f"Table '{name}' is missing in {file1_name}.")
        elif attrs2 is None:
            differences.append(f"Table '{name}' is missing in {file2_name}.")
            print(f"Table '{name}' is missing in {file2_name}.")
        else:
            # Compare relevant attributes
            cat1, subcat1, prod1 = attrs1['Category'], attrs1['SubCategory'], attrs1['Product']
            cat2, subcat2, prod2 = attrs2['Category'], attrs2['SubCategory'], attrs2['Product']

            if cat1 != cat2:
                differences.append(
                    f"Table '{name}' has different Category: {cat1} (in {file1_name}) != {cat2} (in {file2_name})")
            if subcat1 != subcat2:
                differences.append(
                    f"Table '{name}' has different SubCategory: {subcat1} (in {file1_name}) != {subcat2} (in {file2_name})")
            if prod1 != prod2:
                differences.append(
                    f"Table '{name}' has different Product: {prod1} (in {file1_name}) != {prod2} (in {file2_name})")

            if any(attr1 != attr2 for attr1, attr2 in zip([cat1, subcat1, prod1], [cat2, subcat2, prod2])):
                print(f"Table '{name}' has different attributes:")
                print(f"File 1: Category={cat1}, SubCategory={subcat1}, Product={prod1}")
                print(f"File 2: Category={cat2}, SubCategory={subcat2}, Product={prod2}")

    return differences


# Paths to the XML files
file1_path = r'C:\01_SRC\4_1_X\dbdes\xml\GCM.db.xml'
file2_path = r'C:\01_SRC\4_2_X_SDK\dbdes\xml\GSCMNDB.db.xml'

file1_name = os.path.basename(file1_path)
file2_name = os.path.basename(file2_path)

print(f"Processing files:\nFile 1: {file1_path}\nFile 2: {file2_path}")

# Parse the XML files
structure1 = parse_xml(file1_path)
structure2 = parse_xml(file2_path)

print("Printing XML structure for file 1:")
print_xml_structure(structure1)
print("Printing XML structure for file 2:")
print_xml_structure(structure2)

# Extract table data from both XML files
table_data1 = extract_table_elements(structure1)
table_data2 = extract_table_elements(structure2)

print(f"Total elements to compare: {len(table_data1)} in file 1, {len(table_data2)} in file 2")

# Compare table attributes
all_differences = compare_tables(table_data1, table_data2, file1_name, file2_name)

# Determine the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the output file in the same directory as the script
output_file_path = os.path.join(script_dir, 'differences.txt')

# Write differences to the output file
print(f"Writing differences to file: {output_file_path}")

with open(output_file_path, 'w') as file:
    if all_differences:
        file.write("Differences found:\n")
        for difference in all_differences:
            file.write(difference + '\n')
    else:
        file.write("The XML files are identical.\n")

print("Processing complete. Check 'differences.txt' for results.")
