import streamlit as st
import os

from dotenv import load_dotenv

load_dotenv()

from utils import safe_write, attributes, attribute_validations, business_rules

from chains import (
    product_manager_chain,
    file_structure_chain,
    file_path_chain,
    code_chain,
    missing_chain,
    new_classes_chain
)

attributes = attributes()

attribute_validations = attribute_validations()
attribute_validations_str = ', '.join([f'{k}: {v}' for k, v in attribute_validations.items()])

business_rules = business_rules()
business_rules_str = ', '.join([f'{k}: {v}' for k, v in business_rules.items()])


def create_request(attribute_str,
                   attribute_validations_list,
                   business_rules_list):
    return f"""create a fully functional microservice with the below requirements.
    attributes :""" + attribute_str + """
    attribute validations :""" + attribute_validations_list + """
    business rules :""" + business_rules_list + """. 
    Use Redis as the database and generate working code and unit
    and integration tests for the code"""


request = create_request(attributes, attribute_validations_str, business_rules_str)
print("final request is ", request)

st.title("Code Generator")

language = st.radio("Select Language:",
                    ["Python", "Java", "C#", "TypeScript", "Rust", "Kotlin"])

app_name = st.text_input('Enter Project Name:')
submit = st.button("submit", type="primary")

if language and submit and request and app_name:

    dir_path = app_name + '/'

    tech_design = product_manager_chain.run({'language': language, 'input': request})
    req_doc_path = dir_path + '/requirements' + '/requirements.txt'
    safe_write(req_doc_path, tech_design)
    st.markdown(""" :blue[Tech Design : ] """, unsafe_allow_html=True)
    st.write(tech_design)

    file_structure = file_structure_chain.run({'language': language, 'input': tech_design})
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

    missing = True
    missing_dict = {
        file: True for file in files_list
    }

    code_dict = {}

    while missing:

        missing = False
        new_classes_list = []

        for file in files_list:

            code_path = os.path.join(dir_path, 'code', file)
            norm_code_path = os.path.normpath(code_path)

            if not missing_dict[file]:
                safe_write(norm_code_path, code_dict[file])
                st.markdown(""" :red[Code & Unit Tests: 2nd Iteration] """, unsafe_allow_html=True)
                st.write(code_dict[file])
                continue

            code = code_chain.predict(
                language=language,
                file=file,
                tech_design=tech_design,
            )

            code_dict[file] = code

            response = missing_chain.run({'language': language, 'code': code})

            if '<TRUE>' in response:
                missing = missing or missing_dict[file]
            else:
                safe_write(norm_code_path, code)
                st.markdown(""" :blue[Complete Code & Unit Tests: 1st Iteration] """, unsafe_allow_html=True)
                st.write(code)
                continue

            if missing_dict[file]:
                new_classes = new_classes_chain.predict(
                    language=language,
                    tech_design=tech_design,
                    code=code
                )
                new_classes_list.append(new_classes)

        tech_design += '\n\n' + '\n\n'.join(new_classes_list)
