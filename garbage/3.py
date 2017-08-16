def handy(self, play_deck):
    a = raw_input('How many hands? ')
    for i in range(int(a)):
        h = "hand" + str(i+ 1) # dynamilly create key
        q, play_deck = self.deal(self.full_deck) # pull cards from deck
        self.dict_of_hands.setdefault(h, q) # load up dict of hands

    hand_keys = self.dict_of_hands.keys()
    the_hands = self.dict_of_hands

    first_cards = []
    second_cards = []
    for hand in the_hands:
        # print the_hands[hand][0]
        first_cards.append(the_hands[hand][0])

    for hand in the_hands:
        # print the_hands[hand][1]
        second_cards.append(the_hands[hand][1])         

    header = self.dict_of_hands.keys()


    table = texttable.Texttable()
    table.header(header)
    table.add_rows([first_cards, second_cards], header=False)
    print table.draw
