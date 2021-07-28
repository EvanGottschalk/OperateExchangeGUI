# PURPOSE - This program creates a GUI that allows the user to easily create, modify, and cancel array orders on cryptocurrency exchanges

import tkinter
import tkinter.font as font
import copy
import pickle
import pathlib
import os

# OperateExchange is the program which this GUI allows one to use; it does all the calculations for array orders and stores important variables
from OperateExchange import OperateExchange

# This function will create the OperateExchangeGUI class in a non-local scope, making it more secure
def main():
    OE_GUI = OperateExchangeGUI()
    OE_GUI.main_loop()
    del OE_GUI

class OperateExchangeGUI:
    def __init__(self):
    # Array Order settings can be saved to any of 5 save slots; these are located at the very top of the GUI
        self.profile_display = {'I': '', \
                                'II': '', \
                                'III': '', \
                                'IV': '', \
                                'V': ''}
        self.profile_functions = {'I': self.saveProfile_I, \
                                  'II': self.saveProfile_II, \
                                  'III': self.saveProfile_III, \
                                  'IV': self.saveProfile_IV, \
                                  'V': self.saveProfile_V}
    # These variables define all the different colors used in the GUI. Feel free to change them!
        self.my_colors = {'Green': '#41f04c', \
                          'Dark Green': '#0d9900', \
                          'Light Green': '#a0ff8f', \
                          'Red': '#FF0000', \
                          'Light Red': '#ff9696', \
                          'Teal': '#a1ffe3', \
                          'Light Teal': '#d4ffff', \
                          'Pink': '#ff8fd4', \
                          'White': '#FFFFFF', \
                          'Black': '#000000', \
                          'Gray': '#f0f0f0', \
                          'Dark Gray': '#919191', \
                          'Yellow': '#fff200', \
                          'Light Yellow': '#fffaa1', \
                          'Orange': '#ffa600', \
                          'Light Orange': '#ffd9a1', \
                          'Sky Blue': '#b3edff', \
                          'Light Blue': '#92a9fc', \
                          'Lighter Blue': '#bfcdff', \
                          'Blue': '#0000ff', \
                          'Indigo': '#6600ff', \
                          'Purple': '#9900ff', \
                          'Lavender': '#c9a6ff', \
                          'Salmon': '#ffa6b5'}
        self.green_colors = {5: '#f2fff2', \
                            10: '#e6ffe6', \
                            15: '#d7fcd7', \
                            20: '#ccffcc', \
                            25: '#bfffbf', \
                            30: '#b3ffb3'}
        self.red_colors = {5: '#fff2f2', \
                           10: '#ffe6e6', \
                           15: '#ffd9d9', \
                           20: '#ffcccc', \
                           25: '#ffbfbf', \
                           30: '#ffb3b3'}
        self.symbol_colors = {'BTC/USD': '#F7931A', \
                              'ETH/USD': '#FFFF00', \
                              'LTC/USD': self.my_colors['Gray'], \
                              'DOGE/USD': '#B69A35'}
        self.symbol_defaults = {'BTC/USD': {'Amount': 1000, \
                                            'Price': 30000, \
                                            'Granularity': 50, \
                                            'Spread': 2000, \
                                            'End Price': 28000}, \
                                'ETH/USD': {'Amount': 50, \
                                            'Price': 2000, \
                                            'Granularity': .1, \
                                            'Spread': 50, \
                                            'End Price': 1950}, \
                                'LTC/USD': {'Amount': 30, \
                                            'Price': 100, \
                                            'Granularity': .5, \
                                            'Spread': 10, \
                                            'End Price': 90}, \
                                'DOGE/USD': {'Amount': 20, \
                                             'Price': .18, \
                                             'Granularity': .001, \
                                             'Spread': .01, \
                                             'End Price': .17}}
        self.account_colors = {'Main': self.my_colors['White'], \
                               'Short 50x': self.my_colors['Pink'], \
                               'Long 50x': self.my_colors['Teal'], \
                               'Short 50x Quick':self.my_colors['Dark Green'], \
                               'Long 50x Quick':self.my_colors['Light Green'], \
                               'Monty': self.my_colors['Yellow']}
      # Each exchange has its own unique style and color scheme. As exchanges are added, their respective color schemes will be saved in pickle files.
      # That way, when using the GUI, it can assume an appearance similar to the exchange it's connected to. This is nice aesthetically, and also will help
      # prevent users from accidentally thinking they are connected to a different exchange.
        self.all_exchange_colors = {}
        for file in os.listdir('Exchange Colors'):
            self.all_exchange_colors[file.split('.')[0]] = pickle.load(open('Exchange Colors/' + file, 'rb'))
    # There are 10 slots at the bottom of the GUI which show information and buttons for a user's 10 most recent array orders
        self.active_order_labels = {}
        self.active_order_positions = {1: '', \
                                       2: '', \
                                       3: '', \
                                       4: '', \
                                       5: '', \
                                       6: '', \
                                       7: '', \
                                       8: '', \
                                       9: '', \
                                       10: ''}
    # window_height and window_width determine the size of the GUI window
        self.window_width = 940
        self.window_height = 1000
        self.window_size = str(self.window_width) + 'x' + str(self.window_height)
    # layoutDict determines where each modifiable parameter appears in the GUI. Feel free to change it up!
        self.layoutDict = {'Profiles': 0, \
                           'Account': 6, \
                           'Symbol': 7, \
                           'Side': 8, \
                           'Amount': 9, \
                           'Price': 10, \
                           'End Price': 12, \
                           'Spread': 13, \
                           'Granularity': 14, \
                           'Steepness': 15, \
                           'Slope': 16, \
                           'Minimum Order Size': 17, \
                           'Truncation Amount': 17, \
                           'Quick Granularity': 17, \
                           'Style': 18}
    # The 17th row in the GUI interface has been used for testing. It can be changed to a different operation by modifying the row_17_button variable
        #self.row_17_button = 'Truncation Amount'
        #self.row_17_button = 'Minimum Order Size'
        self.row_17_button = 'Quick Granularity'
    # These functions allow users to cancel or rebuild individual array orders
    # They are associated with int values to make it easier to run these functions through the GUI buttons
        self.individual_order_functions = {'Cancel': {1: self.cancelArrayOrder_1, \
                                                      2: self.cancelArrayOrder_2, \
                                                      3: self.cancelArrayOrder_3, \
                                                      4: self.cancelArrayOrder_4, \
                                                      5: self.cancelArrayOrder_5, \
                                                      6: self.cancelArrayOrder_6, \
                                                      7: self.cancelArrayOrder_7, \
                                                      8: self.cancelArrayOrder_8, \
                                                      9: self.cancelArrayOrder_9, \
                                                      10: self.cancelArrayOrder_10}, \
                                           'Rebuild': {1: self.rebuildArrayOrder_1, \
                                                      2: self.rebuildArrayOrder_2, \
                                                      3: self.rebuildArrayOrder_3, \
                                                      4: self.rebuildArrayOrder_4, \
                                                      5: self.rebuildArrayOrder_5, \
                                                      6: self.rebuildArrayOrder_6, \
                                                      7: self.rebuildArrayOrder_7, \
                                                      8: self.rebuildArrayOrder_8, \
                                                      9: self.rebuildArrayOrder_9, \
                                                      10: self.rebuildArrayOrder_10}}
    # UNDER DEVELOPMENT - this variable stores the default layout. A GUI button should be created that allows users to change the layout and save their version.
        self.default_layout = self.layoutDict
    # If auto_preview is True, then a preview of a user's array order will be generated every time they change the order settings.
    # Setting auto_preview to False greatly increases the speed at which one can change the order settings.
    # This feature can be toggled in the GUI
        self.auto_preview = False
        self.auto_quick_rebuild = True
        self.lock_end_price = False
        self.settings_have_changed_since_last_preview = False
        self.quick_granularity_intensity = False
        self.multiplicative_style = False
        self.OE = OperateExchange()
        self.OE.CTE.connect()
        self.current_exchange_colors = self.all_exchange_colors[self.OE.CTE.currentConnectionDetails['Exchange Name']]
        self.GUI = tkinter.Tk()
        self.GUI.configure(bg='#FFFFFF')
        self.font_dict = {'Top Spacer': font.Font(family='Helvetica', size=2), \
                          'Bottom Spacer': font.Font(family='Helvetica', size=2), \
                          1: font.Font(family='Helvetica', size=1), \
                          2: font.Font(family='Helvetica', size=2), \
                          3: font.Font(family='Helvetica', size=3), \
                          4: font.Font(family='Helvetica', size=4), \
                          5: font.Font(family='Helvetica', size=5), \
                          6: font.Font(family='Helvetica', size=6), \
                          7: font.Font(family='Helvetica', size=7), \
                          8: font.Font(family='Helvetica', size=8), \
                          9: font.Font(family='Helvetica', size=9), \
                          10: font.Font(family='Helvetica', size=10), \
                          11: font.Font(family='Helvetica', size=11), \
                          12: font.Font(family='Helvetica', size=12), \
                          13: font.Font(family='Helvetica', size=13), \
                          14: font.Font(family='Helvetica', size=14), \
                          15: font.Font(family='Helvetica', size=15)}
        self.button_font = font.Font(family='Helvetica', size=12)
        self.label_font = font.Font(family='Helvetica', size=12)
        self.title_font = font.Font(family='Helvetica', size=14)
        self.entry_font = font.Font(size=12)
        self.nudge_font = font.Font(family='Helvetica', size=9)
        self.current_value_font = self.label_font

    def main_loop(self):
        self.createGUI()

    def createGUI(self):
### Widgets are created
        
## Create general order widgets

        self.label_order_settings_top_spacer = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], font=self.font_dict['Top Spacer'], text='')
        self.label_general_settings_title = tkinter.Label(self.GUI, font=self.title_font, pady=7, \
                                                          padx=350, text='- General Order Settings -')
        self.button_auto_preview = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text=' Auto-Preview ', command=self.toggleAutoPreview)
        self.label_order_settings_bottom_spacer = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], font=self.font_dict['Bottom Spacer'], text='')
        self.label_last_action = tkinter.Label(self.GUI, font=self.font_dict[9], bg=self.current_exchange_colors['White'], text='. . .')
    # Account Input
        self.label_current_account_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Account: ')
        self.label_current_account = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.account_colors[self.OE.orderSettings['Account']], borderwidth=1, \
                                                   relief='solid', text=' ' + self.OE.orderSettings['Account'] + ' ')
        self.menubutton_account = tkinter.Menubutton(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   direction='right', relief='raised', text='   Change Account   ')
        self.menubutton_account.menu = tkinter.Menu(self.menubutton_account, tearoff=0)
        self.menubutton_account["menu"] = self.menubutton_account.menu
        self.menubutton_account.menu.add_radiobutton(label='Main', command=self.changeAccount_Main)
        self.menubutton_account.menu.add_radiobutton(label='Short 50x', command=self.changeAccount_Short50x)
        self.menubutton_account.menu.add_radiobutton(label='Long 50x', command=self.changeAccount_Long50x)
        self.menubutton_account.menu.add_radiobutton(label='Short 50x Quick', command=self.changeAccount_Short50xQuick)
        self.menubutton_account.menu.add_radiobutton(label='Long 50x Quick', command=self.changeAccount_Long50xQuick)
        self.menubutton_account.menu.add_radiobutton(label='Monty', command=self.changeAccount_Monty)
    # Symbol Input
        self.label_current_symbol_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Symbol: ')
        self.label_current_symbol = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.symbol_colors[self.OE.orderSettings['Symbol']], text=' ' + str(self.OE.orderSettings['Symbol']) + ' ')
        self.menubutton_symbol = tkinter.Menubutton(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=7, direction='right', relief='raised', text='   Change Symbol   ')
        self.menubutton_symbol.menu = tkinter.Menu(self.menubutton_symbol, tearoff=0)
        self.menubutton_symbol["menu"] =  self.menubutton_symbol.menu
        self.menubutton_symbol.menu.add_radiobutton(label='BTC/USD', command=self.changeSymbol_BTC)
        self.menubutton_symbol.menu.add_radiobutton(label='ETH/USD', command=self.changeSymbol_ETH)
        self.menubutton_symbol.menu.add_radiobutton(label='LTC/USD', command=self.changeSymbol_LTC)
        self.menubutton_symbol.menu.add_radiobutton(label='DOGE/USD', command=self.changeSymbol_DOGE)
        self.menubutton_symbol.menu.add_radiobutton(label='LINK/USD', command=self.changeSymbol_LINK)
        self.menubutton_symbol.menu.add_radiobutton(label='ADA/USD', command=self.changeSymbol_ADA)
        self.menubutton_symbol.menu.add_radiobutton(label='UNI/USD', command=self.changeSymbol_UNI)
        self.menubutton_symbol.menu.add_radiobutton(label='ALGO/USD', command=self.changeSymbol_ALGO)
        self.menubutton_symbol.menu.add_radiobutton(label='COMP/USD', command=self.changeSymbol_COMP)
        self.menubutton_symbol.menu.add_radiobutton(label='BCH/USD', command=self.changeSymbol_BCH)
        self.menubutton_symbol.menu.add_radiobutton(label='YFI/USD', command=self.changeSymbol_YFI)
        self.menubutton_symbol.menu.add_radiobutton(label='XTZ/USD', command=self.changeSymbol_XTZ)
        self.menubutton_symbol.menu.add_radiobutton(label='XRP/USD', command=self.changeSymbol_XRP)
        # Current Symbol Price
        #self.label_current_symbol_market_price = tkinter.Label(self.GUI, font=self.title_font, bg=self.symbol_colors[self.OE.orderSettings['Symbol']], text='$___')
    # Side Input
        self.label_current_side_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Side: ')
        self.label_current_side = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=str(self.OE.orderSettings['Side']))
        self.button_change_side = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=2, text='     Change Side      ', command=self.changeSide)
#   This code is from when we used a menuButton to change the side. However, using a menu button is unnecessary, since there are only 2 choices.
##        self.menubutton_side = tkinter.Menubutton(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
##                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
##                                                   direction='right', relief='raised', text='      Change Side      ')
##        self.menubutton_side.menu = tkinter.Menu(self.menubutton_side, tearoff=0)
##        self.menubutton_side["menu"] = self.menubutton_side.menu
##        self.menubutton_side.menu.add_radiobutton(label='Buy / Long', command=self.changeSide_Buy)
##        self.menubutton_side.menu.add_radiobutton(label='Sell / Short', command=self.changeSide_Sell) 
    # Amount Input
        self.label_current_amount_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Amount: ')
        self.label_current_amount = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.orderSettings['Amount']) + ' ')
        self.entry_change_amount = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_amount = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=12, text='      Update Amount      ', command=self.changeAmount)
    # Price Input
        self.label_current_price_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Price: ')
        self.label_current_price = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' $' + str(self.OE.orderSettings['Price']) + ' ')
        self.entry_change_price = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_price = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=9, text='Use Input', command=self.changePrice)
        self.button_change_price_to_market = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Light Blue'], fg=self.current_exchange_colors['Dark Blue'], \
                                                   activebackground=self.current_exchange_colors['Active Light Blue'], activeforeground=self.current_exchange_colors['Dark Blue'], \
                                                   padx=5, text='Use Market', command=self.changePriceToMarket)
## Create array order widgets

        self.label_array_settings_title = tkinter.Label(self.GUI, font=self.title_font, pady=7, \
                                                        padx=363, text='- Array Order Settings -')
        self.button_lock_end_price = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text=' Lock End Price ', command=self.toggleLockEndPrice)
    # Granularity Input
        self.label_current_granularity_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Granularity: ')
        self.label_current_granularity = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Granularity']) + ' ')
        self.entry_change_granularity = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_granularity = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=9, text='    Update Granularity    ', command=self.changeGranularity)
    # Spread Input
        self.label_current_spread_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Spread: ')
        self.label_current_spread = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Spread']) + ' ')
        self.entry_change_spread = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_spread = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=8, text='       Update Spread       ', command=self.changeSpread)
    # End Price Input
        self.label_current_end_price_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='End Price: ')
        self.label_current_end_price = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['End Price']) + ' ')
        self.entry_change_end_price = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_end_price = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=7, text='     Update End Price     ', command=self.changeEndPrice)
    # Steepness Input
        self.label_current_steepness_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Steepness: ')
        self.label_current_steepness = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Steepness']) + ' ')
        self.entry_change_steepness = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_steepness = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=1, text='      Update Steepness      ', command=self.changeSteepness)
    # Slope Input
        self.label_current_slope_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Slope: ')
        self.label_current_slope = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Slope']) + ' ')
        self.entry_change_slope = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
        self.button_change_slope = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   padx=10, text='        Update Slope        ', command=self.changeSlope)
    # Minimum Order Size Input
        if self.row_17_button == 'Minimum Order Size':
            self.label_current_minimum_order_size_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Minimum Order: ')
            self.label_current_minimum_order_size = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Minimum Order Size']) + ' ')
            self.entry_change_minimum_order_size = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
            self.button_change_minimum_order_size = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                       activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                       padx=6, text='      Update Minimum      ', command=self.changeMinimumOrderSize)
    # Truncation Amount Input
        elif self.row_17_button == 'Truncation Amount':
            self.label_current_truncation_amount_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Truncation Amount: ')
            self.label_current_truncation_amount = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Truncation Amount']) + ' ')
            self.entry_change_truncation_amount = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=16, bd=3)
            self.button_change_truncation_amount = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                       activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                       padx=2, text='      Update Truncation      ', command=self.changeTruncationAmount)
    # Quick Granularity Input
        elif self.row_17_button == 'Quick Granularity':
        # Quick Granularity Intensity
            self.label_current_quick_granularity_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Quick Granularity: ')
            self.label_current_quick_granularity_intensity_title = tkinter.Label(self.GUI, font=self.font_dict[11], bg=self.current_exchange_colors['White'], text='Intensity: ')
            self.label_current_quick_granularity_intensity = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], \
                                                                           text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity Intensity']) + ' ')
            self.entry_change_quick_granularity_intensity = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=5, bd=3)
            self.button_change_quick_granularity = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                       activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                       padx=0, text=' Update Quick Granularity ', command=self.changeQuickGranularity)
            
        # Quick Granularity Start %
            self.label_current_quick_granularity_start_title = tkinter.Label(self.GUI, font=self.font_dict[11], bg=self.current_exchange_colors['White'], text='Start %: ')
            self.label_current_quick_granularity_start = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], \
                                                                       text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity Start %']) + ' ')
            self.entry_change_quick_granularity_start = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=5, bd=3)
        # Quick Granularity End %
            self.label_current_quick_granularity_end_title = tkinter.Label(self.GUI, font=self.font_dict[11], bg=self.current_exchange_colors['White'], text='End %: ')
            self.label_current_quick_granularity_end = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], \
                                                                       text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity End %']) + ' ')
            self.entry_change_quick_granularity_end = tkinter.Entry(self.GUI, font=self.entry_font, justify='center', width=5, bd=3)
    # Style Input
        self.label_current_style_title = tkinter.Label(self.GUI, font=self.label_font, bg=self.current_exchange_colors['White'], text='Style: ')
        self.label_current_style = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Style']) + ' ')
        self.menubutton_style = tkinter.Menubutton(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   direction='right', relief='raised', text='      Change Style      ')
        self.menubutton_style.menu = tkinter.Menu(self.menubutton_style, tearoff=0)
        self.menubutton_style["menu"] =  self.menubutton_style.menu
        self.menubutton_style.menu.add_radiobutton(label='Uniform', command=self.changeStyle_Uniform)
        self.menubutton_style.menu.add_radiobutton(label='Linear', command=self.changeStyle_Linear)
        self.menubutton_style.menu.add_radiobutton(label='Circular', command=self.changeStyle_Circular)
        self.menubutton_style.menu.add_radiobutton(label='Trasposed Circular', command=self.changeStyle_TransposedCircular)
        self.menubutton_style.menu.add_radiobutton(label='Parabolic', command=self.changeStyle_Parabolic)
        self.menubutton_style.menu.add_radiobutton(label='Fibonacci', command=self.changeStyle_Fibonacci)
        self.menubutton_style.menu.add_radiobutton(label='Multiplicative', command=self.changeStyle_Multiplicative)
     # Specific style setting inputs
      # Multiplicative Style
        self.label_current_multiplicative_factor = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Light Blue'], text=' ' + str(self.OE.arrayOrderSettings['Multiplicative Factor']) + ' ')
        self.button_multiplicative_factor_plusPoint01 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+.01', command=self.nudgeMultiplicativeFactor_PlusPoint01)
        self.button_multiplicative_factor_plusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+0.1', command=self.nudgeMultiplicativeFactor_PlusPoint1)
        self.button_multiplicative_factor_minusPoint01 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-.01', command=self.nudgeMultiplicativeFactor_MinusPoint01)
        self.button_multiplicative_factor_minusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-0.1', command=self.nudgeMultiplicativeFactor_MinusPoint1)
        
        
## Create array order parameter display widgets
        
        self.label_order_parameters_spacer_1 = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], text='')
        self.label_min_amount_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text=' Min Amount ')
        self.label_min_amount = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=14, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Lowest Price Order Amount']))
        self.label_max_amount_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text=' Max Amount ')
        self.label_max_amount = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=15, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Highest Price Order Amount']))
        self.label_min_price_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text='   Min Price   ')
        self.label_min_price = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=5, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Lowest Price Order Price']))
        self.label_max_price_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text='   Max Price  ')
        self.label_max_price = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=5, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Highest Price Order Price']))
        self.label_number_of_orders_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text='   # of Orders   ')
        self.label_number_of_orders = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=11, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Number of Orders']))
    # The "Amount" section of the Order Settings displays the total array order amount, so it doesn't need to be repeated here
##        self.label_total_amount_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
##                                                   text=' Total Amount ')
##        self.label_total_amount = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
##                                             padx=11, borderwidth=1, relief='solid', text=str(self.OE.arrayOrderParameters['Total Order Amount']))
        self.label_entry_at_execution_title = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                   text='    Full Entry    ')
        self.label_entry_at_execution = tkinter.Label(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Light Blue'], \
                                             padx=5, borderwidth=1, relief='solid', text=str(round(float(self.OE.arrayOrderParameters['Entry at Full Execution']), 2)))

## Create order creation widgets
    # Preview orders
        self.label_preview_orders_spacer = tkinter.Label(self.GUI, pady=4, bg=self.current_exchange_colors['White'], text='')
        self.button_preview_orders = tkinter.Button(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Dark Blue'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Active Dark Blue'], activeforeground=self.current_exchange_colors['White'], \
                                                   pady=5, text='  Preview Orders  ', command=self.previewOrders)
    # Execute orders
        #self.label_execute_orders_spacer = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], text='')
        self.button_execute_orders = tkinter.Button(self.GUI, font=self.title_font, fg=self.current_exchange_colors['White'], \
                                                   activeforeground=self.current_exchange_colors['White'], \
                                                   pady=5, text='  Execute Orders  ', command=self.createArrayOrder)
    # Cancel all orders
        self.button_cancel_all_orders = tkinter.Button(self.GUI, font=self.title_font, bg=self.current_exchange_colors['Red'], fg=self.current_exchange_colors['White'], \
                                                   activebackground=self.current_exchange_colors['Red'], activeforeground=self.current_exchange_colors['White'], \
                                                   pady=5, text=' Cancel All ', command=self.cancelAllOrders)

## Create active order widgets
        self.label_active_orders_top_spacer = tkinter.Label(self.GUI, pady=5, bg=self.current_exchange_colors['White'], font=self.font_dict['Top Spacer'], text='')
        self.label_active_orders_title = tkinter.Label(self.GUI, font=self.title_font, pady=7, \
                                                        padx=390, text='- Active Orders -')
        self.button_refresh_displayed_orders = tkinter.Button(self.GUI, font=self.button_font, bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text=' Refresh ', command=self.refreshDisplayedOrders)
        self.label_active_orders_bottom_spacer = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], font=self.font_dict['Bottom Spacer'], text='')
        self.label_between_active_orders_spacer = tkinter.Label(self.GUI, bg=self.current_exchange_colors['White'], text='')
        
## Create nudge widgets
    # Amount nudge
        self.button_amount_plus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+100', command=self.nudgeAmount_Plus100)
        self.button_amount_plus300 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+300', command=self.nudgeAmount_Plus300)
        self.button_amount_plus500 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+500', command=self.nudgeAmount_Plus500)
        self.button_amount_plus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1000', command=self.nudgeAmount_Plus1000)
        self.button_amount_plus5000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+5000', command=self.nudgeAmount_Plus5000)
        self.button_amount_minus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-100', command=self.nudgeAmount_Minus100)
        self.button_amount_minus300 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-300', command=self.nudgeAmount_Minus300)
        self.button_amount_minus500 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-500', command=self.nudgeAmount_Minus500)
        self.button_amount_minus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1000', command=self.nudgeAmount_Minus1000)
        self.button_amount_minus5000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-5000', command=self.nudgeAmount_Minus5000)
    # Price nudge
##        self.button_price_plus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='+1', command=self.nudgePrice_Plus1)
        self.button_price_plus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+5', command=self.nudgePrice_Plus5)
        self.button_price_plus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+10', command=self.nudgePrice_Plus10)
##        self.button_price_plus25 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='+25', command=self.nudgePrice_Plus25)
        self.button_price_plus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+50', command=self.nudgePrice_Plus50)
        self.button_price_plus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+100', command=self.nudgePrice_Plus100)
        self.button_price_plus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1000', command=self.nudgePrice_Plus1000)
##        self.button_price_minus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='-1', command=self.nudgePrice_Minus1)
        self.button_price_minus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-5', command=self.nudgePrice_Minus5)
        self.button_price_minus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-10', command=self.nudgePrice_Minus10)
##        self.button_price_minus25 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='-25', command=self.nudgePrice_Minus25)
        self.button_price_minus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-50', command=self.nudgePrice_Minus50)
        self.button_price_minus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-100', command=self.nudgePrice_Minus100)
        self.button_price_minus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1000', command=self.nudgePrice_Minus1000)
    # End Price nudge
##        self.button_end_price_plus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='+1', command=self.nudgeEndPrice_Plus1)
        self.button_end_price_plus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+5', command=self.nudgeEndPrice_Plus5)
        self.button_end_price_plus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+10', command=self.nudgeEndPrice_Plus10)
##        self.button_end_price_plus25 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='+25', command=self.nudgeEndPrice_Plus25)
        self.button_end_price_plus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+50', command=self.nudgeEndPrice_Plus50)
        self.button_end_price_plus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+100', command=self.nudgeEndPrice_Plus100)
        self.button_end_price_plus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1000', command=self.nudgeEndPrice_Plus1000)
##        self.button_end_price_minus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='-1', command=self.nudgeEndPrice_Minus1)
        self.button_end_price_minus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-5', command=self.nudgeEndPrice_Minus5)
        self.button_end_price_minus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-10', command=self.nudgeEndPrice_Minus10)
##        self.button_end_price_minus25 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
##                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
##                                                   text='-25', command=self.nudgeEndPrice_Minus25)
        self.button_end_price_minus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-50', command=self.nudgeEndPrice_Minus50)
        self.button_end_price_minus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-100', command=self.nudgeEndPrice_Minus100)
        self.button_end_price_minus1000 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1000', command=self.nudgeEndPrice_Minus1000)
    # Spread nudge
        self.button_spread_plus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+5', command=self.nudgeSpread_Plus5)
        self.button_spread_plus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+10', command=self.nudgeSpread_Plus10)
        self.button_spread_plus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+50', command=self.nudgeSpread_Plus50)
        self.button_spread_plus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+100', command=self.nudgeSpread_Plus100)
        self.button_spread_plus500 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+500', command=self.nudgeSpread_Plus500)
        self.button_spread_minus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-5', command=self.nudgeSpread_Minus5)
        self.button_spread_minus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-10', command=self.nudgeSpread_Minus10)
        self.button_spread_minus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-50', command=self.nudgeSpread_Minus50)
        self.button_spread_minus100 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-100', command=self.nudgeSpread_Minus100)
        self.button_spread_minus500 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-500', command=self.nudgeSpread_Minus500)
    # Granularity nudge
        self.button_granularity_plusPoint5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+0.5', command=self.nudgeGranularity_PlusPoint5)
        self.button_granularity_plus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1', command=self.nudgeGranularity_Plus1)
        self.button_granularity_plus3 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+3', command=self.nudgeGranularity_Plus3)
        self.button_granularity_plus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+5', command=self.nudgeGranularity_Plus5)
        self.button_granularity_plus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+10', command=self.nudgeGranularity_Plus10)
        self.button_granularity_plus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+50', command=self.nudgeGranularity_Plus50)
        self.button_granularity_minusPoint5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-0.5', command=self.nudgeGranularity_MinusPoint5)
        self.button_granularity_minus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1', command=self.nudgeGranularity_Minus1)
        self.button_granularity_minus3 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-3', command=self.nudgeGranularity_Minus3)
        self.button_granularity_minus5 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[20], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-5', command=self.nudgeGranularity_Minus5)
        self.button_granularity_minus10 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[25], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-10', command=self.nudgeGranularity_Minus10)
        self.button_granularity_minus50 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[30], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-50', command=self.nudgeGranularity_Minus50)
    #Steepness nudge
        self.button_steepness_plusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+0.1', command=self.nudgeSteepness_PlusPoint1)
        self.button_steepness_plus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1', command=self.nudgeSteepness_Plus1)
        self.button_steepness_minusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-0.1', command=self.nudgeSteepness_MinusPoint1)
        self.button_steepness_minus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1', command=self.nudgeSteepness_Minus1)
    #Slope nudge
        self.button_slope_plusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+0.1', command=self.nudgeSlope_PlusPoint1)
        self.button_slope_plus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='+1', command=self.nudgeSlope_Plus1)
        self.button_slope_double = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.green_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Green'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='2x', command=self.nudgeSlope_Double)
        self.button_slope_minusPoint1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[5], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-0.1', command=self.nudgeSlope_MinusPoint1)
        self.button_slope_minus1 = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[10], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='-1', command=self.nudgeSlope_Minus1)
        self.button_slope_half = tkinter.Button(self.GUI, font=self.nudge_font, bg=self.red_colors[15], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Red'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='1/2', command=self.nudgeSlope_Half)
    
    # Profile buttons
        self.button_profile_I = tkinter.Button(self.GUI, font=self.font_dict[14], bg=self.my_colors['Teal'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Teal'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='  I  ', command=self.loadProfile_I)
        self.button_save_profile_I = tkinter.Button(self.GUI, font=self.font_dict[7], bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='Save', command=self.saveProfile_I)
        self.button_profile_II = tkinter.Button(self.GUI, font=self.font_dict[14], bg=self.my_colors['Salmon'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Salmon'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='  II  ', command=self.loadProfile_II)
        self.button_save_profile_II = tkinter.Button(self.GUI, font=self.font_dict[7], bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='Save', command=self.saveProfile_II)
        self.button_profile_III = tkinter.Button(self.GUI, font=self.font_dict[14], bg=self.my_colors['Light Yellow'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Light Yellow'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='  III  ', command=self.loadProfile_III)
        self.button_save_profile_III = tkinter.Button(self.GUI, font=self.font_dict[7], bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='Save', command=self.saveProfile_III)
        self.button_profile_IV = tkinter.Button(self.GUI, font=self.font_dict[14], bg=self.my_colors['Sky Blue'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Sky Blue'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='  IV  ', command=self.loadProfile_IV)
        self.button_save_profile_IV = tkinter.Button(self.GUI, font=self.font_dict[7], bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='Save', command=self.saveProfile_IV)
        self.button_profile_V = tkinter.Button(self.GUI, font=self.font_dict[14], bg=self.my_colors['Light Orange'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.my_colors['Light Orange'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='  V  ', command=self.loadProfile_V)
        self.button_save_profile_V = tkinter.Button(self.GUI, font=self.font_dict[7], bg=self.current_exchange_colors['Gray'], fg=self.current_exchange_colors['Black'], \
                                                   activebackground=self.current_exchange_colors['Gray'], activeforeground=self.current_exchange_colors['Black'], \
                                                   text='Save', command=self.saveProfile_V)

### Widgets added to grid
        
## Add general widgets to grid

    # Profile widgets added to grid
        self.button_profile_I.grid(column=1, row=self.layoutDict['Profiles'])
        self.button_save_profile_I.grid(column=1, row=self.layoutDict['Profiles'] + 1)
        self.button_profile_II.grid(padx=(0,50), column=2, row=self.layoutDict['Profiles'])
        self.button_save_profile_II.grid(padx=(0,50), column=2, row=self.layoutDict['Profiles'] + 1)
        self.button_profile_III.grid(columnspan=5, column=1, row=self.layoutDict['Profiles'])
        self.button_save_profile_III.grid(columnspan=5, column=1, row=self.layoutDict['Profiles'] + 1)
        self.button_profile_IV.grid(padx=(0,20), columnspan=3, column=3, row=self.layoutDict['Profiles'])
        self.button_save_profile_IV.grid(padx=(0,20), columnspan=3, column=3, row=self.layoutDict['Profiles'] + 1)
        self.button_profile_V.grid(columnspan=1, column=5, row=self.layoutDict['Profiles'])
        self.button_save_profile_V.grid(columnspan=1, column=5, row=self.layoutDict['Profiles'] + 1)
    # Account settings section title added to grid
        self.label_order_settings_top_spacer.grid(columnspan=6, column=1, row=3)
        self.label_general_settings_title.grid(columnspan=6, column=1, row=4)
        self.button_auto_preview.grid(columnspan=2, column=5, row=4)
        self.label_order_settings_bottom_spacer.grid(columnspan=6, column=1, row=5)
    # Account widgets added to grid
        self.label_current_account_title.grid(column=1, row=self.layoutDict['Account'])
        self.label_current_account.grid(columnspan=2, column=2, row=self.layoutDict['Account'])
        self.menubutton_account.grid(columnspan=1, column=4, row=self.layoutDict['Account'])
    # Symbol widgets added to grid
        self.label_current_symbol_title.grid(column=1, row=self.layoutDict['Symbol'])
        self.label_current_symbol.grid(columnspan=2, column=2, row=self.layoutDict['Symbol'])
        self.menubutton_symbol.grid(columnspan=1, column=4, row=self.layoutDict['Symbol'])
        #self.label_current_symbol_market_price.grid(columnspan=2, column=5, row=self.layoutDict['Symbol'])
        self.label_last_action.grid(columnspan=2, column=5, row=self.layoutDict['Symbol'])
    # Side widgets added to grid
        self.label_current_side_title.grid(column=1, row=self.layoutDict['Side'])
        self.label_current_side.grid(columnspan=2, column=2, row=self.layoutDict['Side'])
        self.button_change_side.grid(column=4, row=self.layoutDict['Side'])
#   This line is from when we used a menuButton to change the side. However, using a menu button is unnecessary, since there are only 2 choices.
##        self.menubutton_side.grid(column=4, row=self.layoutDict['Side'])
    # Amount widgets added to grid
        self.label_current_amount_title.grid(column=1, row=self.layoutDict['Amount'])
        self.label_current_amount.grid(columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_change_amount.grid(columnspan=2, column=5, row=self.layoutDict['Amount'])
        self.entry_change_amount.grid(column=4, row=self.layoutDict['Amount'])
      # Nudge amount up
        self.button_amount_plus100.grid(padx=(5 + 25 * len(str(self.OE.orderSettings['Amount'])), 0), columnspan=2, column=2, row=self.layoutDict['Amount'])
        #self.button_amount_plus300.grid(padx=(85 + 25 * len(str(self.OE.orderSettings['Amount'])), 0), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_plus500.grid(padx=(87 + 25 * len(str(self.OE.orderSettings['Amount'])), 0), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_plus1000.grid(padx=(177 + 25 * len(str(self.OE.orderSettings['Amount'])), 0), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_plus5000.grid(padx=(273 + 25 * len(str(self.OE.orderSettings['Amount'])), 0), columnspan=2, column=2, row=self.layoutDict['Amount'])
      # Nudge amount down
        self.button_amount_minus100.grid(padx=(0, 4 + 25 * len(str(self.OE.orderSettings['Amount']))), columnspan=2, column=2, row=self.layoutDict['Amount'])
        #self.button_amount_minus300.grid(padx=(0, 51 + 25 * len(str(self.OE.orderSettings['Amount']))), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_minus500.grid(padx=(0, 79 + 25 * len(str(self.OE.orderSettings['Amount']))), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_minus1000.grid(padx=(0, 162 + 25 * len(str(self.OE.orderSettings['Amount']))), columnspan=2, column=2, row=self.layoutDict['Amount'])
        self.button_amount_minus5000.grid(padx=(0, 252 + 25 * len(str(self.OE.orderSettings['Amount']))), columnspan=2, column=2, row=self.layoutDict['Amount'])
    # Price widgets added to grid
        self.label_current_price_title.grid(column=1, row=self.layoutDict['Price'])
        self.label_current_price.grid(columnspan=2, column=2, row=self.layoutDict['Price'])
        self.entry_change_price.grid(column=4, row=self.layoutDict['Price'])
        self.button_change_price.grid(column=5, row=self.layoutDict['Price'])
        self.button_change_price_to_market.grid(column=6, row=self.layoutDict['Price'])
      # Nudge price up
        #self.button_price_plus1.grid(padx=(4 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_plus5.grid(padx=(5 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_plus10.grid(padx=(66 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        #self.button_price_plus25.grid(padx=(115 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_plus50.grid(padx=(134 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_plus100.grid(padx=(209 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_plus1000.grid(padx=(298 + 22 * len(str(self.OE.orderSettings['Price'])), 0), columnspan=2, column=2, row=self.layoutDict['Price'])
      # Nudge price down
        #self.button_price_minus1.grid(padx=(0, 1 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_minus5.grid(padx=(0, 1 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_minus10.grid(padx=(0, 56 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        #self.button_price_minus25.grid(padx=(0, 100 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_minus50.grid(padx=(0, 118 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_minus100.grid(padx=(0, 187 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])
        self.button_price_minus1000.grid(padx=(0, 270 + 22 * len(str(self.OE.orderSettings['Price']))), columnspan=2, column=2, row=self.layoutDict['Price'])


## Add array widgets to grid       

      #Array order settings section title added to grid
        self.label_array_settings_title.grid(pady=5, columnspan=6, column=1, row=11)
        self.button_lock_end_price.grid(columnspan=2, column=5, row=11)
    # Granularity widgets added to grid
        self.label_current_granularity_title.grid(column=1, row=self.layoutDict['Granularity'])
        self.label_current_granularity.grid(columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_change_granularity.grid(columnspan=2, column=5, row=self.layoutDict['Granularity'])
        self.entry_change_granularity.grid(column=4, row=self.layoutDict['Granularity'])
      # Nudge granularity up
        self.button_granularity_plusPoint5.grid(padx=(4 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_plus1.grid(padx=(67 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_plus3.grid(padx=(121 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_plus5.grid(padx=(176 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_plus10.grid(padx=(236 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_plus50.grid(padx=(305 + 100, 0), columnspan=2, column=2, row=self.layoutDict['Granularity'])
      # Nudge granularity down
        self.button_granularity_minusPoint5.grid(padx=(0, 1 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_minus1.grid(padx=(0, 59 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_minus3.grid(padx=(0, 108 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_minus5.grid(padx=(0, 155 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_minus10.grid(padx=(0, 211 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
        self.button_granularity_minus50.grid(padx=(0, 273 + 100), columnspan=2, column=2, row=self.layoutDict['Granularity'])
    # Spread widgets added to grid
        self.label_current_spread_title.grid(column=1, row=self.layoutDict['Spread'])
        self.label_current_spread.grid(columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_change_spread.grid(columnspan=2, column=5, row=self.layoutDict['Spread'])
        self.entry_change_spread.grid(column=4, row=self.layoutDict['Spread'])
      # Nudge spread up
        self.button_spread_plus5.grid(padx=(120, 0), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_plus10.grid(padx=(63 + 120, 0), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_plus50.grid(padx=(133 + 120, 0), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_plus100.grid(padx=(211 + 120, 0), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_plus500.grid(padx=(294 + 120, 0), columnspan=2, column=2, row=self.layoutDict['Spread'])
      # Nudge spread down
        self.button_spread_minus5.grid(padx=(0, 120), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_minus10.grid(padx=(0, 56 + 120), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_minus50.grid(padx=(0, 118 + 120), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_minus100.grid(padx=(0, 186 + 120), columnspan=2, column=2, row=self.layoutDict['Spread'])
        self.button_spread_minus500.grid(padx=(0, 263 + 120), columnspan=2, column=2, row=self.layoutDict['Spread'])
    # End Price widgets added to grid
        self.label_current_end_price_title.grid(column=1, row=self.layoutDict['End Price'])
        self.label_current_end_price.grid(columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_change_end_price.grid(columnspan=2, column=5, row=self.layoutDict['End Price'])
        self.entry_change_end_price.grid(column=4, row=self.layoutDict['End Price'])
      # Nudge End Price up
        #self.button_end_price_plus1.grid(padx=(4 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_plus5.grid(padx=(5 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_plus10.grid(padx=(66 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        #self.button_end_price_plus25.grid(padx=(115 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_plus50.grid(padx=(134 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_plus100.grid(padx=(209 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_plus1000.grid(padx=(298 + 22 * len(str(self.OE.arrayOrderSettings['End Price'])), 0), columnspan=2, column=2, row=self.layoutDict['End Price'])
      # Nudge End Price down
        #self.button_end_price_minus1.grid(padx=(0, 1 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_minus5.grid(padx=(0, 1 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_minus10.grid(padx=(0, 56 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        #self.button_end_price_minus25.grid(padx=(0, 100 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_minus50.grid(padx=(0, 118 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_minus100.grid(padx=(0, 187 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
        self.button_end_price_minus1000.grid(padx=(0, 270 + 22 * len(str(self.OE.arrayOrderSettings['End Price']))), columnspan=2, column=2, row=self.layoutDict['End Price'])
    # Steepness widgets added to grid
        self.label_current_steepness_title.grid(column=1, row=self.layoutDict['Steepness'])
        self.label_current_steepness.grid(columnspan=2, column=2, row=self.layoutDict['Steepness'])
        self.button_change_steepness.grid(columnspan=2, column=5, row=self.layoutDict['Steepness'])
        self.entry_change_steepness.grid(column=4, row=self.layoutDict['Steepness'])
      # Nudge Steepness up
        self.button_steepness_plusPoint1.grid(padx=(59 + 35, 0), columnspan=2, column=2, row=self.layoutDict['Steepness'])
        self.button_steepness_plus1.grid(padx=(123 + 35, 0), columnspan=2, column=2, row=self.layoutDict['Steepness'])
      # Nudge Steepness down
        self.button_steepness_minusPoint1.grid(padx=(0, 56 + 35), columnspan=2, column=2, row=self.layoutDict['Steepness'])
        self.button_steepness_minus1.grid(padx=(0, 114 + 35), columnspan=2, column=2, row=self.layoutDict['Steepness'])
    # Slope widgets added to grid
        self.label_current_slope_title.grid(column=1, row=self.layoutDict['Slope'])
        self.label_current_slope.grid(columnspan=2, column=2, row=self.layoutDict['Slope'])
        self.button_change_slope.grid(columnspan=2, column=5, row=self.layoutDict['Slope'])
        self.entry_change_slope.grid(column=4, row=self.layoutDict['Slope'])
      # Nudge Slope up
        self.button_slope_plusPoint1.grid(padx=(59 + 35, 0), columnspan=2, column=2, row=self.layoutDict['Slope'])
        self.button_slope_plus1.grid(padx=(123 + 35, 0), columnspan=2, column=2, row=self.layoutDict['Slope'])
        self.button_slope_double.grid(padx=(175 + 35, 0), columnspan=2, column=2, row=self.layoutDict['Slope'])
      # Nudge Slope down
        self.button_slope_minusPoint1.grid(padx=(0, 56 + 35), columnspan=2, column=2, row=self.layoutDict['Slope'])
        self.button_slope_minus1.grid(padx=(0, 114 + 35), columnspan=2, column=2, row=self.layoutDict['Slope'])
        self.button_slope_half.grid(padx=(0, 168 + 35), columnspan=2, column=2, row=self.layoutDict['Slope'])
    # Minimum Order Size widgets added to grid
        if self.row_17_button == 'Minimum Order Size':
            self.label_current_minimum_order_size_title.grid(column=1, row=self.layoutDict['Minimum Order Size'])
            self.label_current_minimum_order_size.grid(columnspan=2, column=2, row=self.layoutDict['Minimum Order Size'])
            self.button_change_minimum_order_size.grid(columnspan=2, column=5, row=self.layoutDict['Minimum Order Size'])
            self.entry_change_minimum_order_size.grid(column=4, row=self.layoutDict['Minimum Order Size'])
    # Truncation Amount widgets added to grid
        elif self.row_17_button == 'Truncation Amount':
            self.label_current_truncation_amount_title.grid(column=1, row=self.layoutDict['Truncation Amount'])
            self.label_current_truncation_amount.grid(columnspan=2, column=2, row=self.layoutDict['Truncation Amount'])
            self.button_change_truncation_amount.grid(columnspan=2, column=5, row=self.layoutDict['Truncation Amount'])
            self.entry_change_truncation_amount.grid(column=4, row=self.layoutDict['Truncation Amount'])
    # Quick Granularity widgets added to grid
        elif self.row_17_button == 'Quick Granularity':
            self.label_current_quick_granularity_title.grid(column=1, row=self.layoutDict['Quick Granularity'])
            self.button_change_quick_granularity.grid(columnspan=2, column=5, row=self.layoutDict['Quick Granularity'])
        # Start %
            self.label_current_quick_granularity_start_title.grid(padx=(0, 350), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.label_current_quick_granularity_start.grid(padx=(0, 236), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.entry_change_quick_granularity_start.grid(padx=(0, 105), column=4, row=self.layoutDict['Quick Granularity'])
        # Intensity
            self.label_current_quick_granularity_intensity_title.grid(padx=(0, 60), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.label_current_quick_granularity_intensity.grid(padx=(60, 0), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.entry_change_quick_granularity_intensity.grid(column=4, row=self.layoutDict['Quick Granularity'])
        # End %
            self.label_current_quick_granularity_end_title.grid(padx=(236, 0), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.label_current_quick_granularity_end.grid(padx=(350, 0), columnspan=2, column=2, row=self.layoutDict['Quick Granularity'])
            self.entry_change_quick_granularity_end.grid(padx=(105, 0), column=4, row=self.layoutDict['Quick Granularity'])
    # Style widgets added to grid
        self.label_current_style_title.grid(column=1, row=self.layoutDict['Style'])
        self.label_current_style.grid(columnspan=2, column=2, row=self.layoutDict['Style'])
        self.menubutton_style.grid(columnspan=1, column=4, row=self.layoutDict['Style'])
        if self.OE.arrayOrderSettings['Style'] == 'Multiplicative':
        # Multiplicative Factor widgets added to grid
            self.label_current_style.grid(columnspan=1, column=2, row=self.layoutDict['Style'])
            self.label_current_multiplicative_factor.grid(columnspan=3, column=2, row=self.layoutDict['Style'])
          # Nudge Multiplicative Factor up
            self.button_multiplicative_factor_plusPoint01.grid(padx=(54 + 22 * 1.5, 0), \
                                                         columnspan=3, column=2, row=self.layoutDict['Style'])
            self.button_multiplicative_factor_plusPoint1.grid(padx=(129 + 22 * 1.5, 0), \
                                                              columnspan=3, column=2, row=self.layoutDict['Style'])
          # Nudge Multiplicative Factor down
            self.button_multiplicative_factor_minusPoint01.grid(padx=(0, 52 + 22 * 1.5), \
                                                          columnspan=3, column=2, row=self.layoutDict['Style'])
            self.button_multiplicative_factor_minusPoint1.grid(padx=(0, 119 + 22 * 1.5), \
                                                               columnspan=3, column=2, row=self.layoutDict['Style'])
            
    

## Add parameter display widgets to grid
        
    # Parameter widgets added to grid
        self.label_order_parameters_spacer_1.grid(columnspan=6, column=1, row=31)
        self.label_min_amount_title.grid(column=1, row=32)
        self.label_min_amount.grid(column=1, row=33)
        self.label_max_amount_title.grid(padx=(0, 100), columnspan=1, column=2, row=32)
        self.label_max_amount.grid(padx=(0, 100), columnspan=1, column=2, row=33)
        # Removed due to redundancy
##        self.label_total_amount_title.grid(column=4, row=32)
##        self.label_total_amount.grid(column=4, row=33)
##        self.label_order_parameters_spacer_2.grid(columnspan=6, column=1, row=34)
        self.label_min_price_title.grid(padx=(00,0), columnspan=2, column=2, row=32)
        self.label_min_price.grid(padx=(00,0), columnspan=2, column=2, row=33)
        self.label_max_price_title.grid(padx=(30,0), columnspan=1, column=3, row=32)
        self.label_max_price.grid(padx=(30,0), columnspan=1, column=3, row=33)
        self.label_number_of_orders_title.grid(columnspan=1, column=4, row=32)
        self.label_number_of_orders.grid(columnspan=1, column=4, row=33)
        self.label_entry_at_execution_title.grid(columnspan=2, column=5, row=32)
        self.label_entry_at_execution.grid(columnspan=2, column=5, row=33)
        

## Add order creation widgets to grid
    # Preview orders
        self.label_preview_orders_spacer.grid(columnspan=6, column=1, row=41)
        self.button_preview_orders.grid(columnspan=2, column=1, row=42)
    # Execute orders
        #self.label_execute_orders_spacer.grid(columnspan=6, column=1, row=43)
        self.button_execute_orders.grid(columnspan=4, column=2, row=42)
    # Cancel all orders
        self.button_cancel_all_orders.grid(columnspan=3, column=4, row=42)

## Add active order widgets to grid
        self.label_active_orders_top_spacer.grid(columnspan=6, column=1, row=50)
        self.label_active_orders_title.grid(columnspan=6, column=1, row=51)
        self.button_refresh_displayed_orders.grid(columnspan=2, column=5, row=51)
        self.label_active_orders_bottom_spacer.grid(columnspan=6, column=1, row=52)
        self.label_between_active_orders_spacer.grid(columnspan=6, column=1, row=60)
        

        self.changeSide()
        self.GUI.geometry(self.window_size)
        self.GUI.mainloop()

    def changeGranularity(self, *args):
        try:
            granularity_input = self.OE.checkGranularityInput(args[0])
        except:
            try:
                granularity_input = self.OE.checkGranularityInput(self.entry_change_granularity.get())
            except:
                print('ERROR! Invalid value input for Granularity.')
                granularity_input = False
        if granularity_input:
            self.OE.arrayOrderSettings['Granularity'] = float(granularity_input)
            self.entry_change_granularity.delete(0, 'end')
            self.label_current_granularity.config(text=' ' + str(self.OE.arrayOrderSettings['Granularity']) + ' ')
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Granularity set to ' + str(self.OE.arrayOrderSettings['Granularity']))
            self.label_last_action.config(text='[   Just changed Granularity   ]')
        else:
            print('ERROR! Invalid value input for Granularity.')
        

    def changeSpread(self, *args):
        try:
            spread_input = self.OE.checkSpreadInput(args[0])
        except:
            try:
                spread_input = self.OE.checkSpreadInput(self.entry_change_spread.get())
            except:
                print('ERROR! Invalid value input for Spread.')
                spread_input = False
        if spread_input:
        # Attempts to update the End Price
            if self.OE.orderSettings['Side'] == 'buy':
                new_end_price = self.OE.orderSettings['Price'] - spread_input
            else:
                new_end_price = self.OE.orderSettings['Price'] + spread_input
            try:
                new_end_price = self.OE.checkEndPriceInput(new_end_price)
            except:
                print('ERROR! The value input for Spread makes the End Price invalid.')
                new_end_price = False
            if new_end_price:
                self.OE.arrayOrderSettings['Spread'] = float(spread_input)
                self.entry_change_spread.delete(0, 'end')
                self.label_current_spread.config(text=' $' + str(self.OE.arrayOrderSettings['Spread']) + ' ')
                self.OE.arrayOrderSettings['End Price'] = float(new_end_price)
                self.label_current_end_price.config(text=' $' + str(self.OE.arrayOrderSettings['End Price']) + ' ')                
                if self.auto_preview:
                    self.updateParameterLabels()
                else:
                    self.settings_have_changed_since_last_preview = True
                    self.darkenArrayParameters()
                print('Spread set to ' + str(self.OE.arrayOrderSettings['Spread']))
                self.label_last_action.config(text='[   Just changed Spread   ]')
        else:
            print('ERROR! Invalid value input for Spread.')

    def changeEndPrice(self, *args):
        try:
            end_price_input = self.OE.checkEndPriceInput(args[0])
        except:
            try:
                end_price_input = self.OE.checkEndPriceInput(self.entry_change_end_price.get())
            except:
                print('ERROR! Invalid value input for End Price.')
                end_price_input = False
        if end_price_input:          
        # Attempts to update the Spread
            if self.OE.orderSettings['Side'] == 'buy':
                new_spread = self.OE.orderSettings['Price'] - end_price_input
            else:
                new_spread = end_price_input - self.OE.orderSettings['Price']
            try:
                new_spread = self.OE.checkSpreadInput(new_spread)
            except:
                print('ERROR! The value input for End Price makes the Spread invalid.')
                new_spread = False
            if new_spread:
                self.OE.arrayOrderSettings['End Price'] = float(end_price_input)
                self.entry_change_end_price.delete(0, 'end')
                self.label_current_end_price.config(text=' $' + str(self.OE.arrayOrderSettings['End Price']) + ' ')
                self.OE.arrayOrderSettings['Spread'] = float(new_spread)
                self.label_current_spread.config(text=' $' + str(self.OE.arrayOrderSettings['Spread']) + ' ')
                if self.auto_preview:
                    self.updateParameterLabels()
                else:
                    self.settings_have_changed_since_last_preview = True
                    self.darkenArrayParameters()
                print('End Price set to ' + str(self.OE.arrayOrderSettings['End Price']))
                self.label_last_action.config(text='[   Just changed End Price   ]')
        else:
            print('ERROR! Invalid value input for End Price.')
        

    def changeSteepness(self, *args):
        try:
            steepness_input = self.OE.checkSteepnessInput(args[0])
        except:
            try:
                steepness_input = self.OE.checkSteepnessInput(self.entry_change_steepness.get())
            except:
                print('ERROR! Invalid value input for Steepness.')
                steepness_input = False
        if steepness_input or (type(steepness_input) == float):
            self.OE.arrayOrderSettings['Steepness'] = float(steepness_input)
            self.entry_change_steepness.delete(0, 'end')
            self.label_current_steepness.config(text=' ' + str(self.OE.arrayOrderSettings['Steepness']) + ' ')
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Steepness degree set to ' + str(self.OE.arrayOrderSettings['Steepness']))
            self.label_last_action.config(text='[   Just changed Steepness   ]')
        else:
            print('ERROR! Invalid value input for Steepness.')

    def changeSlope(self, *args):
        try:
            slope_input = self.OE.checkSlopeInput(args[0])
        except:
            try:
                slope_input = self.OE.checkSlopeInput(self.entry_change_slope.get())
            except:
                print('ERROR! Invalid value input for Slope.')
                slope_input = False
        if slope_input or (type(slope_input) == float):
            self.OE.arrayOrderSettings['Slope'] = float(slope_input)
            self.entry_change_slope.delete(0, 'end')
            self.label_current_slope.config(text=' ' + str(self.OE.arrayOrderSettings['Slope']) + ' ')
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Slope set to ' + str(self.OE.arrayOrderSettings['Slope']))
            self.label_last_action.config(text='[   Just changed Slope   ]')
        else:
            print('ERROR! Invalid value input for Slope.')
        
        

    def changeMinimumOrderSize(self):
        try:
            minimum_order_size_input = self.OE.checkMinimumOrderSizeInput(self.entry_change_minimum_order_size.get())
            if minimum_order_size_input:
                self.OE.arrayOrderSettings['Minimum Order Size'] = int(minimum_order_size_input)
                self.entry_change_minimum_order_size.delete(0, 'end')
                self.label_current_minimum_order_size.config(text=' ' + str(self.OE.arrayOrderSettings['Minimum Order Size']) + ' ')
                if self.auto_preview:
                    self.updateParameterLabels()
                else:
                    self.settings_have_changed_since_last_preview = True
                    self.darkenArrayParameters()
                print('Minimum Order Size set to ' + str(self.OE.arrayOrderSettings['Minimum Order Size']))
                self.label_last_action.config(text='[  Just changed Minimum Order  ]')
            else:
                print('ERROR! Invalid value input for Minimum Order Size.')
        except:
            print('ERROR! Invalid value input for Minimum Order Size.')


    def changeTruncationAmount(self):
        try:
            truncation_amount_input = self.OE.checkTruncationAmountInput(self.entry_change_truncation_amount.get())
            if truncation_amount_input:
                self.OE.arrayOrderSettings['Truncation Amount'] = int(truncation_amount_input)
                self.entry_change_truncation_amount.delete(0, 'end')
                self.label_current_truncation_amount.config(text=' ' + str(self.OE.arrayOrderSettings['Truncation Amount']) + ' ')
                if self.auto_preview:
                    self.updateParameterLabels()
                else:
                    self.settings_have_changed_since_last_preview = True
                    self.darkenArrayParameters()
                print('Truncation Amount set to ' + str(self.OE.arrayOrderSettings['Truncation Amount']))
                self.label_last_action.config(text='[  Just changed Truncation Amount  ]')
            else:
                print('ERROR! Invalid value input for Truncation Amount.')
        except:
            print('ERROR! Invalid value input for Truncation Amount.')


    def changeQuickGranularity(self):
    # Intensity
        quick_granularity_intensity_input = self.entry_change_quick_granularity_intensity.get()
        if quick_granularity_intensity_input != '':
            try:
                quick_granularity_intensity_input = self.OE.checkQuickGranularityIntensityInput(quick_granularity_intensity_input)
                if type(quick_granularity_intensity_input) == int:
                    self.OE.arrayOrderSettings['Quick Granularity Intensity'] = int(quick_granularity_intensity_input)
                    self.entry_change_quick_granularity_intensity.delete(0, 'end')
                    self.label_current_quick_granularity_intensity.config(text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity Intensity']) + ' ')
                    if self.auto_preview:
                        self.updateParameterLabels()
                    else:
                        self.settings_have_changed_since_last_preview = True
                        self.darkenArrayParameters()
                    print('Quick Granularity Intensity set to ' + str(self.OE.arrayOrderSettings['Quick Granularity Intensity']))
                    self.label_last_action.config(text='[  Just changed QG Intensity  ]')
                else:
                    print('ERROR! Invalid value input for Quick Granularity Intensity.')
            except:
                print('ERROR! Invalid value input for Quick Granularity Intensity.')
    # Start %
        quick_granularity_start_input = self.entry_change_quick_granularity_start.get()
        if quick_granularity_start_input != '':
            try:
                quick_granularity_start_input = self.OE.checkQuickGranularityStartInput(quick_granularity_start_input)
                if type(quick_granularity_start_input) == int or type(quick_granularity_start_input) == float:
                    self.OE.arrayOrderSettings['Quick Granularity Start %'] = float(quick_granularity_start_input)
                    self.entry_change_quick_granularity_start.delete(0, 'end')
                    self.label_current_quick_granularity_start.config(text=' ' + str(100 * self.OE.arrayOrderSettings['Quick Granularity Start %']) + '% ')
                    if self.auto_preview:
                        self.updateParameterLabels()
                    else:
                        self.settings_have_changed_since_last_preview = True
                        self.darkenArrayParameters()
                    print('Quick Granularity Start % set to ' + str(self.OE.arrayOrderSettings['Quick Granularity Start %']))
                    self.label_last_action.config(text='[  Just changed QG Start  ]')
                else:
                    print('ERROR! Invalid value input for Quick Granularity Start %.')
            except:
                print('ERROR! Invalid value input for Quick Granularity Start %.')
    # End %
        quick_granularity_end_input = self.entry_change_quick_granularity_end.get()
        if quick_granularity_end_input != '':
            try:
                quick_granularity_end_input = self.OE.checkQuickGranularityEndInput(quick_granularity_end_input)
                if type(quick_granularity_end_input) == int or type(quick_granularity_end_input) == float:
                    self.OE.arrayOrderSettings['Quick Granularity End %'] = float(quick_granularity_end_input)
                    self.entry_change_quick_granularity_end.delete(0, 'end')
                    self.label_current_quick_granularity_end.config(text=' ' + str(100 * self.OE.arrayOrderSettings['Quick Granularity End %']) + '% ')
                    if self.auto_preview:
                        self.updateParameterLabels()
                    else:
                        self.settings_have_changed_since_last_preview = True
                        self.darkenArrayParameters()
                    print('Quick Granularity End % set to ' + str(self.OE.arrayOrderSettings['Quick Granularity End %']))
                    self.label_last_action.config(text='[  Just changed QG End  ]')
                else:
                    print('ERROR! Invalid value input for Quick Granularity End %.')
            except:
                print('ERROR! Invalid value input for Quick Granularity End %.')
    

    def changeStyle(self, style_input):
        style_input = self.OE.checkStyleInput(style_input)
        if style_input:
            original_style = self.OE.arrayOrderSettings['Style']
            self.OE.arrayOrderSettings['Style'] = str(style_input)
            print('Style set to ' + str(self.OE.arrayOrderSettings['Style']))
        # This adds buttons if the style has an extra setting that can be modified
            if style_input == 'Multiplicative' and not(self.multiplicative_style):
                self.multiplicative_style = True
                self.label_current_style.grid(columnspan=1, column=2, row=self.layoutDict['Style'])
                self.label_current_multiplicative_factor.grid(columnspan=3, column=2, row=self.layoutDict['Style'])
              # Nudge Multiplicative Factor up
                self.button_multiplicative_factor_plusPoint01.grid(padx=(54 + 22 * 1.5, 0), \
                                                             columnspan=3, column=2, row=self.layoutDict['Style'])
                self.button_multiplicative_factor_plusPoint1.grid(padx=(129 + 22 * 1.5, 0), \
                                                                  columnspan=3, column=2, row=self.layoutDict['Style'])
              # Nudge Multiplicative Factor down
                self.button_multiplicative_factor_minusPoint01.grid(padx=(0, 52 + 22 * 1.5), \
                                                              columnspan=3, column=2, row=self.layoutDict['Style'])
                self.button_multiplicative_factor_minusPoint1.grid(padx=(0, 119 + 22 * 1.5), \
                                                                   columnspan=3, column=2, row=self.layoutDict['Style'])
        # This removes the Multiplicative Factor nudge buttons if the chosen style is not Multiplicative
            elif style_input != 'Multiplicative' and self.multiplicative_style:
                self.multiplicative_style = False
                self.label_current_style.grid(columnspan=2, column=2, row=self.layoutDict['Style'])
                self.label_current_multiplicative_factor.grid_forget()
                self.button_multiplicative_factor_plusPoint1.grid_forget()
                self.button_multiplicative_factor_plusPoint01.grid_forget()
                self.button_multiplicative_factor_minusPoint1.grid_forget()
                self.button_multiplicative_factor_minusPoint01.grid_forget()
            
            self.label_last_action.config(text='[   Just changed Style   ]')
            self.label_current_style.config(text=' ' + str(self.OE.arrayOrderSettings['Style']) + ' ')
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
        else:
            print('ERROR! Invalid value input for Style.')

    def changeMultiplicativeFactor(self, *args):
        try:
            multiplicative_factor_input = self.OE.checkMultiplicativeFactorInput(args[0])
        except:
            try:
                multiplicative_factor_input = self.OE.checkMultiplicativeFactorInput(self.entry_change_multiplicative_factor.get())
            except:
                print('ERROR! Invalid value input for Multiplicative Factor.')
                multiplicative_factor_input = False
        if multiplicative_factor_input or (type(multiplicative_factor_input) == float):
            self.OE.arrayOrderSettings['Multiplicative Factor'] = float(multiplicative_factor_input)
            self.label_current_multiplicative_factor.config(text=' ' + str(self.OE.arrayOrderSettings['Multiplicative Factor']) + ' ')
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Multiplicative Factor degree set to ' + str(self.OE.arrayOrderSettings['Multiplicative Factor']))
            self.label_last_action.config(text='[   Just changed Multiplicative Factor   ]')
        else:
            print('ERROR! Invalid value input for Multiplicative Factor.')
        

    def changeStyle_Uniform(self):
        self.changeStyle('Uniform')
        
    def changeStyle_Linear(self):
        self.changeStyle('Linear')
        
    def changeStyle_Circular(self):
        self.changeStyle('Circular')
        
    def changeStyle_TransposedCircular(self):
        self.changeStyle('Transposed Circular')
        
    def changeStyle_Parabolic(self):
        self.changeStyle('Parabolic')

    def changeStyle_Fibonacci(self):
        self.changeStyle('Fibonacci')

    def changeStyle_Multiplicative(self):
        self.changeStyle('Multiplicative')

    def changeSymbol(self, symbol_input):
        symbol_input = self.OE.checkSymbolInput(symbol_input)
        if symbol_input:
            self.OE.orderSettings['Symbol'] = str(symbol_input)
            self.label_current_symbol.config(text=' ' + str(symbol_input) + ' ', bg=self.symbol_colors[self.OE.orderSettings['Symbol']])
            #self.label_current_symbol_price.config(text='$' + str(self.OE.CTE.exchange.fetchTicker(self.OE.orderSettings['Symbol'])['bid']), bg=self.symbol_colors[self.OE.orderSettings['Symbol']])
            self.OE.orderSettings['Amount'] = self.symbol_defaults[symbol_input]['Amount']
            self.OE.orderSettings['Price'] = self.symbol_defaults[symbol_input]['Price']
            self.OE.arrayOrderSettings['Granularity'] = self.symbol_defaults[symbol_input]['Granularity']
            self.OE.arrayOrderSettings['Spread'] = self.symbol_defaults[symbol_input]['Spread']
            self.OE.arrayOrderSettings['End Price'] = self.symbol_defaults[symbol_input]['End Price']
            self.updateSettingsLabels()
            self.updateArraySettingsLabels()
            if self.auto_preview:
                self.updateParameterLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Symbol set to ' + str(self.OE.orderSettings['Symbol']))
            self.label_last_action.config(text='[   Just changed Symbol   ]')
        else:
            print('ERROR! Invalid value input for Symbol.')
        

    def changeSymbol_BTC(self):
        self.changeSymbol('BTC/USD')

    def changeSymbol_ETH(self):
        self.changeSymbol('ETH/USD')

    def changeSymbol_LTC(self):
        self.changeSymbol('LTC/USD')

    def changeSymbol_DOGE(self):
        self.changeSymbol('DOGE/USD')
        
    def changeSymbol_LINK(self):
        self.changeSymbol('LINK/USD')
        
    def changeSymbol_ADA(self):
        self.changeSymbol('ADA/USD')
        
    def changeSymbol_UNI(self):
        self.changeSymbol('UNI/USD')
        
    def changeSymbol_ALGO(self):
        self.changeSymbol('ALGO/USD')
        
    def changeSymbol_COMP(self):
        self.changeSymbol('COMP/USD')
        
    def changeSymbol_BCH(self):
        self.changeSymbol('BCH/USD')
        
    def changeSymbol_YFI(self):
        self.changeSymbol('YFI/USD')
        
    def changeSymbol_XTZ(self):
        self.changeSymbol('XTZ/USD')
        
    def changeSymbol_XRP(self):
        self.changeSymbol('XRP/USD')

#   This version of changeSide is from when we used a menuButton to change the side. However, using a menu button is unnecessary, since there are only 2 choices.
##    def changeSide(self, side_input):
##        side_input = self.OE.checkSideInput(side_input)
##        if side_input:
##            self.OE.orderSettings['Side'] = str(side_input)
##            print('Side set to ' + str(self.OE.orderSettings['Side']))
##            if side_input == 'buy':
##                self.label_current_side.config(text=' Buy / Long ', bg=self.my_colors['Green'])
##                self.button_execute_orders.config(bg=self.my_colors['Dark Green'], activebackground=self.my_colors['Green'])
##            else:
##                self.label_current_side.config(text=' Sell / Short ', bg=self.current_exchange_colors['Red'])
##                self.button_execute_orders.config(bg=self.my_colors['Red'], activebackground=self.current_exchange_colors['Red'])
##        else:
##            print('ERROR! Invalid value input for Side.')
##        self.updateParameterLabels()

##    def changeSide_Buy(self):
##        self.changeSide('buy')
##
##    def changeSide_Sell(self):
##        self.changeSide('sell')

    def changeSide(self):
        if self.OE.orderSettings['Side'] == 'buy':
            self.OE.orderSettings['Side'] = 'sell'
            self.label_current_side.config(text=' Sell / Short ', bg=self.current_exchange_colors['Red'])
            self.button_execute_orders.config(bg=self.my_colors['Red'], activebackground=self.current_exchange_colors['Red'])
        else:
            self.OE.orderSettings['Side'] = 'buy'
            self.label_current_side.config(text=' Buy / Long ', bg=self.my_colors['Green'])
            self.button_execute_orders.config(bg=self.my_colors['Dark Green'], activebackground=self.my_colors['Green'])
        self.updateEndPrice()
        if self.auto_preview:
            self.updateParameterLabels()
            self.updateArraySettingsLabels()
        else:
            self.settings_have_changed_since_last_preview = True
            self.darkenArrayParameters()
        self.label_last_action.config(text='[   Just changed Side   ]')


    def changeAmount(self, *args):
        try:
            amount_input = self.OE.checkAmountInput(args[0])
        except:
            try:
                amount_input = self.OE.checkAmountInput(self.entry_change_amount.get())
            except:
                print('ERROR! Invalid value input for Amount.')
                amount_input = False
        if amount_input:
            self.OE.orderSettings['Amount'] = int(amount_input)
            self.label_current_amount.config(text=' ' + str(amount_input) + ' ')
            self.entry_change_amount.delete(0, 'end')
            if self.auto_preview:
                self.updateParameterLabels()
                self.updateArraySettingsLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Amount set to ' + str(self.OE.orderSettings['Amount']))
            self.label_last_action.config(text='[   Just changed Amount   ]')
        else:
            print('ERROR! Invalid value input for Amount.')
        

    def changePrice(self, *args):
        try:
            price_input = self.OE.checkPriceInput(args[0])
        except:
            try:
                price_input = self.OE.checkPriceInput(self.entry_change_price.get())
            except:
                print('ERROR! Invalid value input for Price.')
                price_input = False
        if price_input:
            self.OE.orderSettings['Price'] = float(price_input)
            self.entry_change_price.delete(0, 'end')
            self.label_current_price.config(text=' $' + str(price_input) + ' ')
            if self.lock_end_price:
                self.updateSpread()
            else:
                self.updateEndPrice()
            if self.auto_preview:
                self.updateParameterLabels()
                self.updateArraySettingsLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Price set to ' + str(self.OE.orderSettings['Price']))
            self.label_last_action.config(text='[   Just changed Price   ]')
        else:
            print('ERROR! Invalid value input for Price.')        
        

    def changePriceToMarket(self):
        try:
            if self.OE.orderSettings['Side'] == 'buy':
                market_price = self.OE.CTE.exchange.fetchTicker(self.OE.orderSettings['Symbol'])['bid']
            else:
                market_price = self.OE.CTE.exchange.fetchTicker(self.OE.orderSettings['Symbol'])['ask']
            self.OE.orderSettings['Price'] = float(market_price)
            self.label_current_price.config(text=' $' + str(market_price) + ' ')
            self.entry_change_price.delete(0, 'end')
            if self.lock_end_price:
                self.updateSpread()
            else:
                self.updateEndPrice()
            if self.auto_preview:
                self.updateParameterLabels()
                self.updateArraySettingsLabels()
            else:
                self.settings_have_changed_since_last_preview = True
                self.darkenArrayParameters()
            print('Price set to Market Price: $' + str(self.OE.orderSettings['Price']))
            self.label_last_action.config(text='[   Just changed Price   ]')
        except:
           print("CONNECTION ERROR! Can't fetch ticker.")
        

    def previewOrders(self):
        self.OE.createArrayOrder('use_current_settings')
        self.label_max_price.config(text=' ' + str(self.OE.arrayOrderParameters['Highest Price Order Price']) + ' ')
        self.label_max_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Highest Price Order Amount']) + ' ')
        self.label_min_price.config(text=' ' + str(self.OE.arrayOrderParameters['Lowest Price Order Price']) + ' ')
        self.label_min_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Lowest Price Order Amount']) + ' ')
        # Removed due to redundancy
        #self.label_total_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Total Order Amount']) + ' ')
        self.label_entry_at_execution.config(text=' ' + str(round(float(self.OE.arrayOrderParameters['Entry at Full Execution']), 2)) + ' ')
        self.label_number_of_orders.config(text=' ' + str(self.OE.arrayOrderParameters['Number of Orders']) + ' ')
        self.updateArraySettingsLabels()
        self.settings_have_changed_since_last_preview = False
        self.lightenArrayParameters()
##        if self.OE.validateOrder(self.OE.arrayOrderParameters['All Orders']):
##            if self.OE.orderSettings['Side'] == 'buy':
##                self.button_execute_orders.config(bg=self.my_colors['Green'], state='active')
##            else:
##                self.button_execute_orders.config(bg=self.my_colors['Red'], state='active')


    def refreshDisplayedOrders(self):
    # First, we figure out which symbols have active orders
        active_orders_by_symbol = {}
        for array_order_position in self.active_order_positions:
            array_order_number = self.active_order_positions[array_order_position]
            if array_order_number != '':
                symbol = self.OE.arrayOrderLedger[array_order_number]['Order Settings']['Symbol']
                if not(symbol in active_orders_by_symbol):
                    open_orders = self.OE.CTE.fetchOpenOrders({'Symbol': symbol})
                    active_orders_by_symbol[symbol] = open_orders
    # Secondly, the GUI's 10 order positions are iterated through and each order is checked and its amount is updated
        for array_order_position in self.active_order_positions:
            array_order_number = self.active_order_positions[array_order_position]
            if array_order_number != '':
                prefetched_open_orders = active_orders_by_symbol[self.OE.arrayOrderLedger[array_order_number]['Order Settings']['Symbol']]
                array_of_orders = self.OE.checkArrayOrder(int(array_order_number), {'Fetch Open Orders': True, \
                                                                                    'Prefetched Open Orders': prefetched_open_orders})
                if array_of_orders:
                    updated_amount = self.OE.arrayOrderLedger[array_order_number]['Total Amount']
                    self.active_order_labels[array_order_number]['Amount'].config(text=' Amount: ' + str(updated_amount) + ' ')
                else:
                    for key in self.active_order_labels[array_order_number]:
                        self.active_order_labels[array_order_number][key].grid_forget()
                    self.active_order_positions[array_order_position] = ''
        #self.button_refresh_displayed_orders.config(text=' Refresh #' + str(self.current_refresh_order_position) + ' ')

                                    
    def cancelArrayOrder(self, array_order_position):
        array_order_number = self.active_order_positions[array_order_position]
        self.OE.cancelArrayOrder(int(array_order_number))
        for key in self.active_order_labels[array_order_number]:
            self.active_order_labels[array_order_number][key].grid_forget()
        self.active_order_positions[array_order_position] = ''
        self.label_last_action.config(text='[   Just canceled Order #' + str(array_order_number) + '   ]')
    
    def cancelArrayOrder_1(self):
        self.cancelArrayOrder(1)

    def cancelArrayOrder_2(self):
        self.cancelArrayOrder(2)

    def cancelArrayOrder_3(self):
        self.cancelArrayOrder(3)

    def cancelArrayOrder_4(self):
        self.cancelArrayOrder(4)

    def cancelArrayOrder_5(self):
        self.cancelArrayOrder(5)

    def cancelArrayOrder_6(self):
        self.cancelArrayOrder(6)

    def cancelArrayOrder_7(self):
        self.cancelArrayOrder(7)

    def cancelArrayOrder_8(self):
        self.cancelArrayOrder(8)

    def cancelArrayOrder_9(self):
        self.cancelArrayOrder(9)

    def cancelArrayOrder_10(self):
        self.cancelArrayOrder(10)

    def cancelAllOrders(self):
        self.OE.CTE.exchange.cancel_all_orders()

    def rebuildArrayOrder(self, array_order_position):
        array_order_number = self.active_order_positions[array_order_position]
        if self.auto_quick_rebuild:
            self.OE.rebuildArrayOrder(int(array_order_number), {'Quick Rebuild': True})
        else:
            self.OE.rebuildArrayOrder(int(array_order_number))
        self.label_last_action.config(text='[   Just rebuilt Order #' + str(array_order_number) + '   ]')

    def rebuildArrayOrder_1(self):
        self.rebuildArrayOrder(1)

    def rebuildArrayOrder_2(self):
        self.rebuildArrayOrder(2)

    def rebuildArrayOrder_3(self):
        self.rebuildArrayOrder(3)

    def rebuildArrayOrder_4(self):
        self.rebuildArrayOrder(4)

    def rebuildArrayOrder_5(self):
        self.rebuildArrayOrder(5)

    def rebuildArrayOrder_6(self):
        self.rebuildArrayOrder(6)

    def rebuildArrayOrder_7(self):
        self.rebuildArrayOrder(7)

    def rebuildArrayOrder_8(self):
        self.rebuildArrayOrder(8)

    def rebuildArrayOrder_9(self):
        self.rebuildArrayOrder(9)

    def rebuildArrayOrder_10(self):
        self.rebuildArrayOrder(10)
    
        
    def createArrayOrder(self):
        if not(self.auto_preview):
            self.updateParameterLabels()
            self.updateArraySettingsLabels()
        self.OE.executeArrayOrders(self.OE.arrayOrderParameters['Individual Order Settings'])
        self.OE.graphArrayOrders(self.OE.arrayOrderParameters['Individual Order Settings'])
        #self.label_current_symbol_market_price.config(text='$' + str(self.OE.CTE.exchange.fetchTicker(self.OE.orderSettings['Symbol'])['bid']))
        array_order_number = len(self.OE.arrayOrderLedger)
        array_order_position = False
        for position in self.active_order_positions:
            if not(array_order_position):
                if self.active_order_positions[position] == '':
                    array_order_position = position
    # This refreshes the displayed order if there was no room before
    # Currently inactive because it's slow
        if not(array_order_position):
            self.refreshDisplayedOrders()
            for position in self.active_order_positions:
                if not(array_order_position):
                    if self.active_order_positions[position] == '':
                        array_order_position = position
    # This triggers if all 8 slots of active orders
        if not(array_order_position):
            print('ERROR! No positions available to display order for ' + str(self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Total Order Amount']) + ' !')
    # This is when there finally is a spot
        else:
            if 'Quick' in self.OE.arrayOrderLedger[array_order_number]['Order Settings']['Account']:
                if 'Long' in self.OE.arrayOrderLedger[array_order_number]['Order Settings']['Account']:
                    account_title = 'L50xQ'
                else:
                    account_title = 'S50xQ'
            else:
                account_title = self.OE.arrayOrderLedger[array_order_number]['Order Settings']['Account']
            self.label_order_title = tkinter.Label(self.GUI, font=self.label_font, text='Order #' + str(array_order_number) + \
                                                   ' (' + account_title + ')', \
                                                   borderwidth=1, relief='solid')
            self.label_order_amount = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Gray'], \
                                                    text=' Amount: ' + str(self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Total Order Amount']) + ' ', \
                                                    borderwidth=1, relief='solid')
        # Arranges the start & end based on if the order is long or short
            if self.OE.orderSettings['Side'] == 'buy':
                start_price = self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Highest Price Order Price']
                end_price = self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Lowest Price Order Price']
                self.label_order_title.config(bg=self.my_colors['Green'])
            else:
                start_price = self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Lowest Price Order Price']
                end_price = self.OE.arrayOrderLedger[array_order_number]['Array Order Parameters']['Highest Price Order Price']
                self.label_order_title.config(bg=self.my_colors['Light Red'])
            self.label_start_price = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Gray'], \
                                                    borderwidth=1, relief='solid', text=' Start: $' + str(start_price) + ' ')
            self.label_end_price = tkinter.Label(self.GUI, font=self.current_value_font, bg=self.current_exchange_colors['Gray'], \
                                                    borderwidth=1, relief='solid', text=' End: $' + str(end_price) + ' ')
        # Creates the cancel order button & assigns the appropriate cancelArrayOrder function
            self.button_cancel_order = tkinter.Button(self.GUI, font=self.font_dict[10], bg=self.current_exchange_colors['Red'], fg=self.current_exchange_colors['White'], \
                                                       activebackground=self.current_exchange_colors['Red'], activeforeground=self.current_exchange_colors['White'], \
                                                       text='Cancel', command=self.individual_order_functions['Cancel'][array_order_position])
        # Creates the rebuild order button & assigns the appropriate rebuildArrayOrder function
            self.button_rebuild_order = tkinter.Button(self.GUI, font=self.font_dict[10], bg=self.current_exchange_colors['Green'], fg=self.current_exchange_colors['White'], \
                                                       activebackground=self.current_exchange_colors['Green'], activeforeground=self.current_exchange_colors['White'], \
                                                       text='Rebuild', command=self.individual_order_functions['Rebuild'][array_order_position])
        # Adds individual order widgets to the grid
            array_row_number = 50 + (10 * int((array_order_position - 1) / 5))
            array_order_columnspan = 1
            if array_order_position % 5 == 0:
                array_order_columnspan = 2
            array_column_number = array_order_position % 5
            if array_column_number == 0:
                array_column_number = 5
            if (array_order_position - 3) % 5 == 0:
                array_order_columnspan = 6
                array_column_number = 1
            self.active_order_positions[array_order_position] = array_order_number
            
            self.label_order_title.grid(columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 3)
            self.label_order_amount.grid(columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 4)
            self.label_start_price.grid(columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 5)
            self.label_end_price.grid(columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 6)
            self.button_cancel_order.grid(padx=(0, 53), columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 7)
            self.button_rebuild_order.grid(padx=(53,0), columnspan=array_order_columnspan, column=array_column_number, row=array_row_number + 7)

            new_array_order_labels = {'Title': self.label_order_title, \
                                      'Amount': self.label_order_amount, \
                                      'Start Price': self.label_start_price, \
                                      'End Price': self.label_end_price, \
                                      'Cancel Button': self.button_cancel_order, \
                                      'Rebuild Button': self.button_rebuild_order}
            self.active_order_labels[array_order_number] = new_array_order_labels

        self.updateParameterLabels()
        self.label_last_action.config(text='[   Just created Order #' + str(array_order_number) + '   ]')
        

    def updateParameterLabels(self):
        self.OE.createArrayOrder('update_current_parameters')
        self.label_max_price.config(text=' ' + str(self.OE.arrayOrderParameters['Highest Price Order Price']) + ' ')
        self.label_max_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Highest Price Order Amount']) + ' ')
        self.label_min_price.config(text=' ' + str(self.OE.arrayOrderParameters['Lowest Price Order Price']) + ' ')
        self.label_min_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Lowest Price Order Amount']) + ' ')
        # Removed due to redundancy
        #self.label_total_amount.config(text=' ' + str(self.OE.arrayOrderParameters['Total Order Amount']) + ' ')
        self.label_entry_at_execution.config(text=' ' + str(round(float(self.OE.arrayOrderParameters['Entry at Full Execution']), 2)) + ' ')
        self.label_number_of_orders.config(text=' ' + str(self.OE.arrayOrderParameters['Number of Orders']) + ' ')
      # This is a price "ticker" that displays the current price of the currency you're trading
      # I commented it out because it slows the program down too much. But, I've been thinking about adding it as an option
        #self.label_current_symbol_price.config(text='$' + str(self.OE.CTE.exchange.fetchTicker(self.OE.orderSettings['Symbol'])['bid']))
        self.settings_have_changed_since_last_preview = False
        self.lightenArrayParameters()

    def updateSettingsLabels(self):
        self.label_current_account.config(text=' ' + str(self.OE.orderSettings['Account']) + ' ')
        self.label_current_symbol.config(text=' ' + str(self.OE.orderSettings['Symbol']) + ' ')
        if self.OE.orderSettings['Side'] == 'sell':
            self.label_current_side.config(text=' Sell / Short ', bg=self.current_exchange_colors['Red'])
            self.button_execute_orders.config(bg=self.my_colors['Red'], activebackground=self.current_exchange_colors['Red'])
        else:
            self.label_current_side.config(text=' Buy / Long ', bg=self.my_colors['Green'])
            self.button_execute_orders.config(bg=self.my_colors['Dark Green'], activebackground=self.my_colors['Green'])
        self.label_current_amount.config(text=' ' + str(self.OE.orderSettings['Amount']) + ' ')
        self.label_current_price.config(text=' ' + str(self.OE.orderSettings['Price']) + ' ')

    def updateArraySettingsLabels(self):
        self.label_current_granularity.config(text=' ' + str(self.OE.arrayOrderSettings['Granularity']) + ' ')
        self.label_current_spread.config(text=' ' + str(self.OE.arrayOrderSettings['Spread']) + ' ')
        self.label_current_end_price.config(text=' ' + str(self.OE.arrayOrderSettings['End Price']) + ' ')
        self.label_current_steepness.config(text=' ' + str(self.OE.arrayOrderSettings['Steepness']) + ' ')
        self.label_current_slope.config(text=' ' + str(self.OE.arrayOrderSettings['Slope']) + ' ')
        if self.row_17_button == 'Minimum Order Size':
            self.label_current_minimum_order_size.config(text=' ' + str(self.OE.arrayOrderSettings['Minimum Order Size']) + ' ')
        elif self.row_17_button == 'Truncation Amount':
            self.label_current_truncation_amount.config(text=' ' + str(self.OE.arrayOrderSettings['Truncation Amount']) + ' ')
        elif self.row_17_button == 'Quick Granularity':
            self.label_current_quick_granularity_intensity.config(text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity Intensity']) + ' ')
            if self.OE.arrayOrderSettings['Quick Granularity Start %'] != 'default':
                self.label_current_quick_granularity_start.config(text=' ' + str(100 * self.OE.arrayOrderSettings['Quick Granularity Start %']) + '% ')
            else:
                self.label_current_quick_granularity_start.config(text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity Start %']) + ' ')
            if self.OE.arrayOrderSettings['Quick Granularity Start %'] != 'default':
                self.label_current_quick_granularity_end.config(text=' ' + str(100 * self.OE.arrayOrderSettings['Quick Granularity End %']) + '% ')
            else:
                self.label_current_quick_granularity_end.config(text=' ' + str(self.OE.arrayOrderSettings['Quick Granularity End %']) + ' ')

    def updateEndPrice(self):
        if self.OE.orderSettings['Side'] == 'buy':
            new_end_price = float(self.OE.orderSettings['Price']) - float(self.OE.arrayOrderSettings['Spread'])
        else:
            new_end_price = float(self.OE.orderSettings['Price']) + float(self.OE.arrayOrderSettings['Spread'])
        self.OE.arrayOrderSettings['End Price'] = new_end_price
        self.label_current_end_price.config(text= ' $' + str(new_end_price))

    def updateSpread(self):
        if self.OE.orderSettings['Side'] == 'buy':
            new_spread = float(self.OE.orderSettings['Price']) - float(self.OE.arrayOrderSettings['End Price'])
        else:
            new_spread = float(self.OE.arrayOrderSettings['End Price']) - float(self.OE.orderSettings['Price'])
        self.OE.arrayOrderSettings['Spread'] = new_spread
        self.label_current_spread.config(text=str(new_spread))

    def changeAccount(self, account_input):
        account_input = self.OE.checkAccountInput('Default', account_input)
        if account_input:
            try:
                connection_data = self.OE.CTE.connect('Default', account_input)
                self.OE.orderSettings['Account'] = str(account_input)
                self.OE.orderSettings['Exchange'] = self.OE.CTE.exchange_name
                print('OE : Account set to ' + str(self.OE.orderSettings['Account']))
                self.label_current_account.config(bg=self.account_colors[self.OE.orderSettings['Account']], text=' ' + str(account_input) + ' ')
                self.label_last_action.config(text='[   Just changed Account   ]')
            except:
                print('OE GUI : ERROR changing accounts!')
        else:
            print('ERROR! Invalid value input for Account.')  
        self.updateParameterLabels()

    def changeAccount_Main(self):
        self.changeAccount('Main')

    def changeAccount_Short50x(self):
        self.changeAccount('Short 50x')

    def changeAccount_Long50x(self):
        self.changeAccount('Long 50x')

    def changeAccount_Short50xQuick(self):
        self.changeAccount('Short 50x Quick')

    def changeAccount_Long50xQuick(self):
        self.changeAccount('Long 50x Quick')

    def changeAccount_Monty(self):
        self.changeAccount('Monty')

    def nudgeSetting(self, setting_to_nudge, amount_to_nudge):
        try:
            new_value = self.OE.orderSettings[setting_to_nudge] + amount_to_nudge
        except:
            new_value = self.OE.arrayOrderSettings[setting_to_nudge] + amount_to_nudge
        if setting_to_nudge == 'Amount':
            self.changeAmount(new_value)
        elif setting_to_nudge == 'Price':
            self.changePrice(new_value)
        elif setting_to_nudge == 'Granularity':
            self.changeGranularity(new_value)
        elif setting_to_nudge == 'Spread':
            self.changeSpread(new_value)
        elif setting_to_nudge == 'End Price':
            self.changeEndPrice(new_value)
        elif setting_to_nudge == 'Steepness':
            self.changeSteepness(new_value)
        elif setting_to_nudge == 'Multiplicative Factor':
            self.changeMultiplicativeFactor(new_value)
        elif setting_to_nudge == 'Slope':
            self.changeSlope(new_value)

    def nudgeAmount_Plus1(self):
        self.nudgeSetting('Amount', 1)
        
    def nudgeAmount_Plus5(self):
        self.nudgeSetting('Amount', 5)

    def nudgeAmount_Plus25(self):
        self.nudgeSetting('Amount', 25)

    def nudgeAmount_Plus100(self):
        self.nudgeSetting('Amount', 100)

    def nudgeAmount_Plus300(self):
        self.nudgeSetting('Amount', 300)
        
    def nudgeAmount_Plus500(self):
        self.nudgeSetting('Amount', 500)

    def nudgeAmount_Plus1000(self):
        self.nudgeSetting('Amount', 1000)

    def nudgeAmount_Plus5000(self):
        self.nudgeSetting('Amount', 5000)

    def nudgeAmount_Minus1(self):
        self.nudgeSetting('Amount', -1)
        
    def nudgeAmount_Minus5(self):
        self.nudgeSetting('Amount', -5)

    def nudgeAmount_Minus25(self):
        self.nudgeSetting('Amount', -25)

    def nudgeAmount_Minus100(self):
        self.nudgeSetting('Amount', -100)

    def nudgeAmount_Minus300(self):
        self.nudgeSetting('Amount', -300)

    def nudgeAmount_Minus500(self):
        self.nudgeSetting('Amount', -500)

    def nudgeAmount_Minus1000(self):
        self.nudgeSetting('Amount', -1000)

    def nudgeAmount_Minus5000(self):
        self.nudgeSetting('Amount', -5000)

    def nudgePrice_Plus1(self):
        self.nudgeSetting('Price', 1)
        
    def nudgePrice_Plus5(self):
        self.nudgeSetting('Price', 5)

    def nudgePrice_Plus10(self):
        self.nudgeSetting('Price', 10)

    def nudgePrice_Plus25(self):
        self.nudgeSetting('Price', 25)

    def nudgePrice_Plus50(self):
        self.nudgeSetting('Price', 50)

    def nudgePrice_Plus100(self):
        self.nudgeSetting('Price', 100)

    def nudgePrice_Plus1000(self):
        self.nudgeSetting('Price', 1000)

    def nudgePrice_Minus1(self):
        self.nudgeSetting('Price', -1)
        
    def nudgePrice_Minus5(self):
        self.nudgeSetting('Price', -5)

    def nudgePrice_Minus10(self):
        self.nudgeSetting('Price', -10)

    def nudgePrice_Minus25(self):
        self.nudgeSetting('Price', -25)

    def nudgePrice_Minus50(self):
        self.nudgeSetting('Price', -50)

    def nudgePrice_Minus100(self):
        self.nudgeSetting('Price', -100)

    def nudgePrice_Minus1000(self):
        self.nudgeSetting('Price', -1000)

    def nudgeEndPrice_Plus1(self):
        self.nudgeSetting('End Price', 1)
        
    def nudgeEndPrice_Plus5(self):
        self.nudgeSetting('End Price', 5)

    def nudgeEndPrice_Plus10(self):
        self.nudgeSetting('End Price', 10)

    def nudgeEndPrice_Plus25(self):
        self.nudgeSetting('End Price', 25)

    def nudgeEndPrice_Plus50(self):
        self.nudgeSetting('End Price', 50)

    def nudgeEndPrice_Plus100(self):
        self.nudgeSetting('End Price', 100)

    def nudgeEndPrice_Plus1000(self):
        self.nudgeSetting('End Price', 1000)

    def nudgeEndPrice_Minus1(self):
        self.nudgeSetting('End Price', -1)
        
    def nudgeEndPrice_Minus5(self):
        self.nudgeSetting('End Price', -5)

    def nudgeEndPrice_Minus10(self):
        self.nudgeSetting('End Price', -10)

    def nudgeEndPrice_Minus25(self):
        self.nudgeSetting('End Price', -25)

    def nudgeEndPrice_Minus50(self):
        self.nudgeSetting('End Price', -50)

    def nudgeEndPrice_Minus100(self):
        self.nudgeSetting('End Price', -100)

    def nudgeEndPrice_Minus1000(self):
        self.nudgeSetting('End Price', -1000)
        
    def nudgeSpread_Plus5(self):
        self.nudgeSetting('Spread', 5)

    def nudgeSpread_Plus10(self):
        self.nudgeSetting('Spread', 10)

    def nudgeSpread_Plus50(self):
        self.nudgeSetting('Spread', 50)

    def nudgeSpread_Plus100(self):
        self.nudgeSetting('Spread', 100)

    def nudgeSpread_Plus500(self):
        self.nudgeSetting('Spread', 500)

    def nudgeSpread_Minus5(self):
        self.nudgeSetting('Spread', -5)

    def nudgeSpread_Minus10(self):
        self.nudgeSetting('Spread', -10)

    def nudgeSpread_Minus50(self):
        self.nudgeSetting('Spread', -50)

    def nudgeSpread_Minus100(self):
        self.nudgeSetting('Spread', -100)

    def nudgeSpread_Minus500(self):
        self.nudgeSetting('Spread', -500)

    def nudgeGranularity_PlusPoint5(self):
        self.nudgeSetting('Granularity', .5)
        
    def nudgeGranularity_Plus1(self):
        self.nudgeSetting('Granularity', 1)

    def nudgeGranularity_Plus3(self):
        self.nudgeSetting('Granularity', 3)

    def nudgeGranularity_Plus5(self):
        self.nudgeSetting('Granularity', 5)

    def nudgeGranularity_Plus10(self):
        self.nudgeSetting('Granularity', 10)

    def nudgeGranularity_Plus50(self):
        self.nudgeSetting('Granularity', 50)

    def nudgeGranularity_MinusPoint5(self):
        self.nudgeSetting('Granularity', -.5)
        
    def nudgeGranularity_Minus1(self):
        self.nudgeSetting('Granularity', -1)

    def nudgeGranularity_Minus3(self):
        self.nudgeSetting('Granularity', -3)

    def nudgeGranularity_Minus5(self):
        self.nudgeSetting('Granularity', -5)

    def nudgeGranularity_Minus10(self):
        self.nudgeSetting('Granularity', -10)

    def nudgeGranularity_Minus50(self):
        self.nudgeSetting('Granularity', -50)

    def nudgeSteepness_PlusPoint1(self):
        self.nudgeSetting('Steepness', .1)
        
    def nudgeSteepness_Plus1(self):
        self.nudgeSetting('Steepness', 1)

    def nudgeSteepness_MinusPoint1(self):
        self.nudgeSetting('Steepness', -.1)
        
    def nudgeSteepness_Minus1(self):
        self.nudgeSetting('Steepness', -1)

    def nudgeSlope_PlusPoint1(self):
        self.nudgeSetting('Slope', .1)
        
    def nudgeSlope_Plus1(self):
        self.nudgeSetting('Slope', 1)

    def nudgeSlope_Double(self):
        self.nudgeSetting('Slope', (self.OE.arrayOrderSettings['Slope'] * 2) - self.OE.arrayOrderSettings['Slope'])

    def nudgeSlope_MinusPoint1(self):
        self.nudgeSetting('Slope', -.1)
        
    def nudgeSlope_Minus1(self):
        self.nudgeSetting('Slope', -1)

    def nudgeSlope_Half(self):
        self.nudgeSetting('Slope', (self.OE.arrayOrderSettings['Slope'] / 2) - self.OE.arrayOrderSettings['Slope'])

    def nudgeMultiplicativeFactor_PlusPoint01(self):
        self.nudgeSetting('Multiplicative Factor', .01)

    def nudgeMultiplicativeFactor_PlusPoint1(self):
        self.nudgeSetting('Multiplicative Factor', .1)
        
    def nudgeMultiplicativeFactor_Plus1(self):
        self.nudgeSetting('Multiplicative Factor', 1)

    def nudgeMultiplicativeFactor_MinusPoint01(self):
        self.nudgeSetting('Multiplicative Factor', -.01)

    def nudgeMultiplicativeFactor_MinusPoint1(self):
        self.nudgeSetting('Multiplicative Factor', -.1)
        
    def nudgeMultiplicativeFactor_Minus1(self):
        self.nudgeSetting('Multiplicative Factor', -1)

    def saveProfile(self, profile_to_update):
        self.profile_display[profile_to_update] = {}
        self.profile_display[profile_to_update]['Order Settings'] = copy.deepcopy(self.OE.orderSettings)
        self.profile_display[profile_to_update]['Array Order Settings'] = copy.deepcopy(self.OE.arrayOrderSettings)
        profile_dict = {}
        profile_dict['Order Settings'] = self.profile_display[profile_to_update]['Order Settings']
        profile_dict['Array Order Settings'] = self.profile_display[profile_to_update]['Array Order Settings']
        print('Profile ' + profile_to_update + ' saved!')
        self.label_last_action.config(text='[   Just saved Profile ' + profile_to_update + '   ]')
        pickle.dump(profile_dict, open(str(pathlib.Path().absolute()) + '\\_Array_Order_Profiles\\Profile_' + profile_to_update + '.pickle', 'wb'))

    def saveProfile_I(self):
        self.saveProfile('I')
        self.label_profile_I_info = tkinter.Label(self.GUI, font=self.font_dict[8], bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                      text=' ' + str(self.OE.orderSettings['Amount']) + ' ' + self.OE.arrayOrderSettings['Style'] + '\n ' + \
                                                      str(float(self.OE.orderSettings['Price'])) + ' - ' + str(float(self.OE.arrayOrderSettings['End Price'])))
        if self.OE.orderSettings['Side'] == 'buy':
            self.label_profile_I_info.config(bg=self.green_colors[20])
        else:
            self.label_profile_I_info.config(bg=self.red_colors[15])
        self.label_profile_I_info.grid(padx=(0,128), rowspan=1, columnspan=2, column=1, row=self.layoutDict['Profiles'])

    def saveProfile_II(self):
        self.saveProfile('II')
        self.label_profile_II_info = tkinter.Label(self.GUI, font=self.font_dict[8], bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                      text=' ' + str(self.OE.orderSettings['Amount']) + ' ' + self.OE.arrayOrderSettings['Style'] + '\n ' + \
                                                      str(float(self.OE.orderSettings['Price'])) + ' - ' + str(float(self.OE.arrayOrderSettings['End Price'])))
        if self.OE.orderSettings['Side'] == 'buy':
            self.label_profile_II_info.config(bg=self.green_colors[20])
        else:
            self.label_profile_II_info.config(bg=self.red_colors[15])
        self.label_profile_II_info.grid(padx=(0,97), rowspan=1, columnspan=2, column=2, row=self.layoutDict['Profiles'])

    def saveProfile_III(self):
        self.saveProfile('III')
        self.label_profile_III_info = tkinter.Label(self.GUI, font=self.font_dict[8], bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                      text=' ' + str(self.OE.orderSettings['Amount']) + ' ' + self.OE.arrayOrderSettings['Style'] + '\n ' + \
                                                      str(float(self.OE.orderSettings['Price'])) + ' - ' + str(float(self.OE.arrayOrderSettings['End Price'])))
        if self.OE.orderSettings['Side'] == 'buy':
            self.label_profile_III_info.config(bg=self.green_colors[20])
        else:
            self.label_profile_III_info.config(bg=self.red_colors[15])
        self.label_profile_III_info.grid(padx=(9,0), rowspan=1, columnspan=1, column=3, row=self.layoutDict['Profiles'])

    def saveProfile_IV(self):
        self.saveProfile('IV')
        self.label_profile_IV_info = tkinter.Label(self.GUI, font=self.font_dict[8], bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                      text=' ' + str(self.OE.orderSettings['Amount']) + ' ' + self.OE.arrayOrderSettings['Style'] + '\n ' + \
                                                      str(float(self.OE.orderSettings['Price'])) + ' - ' + str(float(self.OE.arrayOrderSettings['End Price'])))
        if self.OE.orderSettings['Side'] == 'buy':
            self.label_profile_IV_info.config(bg=self.green_colors[20])
        else:
            self.label_profile_IV_info.config(bg=self.red_colors[15])
        self.label_profile_IV_info.grid(padx=(0,60), rowspan=1, columnspan=2, column=4, row=self.layoutDict['Profiles'])

    def saveProfile_V(self):
        self.saveProfile('V')
        self.label_profile_V_info = tkinter.Label(self.GUI, font=self.font_dict[8], bg=self.current_exchange_colors['White'], borderwidth=1, relief='solid', \
                                                      text=' ' + str(self.OE.orderSettings['Amount']) + ' ' + self.OE.arrayOrderSettings['Style'] + '\n ' + \
                                                      str(float(self.OE.orderSettings['Price'])) + ' - ' + str(float(self.OE.arrayOrderSettings['End Price'])))
        if self.OE.orderSettings['Side'] == 'buy':
            self.label_profile_V_info.config(bg=self.green_colors[20])
        else:
            self.label_profile_V_info.config(bg=self.red_colors[15])
        self.label_profile_V_info.grid(padx=(42,0), rowspan=1, columnspan=2, column=5, row=self.layoutDict['Profiles'])

    def loadProfile(self, profile_to_load):
        try:
            self.changeAccount(profile_dict['Order Settings']['Account'])
            self.OE.orderSettings = copy.deepcopy(self.profile_display[profile_to_load]['Order Settings'])
            self.OE.arrayOrderSettings = copy.deepcopy(self.profile_display[profile_to_load]['Array Order Settings'])
            self.changeSymbol(profile_dict['Order Settings']['Symbol'])
            self.changeStyle(profile_dict['Array Order Settings']['Style'])
            self.updateParameterLabels()
            self.updateSettingsLabels()
            self.updateArraySettingsLabels()
            print('Profile ' + profile_to_load + ' loaded!')
            self.label_last_action.config(text='[   Just loaded Profile ' + profile_to_load + '   ]')
            if profile_to_load == 'I':
                self.saveProfile_I()
            elif profile_to_load == 'II':
                self.saveProfile_II()
            elif profile_to_load == 'III':
                self.saveProfile_III()
            elif profile_to_load == 'IV':
                self.saveProfile_IV()
            elif profile_to_load == 'V':
                self.saveProfile_V()
        except:
            try:
                profile_dict = pickle.load(open(str(pathlib.Path().absolute()) + '\\_Array_Order_Profiles\\Profile_' + profile_to_load + '.pickle', 'rb'))
                self.changeAccount(profile_dict['Order Settings']['Account'])
                self.OE.orderSettings = copy.deepcopy(profile_dict['Order Settings'])
                self.OE.arrayOrderSettings = copy.deepcopy(profile_dict['Array Order Settings'])
                self.changeSymbol(profile_dict['Order Settings']['Symbol'])
                self.changeStyle(profile_dict['Array Order Settings']['Style'])
                self.updateParameterLabels()
                self.updateSettingsLabels()
                self.updateArraySettingsLabels()
                print('Profile ' + profile_to_load + ' loaded from pickle file!')
                self.label_last_action.config(text='[   Just loaded Profile ' + profile_to_load + '   ]')
                if profile_to_load == 'I':
                    self.saveProfile_I()
                elif profile_to_load == 'II':
                    self.saveProfile_II()
                elif profile_to_load == 'III':
                    self.saveProfile_III()
                elif profile_to_load == 'IV':
                    self.saveProfile_IV()
                elif profile_to_load == 'V':
                    self.saveProfile_V()
            except:
                print('ERROR! No information or file to load from Profile ' + profile_to_load)
        
    def loadProfile_I(self):
        self.loadProfile('I')

    def loadProfile_II(self):
        self.loadProfile('II')

    def loadProfile_III(self):
        self.loadProfile('III')

    def loadProfile_IV(self):
        self.loadProfile('IV')

    def loadProfile_V(self):
        self.loadProfile('V')

    def toggleAutoPreview(self):
        if self.auto_preview:
            self.auto_preview = False
            self.button_auto_preview.config(relief='raised', bg=self.current_exchange_colors['Gray'])
        else:
            self.auto_preview = True
            self.button_auto_preview.config(relief='sunken', bg=self.my_colors['Light Teal'])
            self.previewOrders()
        print('Auto-prievew set to ' + str(self.auto_preview) + '.')

    def toggleLockEndPrice(self):
        if self.lock_end_price:
            self.lock_end_price = False
            self.button_lock_end_price.config(relief='raised', bg=self.current_exchange_colors['Gray'])
        else:
            self.lock_end_price = True
            self.button_lock_end_price.config(relief='sunken', bg=self.my_colors['Light Teal'])
        print('Lock End Price set to ' + str(self.lock_end_price) + '.')

    def darkenArrayParameters(self):
        self.label_min_amount.config(bg=self.my_colors['Dark Gray'])
        self.label_max_amount.config(bg=self.my_colors['Dark Gray'])
        # Removed due to redundancy
        #self.label_total_amount.config(bg=self.my_colors['Dark Gray'])
        self.label_number_of_orders.config(bg=self.my_colors['Dark Gray'])
        self.label_min_price.config(bg=self.my_colors['Dark Gray'])
        self.label_max_price.config(bg=self.my_colors['Dark Gray'])
        self.label_entry_at_execution.config(bg=self.my_colors['Dark Gray'])

    def lightenArrayParameters(self):
        self.label_min_amount.config(bg=self.current_exchange_colors['Light Blue'])
        self.label_max_amount.config(bg=self.current_exchange_colors['Light Blue'])
        # Removed due to redundancy
        #self.label_total_amount.config(bg=self.current_exchange_colors['Light Blue'])
        self.label_number_of_orders.config(bg=self.current_exchange_colors['Light Blue'])
        self.label_min_price.config(bg=self.current_exchange_colors['Light Blue'])
        self.label_max_price.config(bg=self.current_exchange_colors['Light Blue'])
        self.label_entry_at_execution.config(bg=self.current_exchange_colors['Light Blue'])

# This will create the OperateExchangeGUI class in a non-local scope, making it more secure
if __name__ == "__main__":
    main()
