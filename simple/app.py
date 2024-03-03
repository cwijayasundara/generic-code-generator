import streamlit as st

from dotenv import load_dotenv
from utils import safe_write, attributes, attribute_validations, business_rules

load_dotenv()

attribute_set = attributes()
attribute_set = ', '.join(attribute_set)

attribute_validations_set = attribute_validations()
attribute_validations_set = ', '.join(attribute_validations_set)

business_rules_set = business_rules()
business_rules_set = ', '.join(business_rules_set)


def create_request(attributes_list,
                   attribute_validations_list,
                   business_rules_list):
    return f"""create a fully functional microservice with the below requirements.
    attributes :""" + attributes_list + """
    attribute validations :""" + attribute_validations_list + """
    business rules :""" + business_rules_list


request = create_request(attribute_set, attribute_validations_set, business_rules_set)
print(request)

from chains import (
    design_chain,
    file_structure_chain,
    file_path_chain,
    code_chain,
)

st.title("Code Generator")

language = st.radio("Select Language:",
                    ["Python", "Java", "C#", "TypeScript", "Rust", "Kotlin"])

app_name = st.text_input('Enter Project Name:')
submit = st.button("submit", type="primary")

if language and submit and app_name:

    dir_path = app_name + '/'

    design = design_chain.run({'language': language, 'input': request})
    design_doc_path = dir_path + '/design' + '/design.txt'
    safe_write(design_doc_path, design)
    st.markdown(""" :blue[Technical Design : ] """, unsafe_allow_html=True)
    st.write(design)

    file_structure = file_structure_chain.run({'language': language, 'input': design})
    file_structure_path = dir_path + '/file_structure' + '/file_structure.txt'
    safe_write(file_structure_path, file_structure)
    st.markdown(""" :blue[File Names :] """, unsafe_allow_html=True)
    st.write(file_structure)

    files = file_path_chain.run({'language': language, 'input': file_structure})
    files_path = dir_path + '/files' + '/files.txt'
    safe_write(files_path, files)
    st.markdown(""" :blue[File Paths :] """, unsafe_allow_html=True)
    st.write(files)

    files_list = files.split('\n')

    for file in files_list:
        st.markdown(""" :blue[Generating code for + {file} :] """, unsafe_allow_html=True)
        code = code_chain.predict(language=language, file=file, design=design)
        safe_write(files_path, code)
        st.write(code)
