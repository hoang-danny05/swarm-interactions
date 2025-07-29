# :cyclone: Swarm-Interactions

I recently saw swarms and thought this would be a good idea to include to our project! Still under development, of course. Our system is of two users, alice and bob. Alice talks first, and Bob responds. 
Both bots have the chance to end conversation by calling the end_conversation() method given to them. (yes, swarms is pretty cool, right?). 

All conversations are stored in the Warehouse directory. View.py allows easy parsing of each output file. 
Note: we are using openai/swarms, but there exists an enterprise-ready version of swarms at [kyegomez/swarms](https://github.com/kyegomez/swarms).

## To-do

- ~~Double runs in Testing directory~~
- Annotate a good subset of the runs
- ~~Delete result json files that have improper formatting~~ 


## :hammer: How to setup

1) Clone or download this repository
2) Create a virtual environment and use it (OPTIONAL)
```bash
python -m venv venv-chatproj
source venv-chatproj/bin/activate
```
3) Install the required dependencies
```cmd
pip install -r requirements.txt
```
- if installing swarms fails, try this command: (this uses https instead of ssh)
```
pip install git+https://github.com/openai/swarm.git
```

## Agents
Agent configurations are stored in `CONFIG.py`. 

To-do:
  - Add default configurations: `you are stubborn`, null identity, etc. 


## :clipboard: Development Notes. (v0.3 is the latest)
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
- Bots are generally more coherent because the initial prompt was changed to be from bob. 

Status of current runs:
- Warehouse stores all output
- The subfolders of Warehouse indicate the values of the different profiles. BA would mean B is in slot 1, A is in slot 2. 
