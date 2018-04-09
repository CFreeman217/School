import re

string = '''
16097 EPIC MOUNT DORA 12 - Sheet - E1-10 - FIRST FLOOR PLAN - LIGHTING A.pdf
16097 EPIC MOUNT DORA 12 - Sheet - E2-63 - LIGHTING SCHEDULE AND DETAILS.pdf
16043 - FRIDLEY WAUKEE 12 SCREEN -  MEP_cfreemanYG8P3 - Sheet - P1-10 - FIRST FLOOR PLAN - PLUMBING.pdf
'''
.       - Any Character Except New Line
# \d      - Digit (0-9)
# \D      - Not a Digit (0-9)
# \w      - Word Character (a-z, A-Z, 0-9, _)
# \W      - Not a Word Character
# \s      - Whitespace (space, tab, newline)
# \S      - Not Whitespace (space, tab, newline)

# \b      - Word Boundary
# \B      - Not a Word Boundary
# ^       - Beginning of a String
# $       - End of a String

# []      - Matches Characters in brackets
# [^ ]    - Matches Characters NOT in brackets
# |       - Either Or
# ( )     - Group

# Quantifiers:
# *       - 0 or More
# +       - 1 or More
# ?       - 0 or One
# {3}     - Exact Number
# {3,4}   - Range of Numbers (Minimum, Maximum)


# #### Sample Regexs ####

# [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+
sheetRegex = re.compile(r"""(                    
    (\d{5})             # Job number
    (\s.\s)?            # Trash
    (.*)                # Job name
    (\s-\s)             # Trash
    (.*)?               # Trash Job Name
    (\s.\s)?            # Trash " - "
    (Sheet)             # Trash "Sheet"
    (\s.\s)             # Trash
    (\D\d.\d\d)         # Sheet Number
    (\s.\s)             # Trash
    (.*)                # Sheet Name
    (\.[a-zA-Z]{2,4})   # Suffix
                        )""", re.VERBOSE)

matches = sheetRegex.findall(string)
output = []
for match in matches:
    print(match)
    jNum = match[1]
    jName = match[3].strip()
    sNum = match[-4]
    sName = match[-2]
    suffix = match[-1]
    out_str = jNum + " - " + sNum + " - " + sName + suffix
    print(out_str)