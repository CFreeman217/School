import os
import re
trial_regex = re.compile(r'''(

    (\d+)
    ( kg )
    (osc trial )?
    (\d)?

)''', re.VERBOSE)
for file_name in os.walk('.'):
    
    matches = trial_regex.findall(file_name)
    matches[1] = mass
    if matches[-2] == 'osc trial':
        title = 'displaceMass'
    else:
        title = 'displacement'
    if matches[-1] != []:
        trial = matches[-1]
    prefix = 'Lab10_'
    out_string = prefix + mass + 'g_' + title + trial + '.txt'
    os.rename (file_name, file_name.replace(file_name, out_string))
