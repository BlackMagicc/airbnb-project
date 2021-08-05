from airbnb.airbnb import Airbnb

with Airbnb() as bot:
    bot.land_first_page()
    # bot.select_place_to_go(input('Where would you like to go? '))
    bot.select_place_to_go('Seattle')
    # bot.select_dates(check_in_date=input('Enter check in date (Month Day, Year) '),
    #                  check_out_date=input('Enter check out date (Month Day, Year) '))    bot.select_place_to_go(input('Where would you like to go? '))
    bot.select_dates(check_in_date='2021-09-14',
                     check_out_date='2021-09-28')
    # bot.select_guests(int(input('How many guests? ')))
    bot.select_guests(3)
    # bot.search()
    # bot.more_filters()
    # bot.apply_filters()
    # bot.refresh()
    # bot.report_results()
