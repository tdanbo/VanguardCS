import re

string = " Master Active. The character can subdue an enemy with a passed [Persuasive←Resolute] test. A subdued enemy can be forced to stand down and negotiate, to flee from an ongoing battle (if possible), or surrender if it is impossible to flee. When already in combat, the enemy must first be wounded by the character or by one of the character's allies before it can be subdued."
matches = re.findall(r'\b\d*[dD]\d+\+?\d*\b', string)
if matches:
    print(matches)  # Output: ['1D8', '4d20', '2d10+2']
else:
    pass
