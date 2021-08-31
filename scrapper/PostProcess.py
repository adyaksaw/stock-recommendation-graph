def print_to_file(array, file_name):
    with open(file_name, "w") as txt_file:
        for line in array:
            txt_file.write("".join(line) + "\n")


def process_entity(entity):
    temp_entity = ""
    if(len(entity) > 1):
        for x in entity:
            temp_entity += x
            temp_entity += ','
        temp_entity = temp_entity[:-1]
    else:
        temp_entity = entity[0]

    # temp_entity = temp_entity[:-1]  # Remove extraneous newline
    temp_entity = temp_entity.lower()  # Lowercase
    if(temp_entity == 'banks'):
        temp_entity = 'bank'
    if(temp_entity == 'minyak, gas & batu bara'):
        temp_entity = 'minyak, gas, & batu bara'
    if(temp_entity == 'financials'):
        temp_entity = 'keuangan'
    if(temp_entity == 'pendukung minyak, gas & batu bara'):
        temp_entity = 'pendukung minyak, gas, & batu bara'
    if(temp_entity == 'jasa & perlengkapan minyak, gas & batu bara'):
        temp_entity = 'jasa & perlengkapan minyak, gas, & batu bara'
    return temp_entity


def is_empty_entity(entity):
    empty = ['-', 'n/a', '-', '(-)', '0', ' ', '.', '', 'masyarakat', 'publik']
    return entity in empty


def convert_relation(entity):
    direktur_list = [
        'direktur utama', 'wakil direktur utama', 'wakil presiden direktur',
        'presiden direktur'
    ]
    komite_audit_list = [
        'ketua', 'anggota'
    ]
    komisaris_list = [
        'komisaris utama', 'komisaris', 'presiden komisaris',
        'wakil presiden komisaris', 'wakil komisaris utama'
    ]

    entity = entity.lower()
    if (entity in direktur_list):
        entity = 'direktur'
    elif (entity in komite_audit_list):
        entity = 'komite audit'
    elif (entity in komisaris_list):
        entity = 'komisaris'
    return entity


entity = set()
relation_line = set()
with open('relation_raw.csv', "r+") as in_file:
    with open('relation.csv', 'w') as relation_file:
        with open('listing_date.csv', 'w') as listing_file:
            with open('delisting_date.csv', 'w') as delisting_file:
                for line in in_file:
                    parsed_line = line.split(",")
                    added_attribute = parsed_line[-1]
                    added_attribute = added_attribute[:-1]
                    parsed_line.pop()
                    processed_entity = process_entity(parsed_line[2:])
                    if(not is_empty_entity(processed_entity)):
                        parsed_line[1] = convert_relation(parsed_line[1])
                        parsed_line[2] = processed_entity
                        while(len(parsed_line) > 3):
                            parsed_line.pop()
                        parsed_line.append(added_attribute)
                        if(parsed_line[1] == 'tanggal pencatatan'):
                            listing_file.write("|".join(parsed_line) + "\n")
                        elif(parsed_line[1] == 'delisting date'):
                            delisting_file.write("|".join(parsed_line) + "\n")
                        else:
                            converted_line = "|".join(parsed_line) + "\n"
                            if(converted_line in relation_line):
                                continue
                            entity.add(processed_entity)
                            relation_file.write(converted_line)
                            relation_line.add(converted_line)
                    elif(parsed_line[1] == 'tanggal pencatatan'):
                        print(parsed_line[0],
                              "tidak memiliki tanggal pencatatan")


print_to_file(list(entity), 'other_entity.csv')
