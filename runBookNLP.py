## By Eva Portelance - June 20, 2017
## Modified by Cheng Lin - Feb 4, 2019
## Usage: runBookNLP.py <directorynameforbooks>
import os, sys, csv

femPRP = {'she','herself', 'ms.','ms','miss','mrs.','mrs','madam','lady'}
masPRP = {'he','himself', 'mr.','mr','sir', 'mister','lord'}

def run_book_nlp(parent_path, subpath_for_output):
    if len(subpath_for_output) >0:
        subpath_for_output += '/'

    for file_path in os.listdir(parent_path):
        full_path = os.path.join(parent_path, file_path)

        #if fullpath leads to a text file
        if file_path.endswith('.txt'):
            print('\n---------Running bookNLP for '+ full_path +'----------\n')

            command = './runjava novels/BookNLP -doc ' + parent_path +'/'+ file_path \
                      + ' -printHTML -p data/output/' + subpath_for_output+file_path + '.result' \
                      + ' -tok data/tokens/' + subpath_for_output+file_path + '.tokens.csv -f'
            os.system(command)

            print('\n---------Running gender feature for ' + full_path + '----------\n')
            add_gender('data/tokens/'+subpath_for_output+file_path+'.tokens.csv')

        # if full path is a folder directory
        if os.path.isdir(full_path):
            print('\n---------'+file_path+' is a directory----------\n')
            run_book_nlp(parent_path+'/'+file_path, file_path)


def add_gender(file_path):
    table = []
    file = file_path
    with open(file, encoding='utf-8', mode='r+') as f:
        for line in f:
            table.append(line.strip('\n').split('\t'))
    f.close()
    title = table[0]
    title.append('totalPRPgender')
    title.append('confidenceGender')
    title.append('genderLabel')
    table = table[1:]

    characters = []
    for line in table:
        if line[14] != '-1':
            if line[14] not in characters:
                characters.append(line[14])

    genderCounts = []
    for c in characters:
        fem=0
        mas=0
        for line in table:
            if line[14] == c:
                if line[9].lower() in femPRP:
                    fem+=1
                elif line[9].lower() in masPRP:
                    mas+=1
        tot=fem+mas

        # if more female than male pronouns, label as female (label = 1)
        if fem > mas:
            ratio = fem/tot
            label = 1
        # if more male than female pronouns, label as male (label = 2)
        elif fem < mas:
            ratio = mas/tot
            label=2
        else:
            ratio = 0.5
            label=0
        genderCounts.append([c,[tot,ratio,label]])

    for line in table:
        if line[14] != '-1':
            found = False
            for c in genderCounts:
                if c[0] == line[14]:
                    line.append(c[1][0])
                    line.append(c[1][1])
                    line.append(c[1][2])
                    found = True
            if not found:
                line.append(0)
                line.append(0.5)
                line.append(0)
        else:
            line.append(0)
            line.append(0)
            line.append(0)
    with open(file, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(title)
        writer.writerows(table)
    f.close()


print('corpus root directory: '+ sys.argv[1])
run_book_nlp(sys.argv[1], "")