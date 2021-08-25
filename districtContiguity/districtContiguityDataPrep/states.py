STATES = {
    'AL': {'STFIPS': '01', 'Districts': {'congress20': 7, 'congress10': 7, 'state_senate': 35, 'state_house': 105}},
    'AK': {'STFIPS': '02', 'Districts': {'state_senate': 20, 'state_house': 40}},
    'AZ': {'STFIPS': '04', 'Districts': {'congress20': 9, 'congress10': 9, 'state_senate': 30}}, # multi-member house elected from each senate district
    'AR': {'STFIPS': '05', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 35, 'state_house': 100}},
    'CA': {'STFIPS': '06', 'Districts': {'congress20': 52, 'congress10': 53, 'state_senate': 40, 'state_house': 80}},
    'CO': {'STFIPS': '08', 'Districts': {'congress20': 8, 'congress10': 7, 'state_senate': 35, 'state_house': 65}},
    'CT': {'STFIPS': '09', 'Districts': {'congress20': 5, 'congress10': 5, 'state_senate': 36, 'state_house': 151}},
    'DE': {'STFIPS': '10', 'Districts': {'state_senate': 21, 'state_house': 41}},
    'DC': {'STFIPS': '11', 'Districts': {'wards': 8}},
    'FL': {'STFIPS': '12', 'Districts': {'congress20': 28, 'congress10': 27, 'state_senate': 40, 'state_house': 120}},
    'GA': {'STFIPS': '13', 'Districts': {'congress20': 14, 'congress10': 14, 'state_senate': 56, 'state_house': 180}},
    'HI': {'STFIPS': '15', 'Districts': {'congress20': 2, 'congress10': 2, 'state_senate': 25, 'state_house': 51}},
    'ID': {'STFIPS': '16', 'Districts': {'congress20': 2, 'congress10': 2, 'state_senate': 35}}, # multi-member house elected from each senate district
    'IL': {'STFIPS': '17', 'Districts': {'congress20': 17, 'congress10': 18, 'state_senate': 59, 'state_house': 118}},
    'IN': {'STFIPS': '18', 'Districts': {'congress20': 9, 'congress10': 9, 'state_senate': 50, 'state_house': 100}},
    'IA': {'STFIPS': '19', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 50, 'state_house': 100}},
    'KS': {'STFIPS': '20', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 40, 'state_house': 125}},
    'KY': {'STFIPS': '21', 'Districts': {'congress20': 6, 'congress10': 6, 'state_senate': 38, 'state_house': 100}},
    'LA': {'STFIPS': '22', 'Districts': {'congress20': 6, 'congress10': 6, 'state_senate': 39, 'state_house': 105}},
    'ME': {'STFIPS': '23', 'Districts': {'congress20': 2, 'congress10': 2, 'state_senate': 35, 'state_house': 151}},
    'MD': {'STFIPS': '24', 'Districts': {'congress20': 8, 'congress10': 8, 'state_senate': 47}}, # multi-member house
    'MA': {'STFIPS': '25', 'Districts': {'congress20': 9, 'congress10': 9, 'state_senate': 40, 'state_house': 160}},
    'MI': {'STFIPS': '26', 'Districts': {'congress20': 13, 'congress10': 14, 'state_senate': 38, 'state_house': 110}},
    'MN': {'STFIPS': '27', 'Districts': {'congress20': 8, 'congress10': 8, 'state_senate': 1, 'state_house': 1}},
    'MS': {'STFIPS': '28', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 67, 'state_house': 134}},
    'MO': {'STFIPS': '29', 'Districts': {'congress20': 8, 'congress10': 8, 'state_senate': 34, 'state_house': 163}},
    'MT': {'STFIPS': '30', 'Districts': {'congress20': 2,'state_senate': 50, 'state_house': 100}},
    'NE': {'STFIPS': '31', 'Districts': {'congress20': 3, 'congress10': 3, 'state_senate': 49}}, ## No state house in NE
    'NV': {'STFIPS': '32', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 21, 'state_house': 42}},
    'NH': {'STFIPS': '33', 'Districts': {'congress20': 2, 'congress10': 2, 'state_senate': 24, 'state_house': 1}}, ## Multi-member house election from county subdivisions.
    'NJ': {'STFIPS': '34', 'Districts': {'congress20': 12, 'congress10': 12, 'state_senate': 40}},  # multi-member house elected from each senate district
    'NM': {'STFIPS': '35', 'Districts': {'congress20': 3, 'congress10': 3, 'state_senate': 42, 'state_house': 70}},
    'NY': {'STFIPS': '36', 'Districts': {'congress20': 26, 'congress10': 27, 'state_senate': 63, 'state_house': 150}},
    'NC': {'STFIPS': '37', 'Districts': {'congress20': 14, 'congress10': 13, 'state_senate': 50, 'state_house': 120}},
    'ND': {'STFIPS': '38', 'Districts': {'state_senate': 47}}, # multi-member house elected from each senate district
    'OH': {'STFIPS': '39', 'Districts': {'congress20': 15, 'congress10': 16, 'state_senate': 33, 'state_house': 99}},
    'OK': {'STFIPS': '40', 'Districts': {'congress20': 5, 'congress10': 5, 'state_senate': 48, 'state_house': 101}},
    'OR': {'STFIPS': '41', 'Districts': {'congress20': 6, 'congress10': 5, 'state_senate': 30, 'state_house': 60}},
    'PA': {'STFIPS': '42', 'Districts': {'congress20': 17, 'congress10': 18, 'state_senate': 50, 'state_house': 203}},
    'PR': {'STFIPS': '72', 'Districts': {'state_senate': 8, 'state_house': 40}},
    'RI': {'STFIPS': '44', 'Districts': {'congress20': 2, 'congress10': 2, 'state_senate': 38, 'state_house': 75}},
    'SC': {'STFIPS': '45', 'Districts': {'congress20': 7, 'congress10': 7, 'state_senate': 46, 'state_house': 124}},
    'SD': {'STFIPS': '46', 'Districts': {'state_senate': 34}}, # multi-member house elected from each senate district (except for 2 districts drawn for VRA)
    'TN': {'STFIPS': '47', 'Districts': {'congress20': 9, 'congress10': 9, 'state_senate': 33, 'state_house': 99}},
    'TX': {'STFIPS': '48', 'Districts': {'congress20': 38, 'congress10': 36, 'state_senate': 31, 'state_house': 150}},
    'UT': {'STFIPS': '49', 'Districts': {'congress20': 4, 'congress10': 4, 'state_senate': 29, 'state_house': 75}},
    'VT': {'STFIPS': '50', 'Districts': {}}, ## Both houses have districts that election various numbers of multi-member representatives
    'VA': {'STFIPS': '51', 'Districts': {'congress20': 11, 'congress10': 11, 'state_senate': 40, 'state_house': 100}},
    'WA': {'STFIPS': '53', 'Districts': {'congress20': 10, 'congress10': 10, 'state_senate': 49}}, # multi-member house elected from each senate district
    'WV': {'STFIPS': '54', 'Districts': {'congress20': 2, 'congress10': 3}}, ## Both houses have districts that election various numbers of multi-member representatives
    'WI': {'STFIPS': '55', 'Districts': {'congress20': 8, 'congress10': 8, 'state_senate': 33, 'state_house': 99}},
    'WY': {'STFIPS': '56', 'Districts': {'state_senate': 30, 'state_house': 60}}}