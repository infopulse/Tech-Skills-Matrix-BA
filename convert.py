from jinja2 import Template
import os

TEMPLATE = 'template.html'
MATRIX = 'matrix'
OUTPUT = 'web/index.html'
number = 1


def convert(file, num):
    with open(file) as file:
        lines = file.readlines()

    data = {'category': {}}
    category = ''
    level = 0

    for line in lines:
       
        if '***' in line:
            start = line.index('***')
            end = line.index('***', start + 3)
            text = line[start + 3:end]
            line = line.replace(f'***{text}***', f'<b><i>{text}</i></b>')
        if '**' in line:
            start = line.index('**')
            end = line.index('**', start + 2)
            text = line[start + 2:end]
            line = line.replace(f'**{text}**', f'<b>{text}</b>')
        if '*' in line:
            start = line.index('*')
            end = line.index('*', start + 1)
            text = line[start + 1:end]
            line = line.replace(f'*{text}*', f'<i>{text}</i>')

        if '[' in line and ']' in line and '(' in line and ')' in line:
            start = line.index('[')
            end = line.index(']')
            link = line[line.index('(', start) + 1:line.index(')', start)]
            text = line[start + 1:end]
            line = line.replace(f'[{text}]({link})', f'<a href="{link}">{text}</a>')
            
        if line.startswith('# '):
            data['header'] = line.strip('#')
            data['number'] = '0' + str(num)
        elif line.startswith('## '):
            category = line.strip('##').strip()
            data['category'][category] = ''
        elif line.startswith('### '):
            formatedline = line.strip('###').strip()
            data['category'][category] = data['category'][category] +  '<h3>' + formatedline + '</h3>'
        elif line.startswith('#### '):
            formatedline = line.strip('####').strip()
            data['category'][category] = data['category'][category] +  '<h4>' + formatedline + '</h4>'
        elif line.startswith('##### '):
            formatedline = line.strip('#####').strip()
            data['category'][category] = data['category'][category] +  '<h5>' + formatedline + '</h5>'
        elif line.startswith('###### '):
            formatedline = line.strip('######').strip()
            data['category'][category] = data['category'][category] +  '<h6>' + formatedline + '</h6>'
        elif line.startswith('- ') or line.startswith('  - '):
            content = data['category'][category]
            if line.startswith('- ') and level == 0:
                level = 1
                content =  content + '<ul><li>' + line.strip('- ')
            elif line.startswith('- ') and level == 1:
                content =  content + '<li>' + line.strip('- ')
            elif line.startswith('- ') and level == 2:
                level = 1
                content = content + '</li></ul><li>' + line.strip('- ')
            elif line.startswith('  - ') and level == 1:
                level = 2
                content =  content + '<ul><li>' + line.strip('  - ')
            elif line.startswith('  - ') and level == 2:
                content = content + '<li>' + line.strip('  - ')
              
            data['category'][category] = content
        elif line == '\n':
            data['category'][category] = data['category'].get(category, '') + '</li></ul>' * level
            
        elif line != '\n':
            if data.get('description', ''):
                data['category'][category] = data['category'].get(category, '') + '<p>' + line + '</p>'
            else:
                data['description'] = line
   
    return data


if __name__ == '__main__':
    data = []
    files = os.listdir(MATRIX)
    files.sort()
    for file in files:
        if file.endswith('.md'):
            data.append(convert(os.path.join(MATRIX, file), number))
            number += 1
    template = Template(open(TEMPLATE).read())
    levels = ((1, 'Trainee'), (2, 'Junior'), (3, 'Middle'), (4, 'Senior'), (5, 'Expert'))
    with open(OUTPUT, 'w') as file:
        file.write(template.render(data=data, levels=levels))
