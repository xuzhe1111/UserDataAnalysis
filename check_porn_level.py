import json
import requests
import sys

def load_text(file_path):
    text_list = []
    with open(file_path, 'r') as file_stream:
        for line in file_stream:
            text_list.append(line.rstrip('\n'))

    return text_list

def request_interface(text_list, output_path):
    with open(output_path, 'w') as output_stream:
        for text in text_list:
            url = "%s" % text
            ret = requests.get(url)
            if ret.status_code != 200:
                print "Failed to request interface"
                continue

            response = ret.json()
            for item in response['labelList']:
                if item['label'] == '1':
                    try:
                        prob = float(item['probability'])
                        output_stream.write("%.2f|%s\n" % (prob, text))
                    except:
                        continue

def main():
    file_path = sys.argv[1]
    output_path = sys.argv[2]
    text_list = load_text(file_path)
    request_interface(text_list, output_path)

if __name__ == '__main__':
    main()
