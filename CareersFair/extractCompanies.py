from urllib import urlopen

url = raw_input('relative address of the source file: ')
html = urlopen(url).read()

#import sponsors: sponsors.txt
fSponsors = raw_input('relative address of files containing exception companies (i.e. companies that should be deleted from the list): ')
fSponsors = open(fSponsors, 'r').read()
sponsors = fSponsors.split(',')
for i in range(0, len(sponsors)):
    sponsors[i] = sponsors[i].strip(' \t\n')

import re
emails = re.findall(r'(?<=mailto:)[^"\t]*', html)
lines = html.splitlines(False)
lLines = 0
for num, line in enumerate(lines, 0):
    lines[num] = lines[num].strip(' \t')
    if lines[num] != '':
        lines[lLines] = lines[num]
        lLines = lLines + 1

posLines = 0
info, lInfo = [], 0
while posLines < lLines:
    #MARK: processing email
    while re.search(r'(?<=mailto:)[^"\t]*', lines[posLines]) == None:
        posLines += 1
    email = re.search(r'(?<=mailto:)[^"\t]*', lines[posLines]).group(0)
    if re.search(r"<br />", email) != None or re.search(r'<br/>', email) != None:
        posLines += 1
        continue
#    email = email.strip('<br />')
    flagSponsor = False
    for sponsor in sponsors:
        if re.search(sponsor, email) != None:
            flagSponsor = True
            break
    if flagSponsor == True or email == '' or (lInfo != 0 and email == info[lInfo - 1][0]):
        posLines += 1
        continue
    #MARK: processing name
    while re.search(r'(?<=rowspan="2">).*</td>', lines[posLines]) == None:
        posLines += 1
    name = re.search(r'(?<=rowspan="2">).*</td>', lines[posLines]).group(0)[0:-5]
    #MARK: processing contact
    contact = name
    if contact == '':
        contact = 'Sir/Madam'
    contact = contact.split(' ')
    if len(contact) == 3:
        if contact[0] == 'Professor' or contact[0] == 'professor':
            contact[0] = 'Prof.'
        contact = contact[0] + ' ' + contact[2]
    else:
        contact = contact[0]
    info.append([email, name, contact])
    lInfo += 1

for contact in info:
    print contact[0] + ", " + contact[1] + ', ' + contact[2]
#print lInfo

#print re.findall(r'(?<=</a>\n\b</td>\n\b<td rowspan = "2">[^<]/td>)', html)
#print re.findall(r'(?<=</a>\n[<>\/a-z]*)', html)

