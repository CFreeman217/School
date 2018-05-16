# # def isPhoneNumber(text):
# #     if len(text) != 12:
# #         return False
# #     for i in range(0, 3):
# #         if not text[i].isdecimal():
# #             return False
# #     if text[3] != "-":
# #         return False
# #         if not text[i].isdecimal():
# #             return False
# #     if text[7] != "-":
# #         return False
# #         for i in range(8,12):
# #             if not text[i].isdecimal():
# #                 return False
# #     return True

# # # pNum = isPhoneNumber("913-488-0267")
# # # print(pNum)

# # message = "Call me at 415-555-1011 tomorrow. 415-555-9999 is my office."
# # for i in range(len(message)):
# #     chunk = message[i:i + 12]
# #     if isPhoneNumber(chunk):
# #         print("Phone number found: " + chunk)
# # print("Done")

import re
phoneNumRegex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?      # Area Code
    (\s|-|\.)?              # Separator
    (\d{3})                 # First 3 Digits
    (\s|-|\.)               # Separator
    (\d{4})                 # Last 4
    (\s*(ext|x|ext.)\s*(\d{2,5}))?    # Extension
    )''', re.VERBOSE | re.IGNORECASE)

# Create email regex
emailRegex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+   # Username
    @                   # @ symbol
    [a-zA-Z0-9.-]+      # Domain Name
    (\.[a-zA-Z]{2,4})   # Dot Something
)''', re.VERBOSE)

mo = phoneNumRegex.search("My number is 913-488-0267.")
# print(mo.span())
print(mo)
# print(areaCode)

# import re
# agentNamesRegex = re.compile(r"Agent (\w)\w*")
# out = agentNamesRegex.sub(r"\1****", "Agent Alice told Agent Carol, that Agent Eve knew Agent Bob was a double agent.")
# print(out)