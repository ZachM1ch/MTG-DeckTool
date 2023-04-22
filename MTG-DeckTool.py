##---------------------##
## Zachary Michniewicz ##
##    DeckTool V1.0    ##
##    21 April 2023    ##
##---------------------##

# imports
import requests
import json
import PIL.Image
import PIL.ImageTk
from io import BytesIO
from tkinter import *
import webbrowser

# create root window
root = Tk()
 
# setup window
root.title("Magic: The Gathering DeckTool")
root.geometry('1430x980')
root['bg'] = '#19232D'

# global variable for result of api call
call_result = {}

# lists for results of search
labels = []
images = []
entries = []
buttons = []

# variable for result of add
add_var = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]

# list of dicts for decklist
decklist = []

# preparing variable for decklist viewing
title_label = Text(root, height= 1, borderwidth=0)

# function to open TCGPlayer mass entry page
def tcg():
    webbrowser.open('https://www.tcgplayer.com/massentry?productline=Magic')
    
# function to check if card is legal in selected format
def formatted():
    # get radio button value
    rad = radio.get()
    return rad
    

# function to add cards to decklist
def added(index):

    #check if card is legal in selected format    
    if str(formatted()) == 'kitchen' or call_result['data'][index]['legalities'][str(formatted())] == 'legal' or call_result['data'][index]['legalities'][str(formatted())] == 'restricted':
        error_label.configure(text = "")
    
        # increase decklist qty if card is on already
        same = False
        for i in decklist:
            if i['name'] == call_result['data'][index]['name']:
                i['qty'] += int(add_var[index].get())
                same = True
                if i['qty'] < 1:
                    decklist.remove(i)
                    break;
        if same == False:
            decklist.append({'qty': int(add_var[index].get()), 'name': call_result['data'][index]['name'], 'set': call_result['data'][index]['set'], 'price': call_result['data'][index]['prices']['usd']})
    
            # format set code
            cap_set = '['
            for i in decklist[-1]['set']:
                if i.isalpha() == True:
                    cap_set += i.capitalize()
                else:
                    cap_set += i
            cap_set += ']'
            decklist[-1]['set'] = cap_set
    
        entries[index].delete(0, END)
    
        same == False
        print(decklist)  
    else:
         error_label.configure(text = "The card chosen is not legal in the selected format", fg = 'red')

# function to view decklist
def viewed():
    
    # reset lists
    resetLists(labels, images, entries, buttons)
    
    data = "Decklist\n-----------------------------------------"
    
    for i in range(len(decklist)):
        info = "\n" + str(decklist[i]['qty']) + " " + decklist[i]['name'] + " " + decklist[i]['set']
        data += info
    
    title_label.configure(height = len(decklist)+2, bg = '#505F69', fg = 'white')
    title_label.insert(1.0, data)
    title_label.grid(column = 1, row = 1, padx = 15)
    
    # estimated price output
    cost = 0.0
    for i in decklist:
        cost += (int(i['qty']) * (float(i['price'])*100))
    cost = cost / 100
        
    est = "Estimated Price: $%.2f" % cost
    
    price_label = Label(root, text = est, justify = "left", anchor = "w", bg = '#19232D', fg = 'white')
    price_label.grid(column=1, row=2)
    
    
# function to save decklist
def saved():
    # reset everything
    resetLists(labels, images, entries, buttons)
    title_label.delete("1.0", "end")
    title_label.grid_remove()
    
    #retrieve decklist name
    dln = txt_list.get()
    if dln == "":
        dln = "Decklist"
    
    # get data from viewable list
    f = open(dln + ".txt", "w")
    for i in decklist:
        f.write(str(i['qty']) + " " + i['name'] + " " + i['set'] + "\n")
    f.close()
    

# function to format search term for api call
def searchFormat(term):
    res = ""
    for i in term:
        if i == '\"':
            res = res + "%22"
        elif i == ',':
            res = res + "%2C"
        elif i == ' ':
            res = res + "+"
        else:
            res = res + i
    return res

# reset lists
def resetLists(l1, l2, l3, l4):
    # reset lists
    for a in l1:
        a.grid_remove()
    for b in l2:
        b.grid_remove()
    for c in l3:
        c.grid_remove()
    for d in l4:
        d.grid_remove()
        
 
# function to search and display results of api call
def searched():
    
    global call_result
    
    # reset everything
    resetLists(labels, images, entries, buttons)
    title_label.delete("1.0", "end")
    title_label.grid_remove()
        
    # api call
    req = "https://api.scryfall.com/cards/search?q="
    tmp_res = txt.get()
    reqs = req + searchFormat(tmp_res) + "+-is%3Adoublesided+-st%3Amemorabilia+-st%3Atoken+-set%3Apmoa+usd>%3D0.01&order=usd&dir=asc"
    full_req = requests.get(reqs)
    full_list = json.loads(full_req.text)
    
    if full_list['object'] == 'error':
        error_label.configure(text = "The search term entered did not return any results", fg = 'red')
    else:
        error_label.configure(text = "")
        
        call_result = full_list
    
        # determine list of displayed results
        list_len = len(full_list['data'])
        if list_len < 16:
            range_run = list_len
        else:
            range_run = 16
            
        # create empty labels across window
        row_ct = 1
        for i in range(range_run):
            labels.append(Label(root, text = "", justify = "left", anchor = "nw", width = 25, wraplength = 150, bg = '#19232D', fg = 'white'))
            entries.append(Entry(root, justify = "right", textvariable = add_var[i], width = 10, bg = '#6C7073', fg = 'white'))
            buttons.append(Button(root, text = "Add to deck", command=lambda index=i: added(index), bg = '#32414B', fg = 'white'))
            col = ((int((i)/4)+1)*3)-2
            images.append(Label(root))
            images[i].grid(column =col, row =row_ct, rowspan=5)
            labels[i].grid(column =col+1, row =row_ct, columnspan=2, rowspan=5)
            row_ct += 5
            entries[i].grid(column =col+1, row = row_ct, sticky="e", padx=7)
            buttons[i].grid(column =col+2, row = row_ct, sticky="w")
            row_ct += 1
            
            if row_ct > 24:
                row_ct = 1
                
        # gather and format the results of the api call for card
        card_list = ""
        for i in range(range_run):   
            card_list = card_list + "------------------------------\n"
            card_list = card_list + "Name: " + full_list['data'][i]['name'] + "\n"
            card_list = card_list + "Set: " + full_list['data'][i]['set_name'] + "\n"
            #card_list = card_list + "CMC: " + str(int(full_list['data'][i]['cmc'])) + "\n"
            card_list = card_list + "Price: $" + str(full_list['data'][i]['prices']['usd']) + "\n"
            
            # get image of card
            img_url = full_list['data'][i]['image_uris']['small']
            img_resp = requests.get(img_url)
            img_actual = PIL.Image.open(BytesIO(img_resp.content))
            real_img = PIL.ImageTk.PhotoImage(img_actual)
            
            # configure card label to image
            images[i].configure(image = real_img)
            images[i].image = real_img
            
            # get and format more rresults from card (for format legality)
            legal = full_list['data'][i]['legalities'].items()
            for k, v in legal:
                if (k == 'standard' or k == 'modern' or k == 'legacy' or k == 'vintage' or k == 'commander'):
                    card_list = card_list + k.capitalize() + ": " + v.capitalize().replace("_", " ") + "\n"
                    
            card_list = card_list + "------------------------------"
                    
            # configure text label to formatted results
            labels[i].configure(text = card_list)
                    
            # reset formatted text var for next card
            card_list = ""
                    
                    
# left column of buttons
leftside = Label(root, text = "", justify = "left", anchor = "nw", bg = '#19232D', fg = 'white')
leftside.grid(column=0, row=0)

# view deck button
view_deck = Button(root, text = "View Deck", command=viewed, bg = '#32414B', fg = 'white')
view_deck.grid(column=0, row=1)

# left column of buttons
listname = Label(root, text = "List Name:", justify = "left", anchor = "nw", bg = '#19232D', fg = 'white')
listname.grid(column=0, row=2)

# deck name field
txt_list = Entry(root, width=15, bg = '#6C7073', fg = 'white')
txt_list.grid(column =0, row =3) 

# save deck button
save_deck = Button(root, text = "Save Deck", command=saved, bg = '#32414B', fg = 'white')
save_deck.grid(column=0, row=4)

# tcgplayer button
tcg_entry = Button(root, text = "Entry Page", command=tcg, bg = '#32414B', fg = 'white')
tcg_entry.grid(column=0, row=5)

# radio label
radio_label = Label(root, text = "Legality:", justify = "left", anchor = "nw", bg = '#19232D', fg = 'white')
radio_label.grid(column=0, row=6)

# radio buttons
radio = StringVar(root, "kitchen")
R1 = Radiobutton(root, text="Kitchen Table", variable=radio, value="kitchen", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 7, sticky = 'w')
R1 = Radiobutton(root, text="Standard", variable=radio, value="standard", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 8, sticky = 'w')
R1 = Radiobutton(root, text="Modern", variable=radio, value="modern", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 9, sticky = 'w')
R1 = Radiobutton(root, text="Legacy", variable=radio, value="legacy", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 10, sticky = 'w')
R1 = Radiobutton(root, text="Vintage", variable=radio, value="vintage", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 11, sticky = 'w')
R1 = Radiobutton(root, text="Commander", variable=radio, value="commander", command=formatted, bg = '#19232D', fg = 'white', selectcolor = '#3E6691', activebackground = '#19232D', activeforeground = 'white')
R1.grid(column = 0, row = 12, sticky = 'w')


# labels along the top
search_term = Label(root, text = "Enter your search", justify = "left", anchor = "nw", bg = '#19232D', fg = 'white')
search_term.grid(column=1, row=0)
 
# search bar field
txt = Entry(root, width=15, bg = '#6C7073', fg = 'white')
txt.grid(column =2, row =0) 

# button widget for search bar
btn = Button(root, text = "Search", command=searched, bg = '#32414B', fg = 'white')
btn.grid(column=3, row=0, padx=20)

# label for potential errors
error_label = Label(root, text = "", bg = '#19232D')
error_label.grid(column = 4, row = 0)
       
 
# Execute Tkinter
root.mainloop()























