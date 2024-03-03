from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# gpt-3.5-turbo-0125
# gpt-4-0125-preview

llm = ChatOpenAI(model_name='gpt-3.5-turbo-0125',
                 streaming=True,
                 callbacks=[StreamingStdOutCallbackHandler()],
                 temperature=0
                 )

prompt = """System: 

You are a product manager, and expert in software design and and your job is to design working software.

You are provided a rough description {input} of the software and the programming language {language} to use.

You are required to come up with a technical design of the software covering the below.

- The technology stack.
- Full data model based on the attribute list
- Full attribute validations based on the attribute validations 
- Full business rules based on the business rules
- API endpoints

produce the output in the following format:
- technology stack: <TECHNOLOGY STACK>
- data model: <DATA MODEL>
- attribute validations: <ATTRIBUTE VALIDATIONS>
- business rules: <BUSINESS RULES>
- api endpoints: <API ENDPOINTS>

Don't generate code or unit tests at this stage and return only the above asked artefacts!!

programming_language: {language}

Human: {input}

Complete software design:
"""

product_manager_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """
System: You are an expert software engineer and your job is to design software in {language}. 

You are provided with the technical design {input} of the software and the programming language {language} to use.

Produce the file structure for a fully working software based on the technical design:

PLEASE DO NOT INCLUDE THE UNIT TESTS IN THE FILE STRUCTURE.

Make sure to take all the aspects of the technical design into consideration and produce the file structure.

Some examples below:

- If the technical design has a section for the data model, refer that section while generating the file structure. - 
If the technical design has a section for the attribute validations, refer that section while generating the file 
structure. - If the technical design has a section for the business rules, refer that section while generating the 
file structure.

Don't generate non-{language} files or any other descriptions and produce JUST the file structure.

language: {language}

Software design: {input}

File structure:

"""

file_structure_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """System: Return the complete list of the file paths, including the folder structure using the following 
list of {language} files. Only return well formed file paths: ./<FOLDER_NAME>/<FILE_NAME>.py

Follow the following template:
<FILE_PATH 1>
<FILE_PATH 2>
...

language: {language}

Human: {input}

File paths list:

"""

file_path_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """
System: You are an expert software engineer in {language}. 

Your job is to write fully functional {language} code. 

Write {language} code for the following file {file} using the following description {tech_design}.

Refer the correct section of the technical design to write the code.

Some examples below: 

- If the technical design has a section for the data model, refer that section while generating code for the domain 
class.
- If the technical design has a section for the attribute validations, refer that section while generating code for
the attribute validations.
- If the technical design has a section for the business rules, refer that section while generating code for the
business rules.

DO NOT REGENERATE THE SAME CODE MORE THAN ONES! REFER THE ALREADY GENERATED CODE! RESPECT THE DRY PRINCIPLE!

Some examples below: 

- If you have already generated the domain class, do not generate it again. import that from the repository class or 
a business services class 

Only return fully functional {language} code and NOTHING ELSE! The code should be able to run in a {language} 
interpreter or compiler.

Make sure to implement all the methods and functions. Make sure to import all the necessary packages. The code should 
be complete.

language: {language}

File name: {file}

tech_design: {tech_design}

code:

"""

code_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """
Return `<TRUE>` If the following {language} code contains non-implemented parts and return `<FALSE>` otherwise

If a {language} code contains `TODO` or `pass`, it means the code is not implemented.

language: {language}

code: {code}

Return `<TRUE>` if the code is not implemented and return `<FALSE>` otherwise:
"""

missing_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """
System: You are an expert {language} software engineer. 

The following {language} code {code} may contain non-implemented functions.

If the code contains non-implemented functions, describe what additional functions or classes you would need to 
implement those missing implementations based on the technical design {tech_design}. 

Provide a detailed description of those additional classes or functions that you need to implement.

Make sure to design a software that incorporates all the best practices of {language} development.

language: {language}

tech_design: {tech_design}

code: {code}

Only return text if some functions are not implemented.

The new classes and functions needed:
"""

new_classes_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)
