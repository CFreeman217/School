def conv_date(in_date):
    num_days = {1:31,
                2:28,
                3:31,
                4:30,
                5:31,
                6:30,
                7:31,
                8:31,
                9:30,
                10:31,
                11:30,
                12:31}

    month = int(in_date[0])
    day = int(in_date[1])
    today = day
    m_iter = 1
    while m_iter < month:
        today += num_days[m_iter]
        m_iter += 1
    return today

def askdate():
    while True:
        in_mo = input('Enter Month : ')
        in_day = input('Enter Day : ')
        if in_mo.isalpha() or in_day.isalpha():
            print('Function takes number arguments only. Exiting.')
            break

        number = conv_date([in_mo, in_day])
        print('Converted date is {}'.format(number))

askdate()