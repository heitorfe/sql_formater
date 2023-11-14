import streamlit as st

from formater import *

# Configuração do aplicativo Streamlit
st.title("Formatador SQL")

# Text Area para inserir o SQL
sql_input = st.text_area("Insira o SQL aqui")

# Controles deslizantes e seletores para os parâmetros
comma_first = st.checkbox("Vírgula primeiro", value = True)
strip_comments = st.checkbox("Remover comentários", value = False)
align_aliases_config = st.checkbox("Alinha aliases (Em desenvolvimento)", value = True)
# input_as_into_aliases  = st.checkbox("Input 'AS'", value = False)


# Botão para formatar o SQL
if st.button("Formatar"):
    if sql_input:

        if align_aliases_config:
            sql_input = input_as(sql_input)

        formatted_sql = format_sql(sql_input, strip_comments)
        formatted_sql = remove_linhas_vazias(formatted_sql)

        if comma_first:
            formatted_sql = put_comma_first(formatted_sql)

        if align_aliases_config:
            formatted_sql = align_aliases(formatted_sql)

        st.text("SQL Formatado:")
        st.code(formatted_sql, language="sql", line_numbers=True)

        
    else:
        st.warning("Por favor, insira um SQL para formatar.")



