import sys

def load_celebrity_name(celebrity_file):
    name_list = []
    with open(celebrity_file, 'r') as name_stream:
        for line in name_stream:
            meta = line.rstrip('\n').split('\t')[1]
            meta_fields = meta.split('\001')
            name = ''
            imp = 0
            clk = 0
            for field_str in meta_fields:
                str_fields = field_str.split('\002')
                field_name = str_fields[0]
                if field_name == 'name':
                    name = str_fields[1]
                elif field_name == 'impression_count_history':
                    try:
                        imp = int(str_fields[1])
                    except:
                        continue
                elif field_name == 'click_count_history':
                    try:
                        clk = int(str_fields[1])
                    except:
                        continue

            if imp <= 0:
                continue

            if clk * 1.0 / imp < 0.06:
                continue

            if len(name.decode('utf8')) == 1:
                continue

            name_list.append(name)

    return name_list

if __name__ == '__main__':
    name_list = load_celebrity_name(sys.argv[1])
    for line in sys.stdin:
        fields = line.rstrip('\n').split('\001')
        if len(fields) != 5:
            continue

        query = fields[1]
        try:
            imp = fields[2]
            imp_count = int(imp)
            clk = fields[3]
            long_clk = fields[4]
        except:
            continue

        if imp_count < 3:
            continue

        for name in name_list:
            if query.find(name) != -1:
                print '|'.join([query, name, imp, clk, long_clk])
                break
