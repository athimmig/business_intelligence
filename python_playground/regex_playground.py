import re

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M | re.I )

if matchObj:
    print "matchObj.group() :", matchObj.group()
    print "matchObj.group(1):", matchObj.group(1)
    print "matchObj.group(2):", matchObj.group(2)
else:
    print "No matches found."

'''Output:
matchObj.group() :  Cats are smarter than dogs
matchObj.group(1):  Cats
matchObj.group(2):  smarter
'''

title = "The Searchers (1956)"

matchObj = re.match( r'\([0-9]{4}\(', title, re.M | re.I )

if matchObj:
    print matchObj.group()
else:
    print "No match found in", title

print "Match vs Search"
print "---------------"

matchObj = re.match( r'dogs', line, re.M | re.I )

if matchObj:
    print "Match: ", matchObj.group()
else:
    print "No match."

matchObj = re.search( r'dogs', line, re.M | re.I )

if matchObj:
    print "Search(): ", matchObj.group()
else:
    print "No match."

print "Self-Understanding Check"
print "------------------------"

title = "The Searchers (1956)"

matchObj = re.search( r'\([0-9]{4}\)', title, re.I | re.M )
# Try to search this without the brackets, but using them as
# a lookahead/back

if matchObj:
    print "Found: ", matchObj.group()
else:
    print "No year found."

print "\n\nsub()"

phone = "2004-959-559 #This is a phone number"

# Delete python-style comments in string
num = re.sub(r'#.*$', "", phone ) #replace occurrences of _ with _ in _

print "Phone Num :", num

#remove anything other than digits
num = re.sub(r'\D', "", phone)
print "Phone number:", num

print "\n\nSelf-Check"
print     "----------"

#Remove year from title
titleOnly = re.sub(r'\w*\([0-9]{4}\)$', "", title )

print titleOnly

year = re.search(r'\d{4}', title )
print year.group()

print "\n\nLookaheads and stuff..."
print "-----------------------"

string = "The Terminator (1984)"

matchObj = re.search(r'.*(?= \([0-9]{4}\))', string, re.M | re.I )

if matchObj:
    print matchObj.group()
else:
    print "Not found."


# Negative lookahead: match when it isn't followed by something else
string = "Queen Bee Barbeque"

# I want to match 'que', but not "Queen" when doing a case-insensitive search
# I can do this with a positive lookahead
match = re.search(r'que(?=$)', string ) # match the "que" that's IS followed by end-of-line
print "+ Lookahead:", match.group()

# or with a negative lookahead
match = re.search(r'que(?!=\w*)', string ) # match the "que" that IS NOT followed by any word character
print "- Lookahead:", match.group()

# Cool!
# So with movie titles, there may be a year in the title.
# What if I want to extract the year that it was made from the data,
# but not the year that's part of the title itself? Lookaheads and Lookbehinds.
# In our case, since the movie's year is surrounded by (), we can look ahead and look behind for those.
# Observe:

title = "The Taking of Pelham One Two Three (1923)"
print title
print "Extracting year..."

year = re.search(r'(?<=\()\d{4}(?=\))', title)
print year.group()

# I could also strip unwanted characters to get only the match
# This line says to substitute anything that isn't a group of four digits
# that aren't surrounded by () and replace it with "". We get a string back
# rather than a match object.
year = re.sub(r'(?<!\()\D(?!\))', "", title )
print title, "was made in", year
