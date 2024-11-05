# Swarm-Interactions

I recently saw swarms and thought this would be a good idea to include to our project! Still under development, of course. Our system is of two users, alice and bob. Alice talks first, and Bob responds. 
Both bots have the chance to end conversation by calling the end_conversation() method given to them. (yes, swarms is pretty cool, right?). 

All conversations are stored in the Warehouse directory. Sorry if they aren't formatted nicely. 

## setup notes

Create a virtual environment in this directory
```
python -m venv venv-chatproj
```

-install swarms
- install requirements.txt

to use gpt-3.5 turbo
```
cp ./other/types.py ./venv-chatproj/lib/python3.10/site-packages/swarm/types.py
```

## Development Notes. (v0.3 is the latest)
Making the bots play their own roles is complicated. The bots don't expect to be addressed in the third person. So, when the system prompt is added to the messages, it bugs everything out.

Messages as of v0.1:
  - Initial system prompt ONLY given to Alice
  - Alice's response was made to be the users (not intended)
  - Agents would tend to end conversation after the first message
  - Message Array = [alice (user), bob, alice...]

Status of v0.2:
- Initial system prompt visible to both bots
- Message Array = [Initial Prompt(user), alice, bob, alice...]
- Agents would lose their sense of self and start talking about Alice and Bob in third person. 

Status of v0.3:
- Code readability significantly improved
- Restructured the program to look a lot like mathematical induction
- Message array is the same -> 
  - Agents still occasionally talk about themselves or others in third person. 

Status of v0.4:
- HUGE overhaul (kinda)
- No signs of bots talking about themselves (yet) from skimming the work
- Added ability to iterate through all possible personality types. 
- Need for a conversation limit or a neutral third party that judges the AIs impartially. 

Status of v0.5:
- Allows users to change the model in a variable
- Bots are now told to give reasons for ending the conversations. Ending conversation is no longer omitted. 

