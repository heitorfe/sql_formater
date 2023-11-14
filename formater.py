import sqlparse
import re
from sql_metadata import Parser

def remove_linhas_vazias(texto):
    linhas = texto.split('\n')
    linhas_nao_vazias = [linha for linha in linhas if linha.strip() != '']
    texto_sem_linhas_vazias = '\n'.join(linhas_nao_vazias)
    return texto_sem_linhas_vazias


def align_aliases(sql):
    select_from_part = re.search(r'SELECT(.*?)FROM', sql, re.DOTALL | re.IGNORECASE)
    select_clause = select_from_part.group(0)
    select_clause_lines = select_clause.split('\n')

    # get lengths and max length
    lengths=[]

    for line in select_clause_lines:

        split = re.split(' AS ', line)
        length = sum([len(item) for item in split[:-1]]) 
        lengths.append(length)


    max_length = max(lengths)

    new_select_clause = ''

    # align aliases
    for i in range(len(select_clause_lines)):

        line = select_clause_lines[i]
        length = lengths[i]

        diff = max_length - length + 4
        split = re.split(' AS ', line)

        if split[-1].startswith('[') and split[-1].endswith(']'):
            line = line.replace(' AS', ' '*diff + 'AS')
        new_select_clause+=line + '\n'
        
        new_sql = sql.replace(select_clause, new_select_clause)
    return new_sql




def input_as(sql):
    p = Parser(sql)
    tokens = p.tokens
    print('Input as')
    aliases_without_as = []
    selects = 0

    for i, token in enumerate(tokens):

        HAS_BRACKETS = (token.value.startswith('[') and token.value.endswith(']'))


        if token.is_alias_without_as:
            if not HAS_BRACKETS:
                token.value = f'[{token}]'

            token.value = f'AS {token}'
            aliases_without_as.append(token.value)
            print(token)
        elif token.is_alias_definition and not token.is_alias_without_as and not HAS_BRACKETS:   # colocando colchete em alias que ja possuem AS
            token.value = f'[{token}]'

        if token.value == 'SELECT': # impede uso na subquery
            selects += 1
            if selects>1:
                break
            
    return ' '.join([token.value for token in tokens])
    

# Função para formatar o SQL
def format_sql(sql, strip_comments):
    sql_formatted = sqlparse.format(
        sql,
        reindent_aligned=True,
        keyword_case='upper',
        use_space_around_operators = True,
        comma_first=False,
        strip_comments=strip_comments
    )

    sql_formatted = sql_formatted.replace('@ ', '@')
    return sql_formatted


def put_comma_first(sql):

    formatted_sql = sql.replace(',\n', '\n,')

    matches = re.findall(r',  +'  , formatted_sql)
    for i, match in enumerate(matches):
        formatted_sql = formatted_sql.replace(match, ' '*(len(match)-2) + ', ')

    return formatted_sql
