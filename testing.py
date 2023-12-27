import csv 

csv_file = 'data/GTIN.csv'

def create_dict(csv_file):
    gtin_part = {}
    with open(csv_file, newline ='', encoding ='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            part,gtin  = row
            gtin_part[gtin] = part
    return gtin_part

dict = create_dict(csv_file)


def get_part(gtin):
    return dict.get(gtin,"No part found")

gtin = "10715001110401"
part = get_part(gtin)
print(part)
