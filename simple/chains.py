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
You are provided a rough description of the software and the programming language to use.
You are required to come up with a technical design of the software covering the below.

- The technology stack.
- Full data model based on the attribute list
- Full attribute validations based on the attribute validations 
- Full business rules based on the business rules
- API endpoints
- Error handling

Don't hesitate to make design choices if the initial description doesn't provide enough 
information. 

Don't generate code or unit tests at this stage!!

programming_language: {language}

Human: {input}

Complete software design:
"""

design_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)


prompt = """

System: 
You are an expert software engineer and your job is to design software in {language}. You are provided a complete
software design {input} and the programming language to use.

You are required to come up with a file structure for the software design.

- Provide a detailed description of the file structure with the required folders and {language} files.
- Make sure to design a file structure that incorporates all the best practices of software development in {language}.
- Make sure you explain in which folder each file belong to. 
- Folder and file names should not contain any white spaces.
- A human should be able to exactly recreate that file structure.
- Make sure that those files account for the design of the software.

ONLY RETURN THE FILE STRUCTURE AND NOTHING ELSE !

Don't generate non-{language} files.

language: {language}

Software design: {input}

File structure:

"""

file_structure_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """System: You are an expert software engineer. Your job is to write {language} code.

Return the complete list of the file paths, including the folder structure using the following 
list of {language} files. 

You are provided a complete file structure {input} and the programming language to use.

Only return well formed file paths: ./<FOLDER_NAME>/<FILE_NAME>.py

Follow the following template:
<FILE_PATH 1>
<FILE_PATH 2>
...

ONLY RETURN THE FILE PATHS AND NOTHING ELSE !

language: {language}

Human: {input}

File paths list:

"""

file_path_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

prompt = """
System: 
You are an expert software engineer. Your job is to write {language} code.

- Write the code for the following {file} using the following technical {design}.
- Only refer the sections of the design that are relevant to coding the {file}.
- Example: 
If the design contains a section about the business entity, and the file is a business entity class!
If the design contains a section about the database, and the file is a persistence / repository class!
If the design contains a section about the API, and the file is a controller class!
If the design contains a section about the data model, and the file is a model class!
If the design contains a section about the business rules, and the file is a business validation class!
If the design contains a section about the attribute validations, and the file is an attribute validation class!                  
- Only return code! The code should be able to run in a {language} interpreter or compiler.
- Make sure to implement all the methods and functions fully without any `TODO` or `pass` statements or any other 
placeholders.
- Make sure to import all the necessary packages AND DON'T REPEAT YOURSELF!

THE GENERATED CODE SHOULD BE COMPLETE WITHOUT TODOS, PASSED AND ANY OTHER FORMS OF NON IMPLEMENTED CODE!!

language: {language}

file: {file}

design: {design}

{language} Code for this file:

"""

code_chain = LLMChain.from_string(
    llm=llm,
    template=prompt
)

# prompt = """
# Return `<TRUE>` If the following {language} code contains non-implemented parts and return `<FALSE>` otherwise
#
# If a {language} code contains `TODO` or `pass`, or any other source comment asking the human to implement it,
# that  means the code is not implemented.
#
# language: {language}
#
# code: {code}
#
# Return `<TRUE>` if the code is not implemented and return `<FALSE>` otherwise:
# """
#
# missing_chain = LLMChain.from_string(
#     llm=llm,
#     template=prompt
# )
#
# prompt = """System:
#
# You are an expert software engineer.
#
# The following {language} code may contain non-implemented functions.
#
# If the code contains non-implemented functions, describe what additional functions or classes you would need to
# implement those missing implementations.
# Provide a detailed description of those additional classes or functions that you need to implement.
# Make sure to design a software that incorporates all the best practices of software development.
#
# language: {language}
#
# design: {design}
#
# Code: {code}
#
# Only return text if some functions are not implemented.
#
# The new classes and functions needed:
# """
#
# new_classes_chain = LLMChain.from_string(
#     llm=llm,
#     template=prompt
# )
