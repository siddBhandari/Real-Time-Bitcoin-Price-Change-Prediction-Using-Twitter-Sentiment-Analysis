sampleText = 'Hello this sentence contains and s'

print(sampleText.lower())

bannedWords = ['nft', 'giveaway', 'referral']

if any(word in sampleText.lower().split(" ") for word in bannedWords):
    print('spam')
else:
    print('not Spam')

# sampleText = [word for word in sampleText.split()]
# # for word in sampleText:

# if 'giveaway' in bannedWords:
#     print("spam")
