# :cyclone: Swarm-Interactions

I recently saw swarms and thought this would be a good idea to include to our project! Still under development, of course. Our system is of two users, alice and bob. Alice talks first, and Bob responds. 
Both bots have the chance to end conversation by calling the end_conversation() method given to them. (yes, swarms is pretty cool, right?). 

All conversations are stored in the Warehouse directory. View.py allows easy parsing of each output file. 
Note: we are using openai/swarms, but there exists an enterprise-ready version of swarms at [kyegomez/swarms](https://github.com/kyegomez/swarms).

## To-do

- ~~Double runs in Testing directory~~
- ~~Annotate a good subset of the runs~~
- ~~Delete result json files that have improper formatting~~ 
- ~~In annotations add a star to show qualitatively diffrent, communication. (make it a button on view GUI)~~

## Notes

In `Warehouse/test/AE` all runs are empty. Starting annotation on `Warehouse/test/AF`.

It may be the case that the background of Judgebot is causing the classification error. 

Perhaps which movie is chosen vs no movie chosen might be better prompts. Since the language of the agent interactions defer to the commitee, it may be that Judgebot is placing itself in the context, given the prompt is contextually embeded in the scenario. 

**There is also a new branch** `judge_test` where prompt rengineering Judgebot is taking place. 

### Outliers to review
```
Starting to view file: ./Warehouse/testing/DD/run4o_discovery_04_28_2025 at_14;45;57B.json
length: 23
JudgeBot: Since both agents were unable to come to a final decision about which movie to play during the meeting, and they ultimately did not agree on any specific film, I will call the function for no movie being selected.

no_decision
Getting judgement...
Judge bot thinks nobody won

        debug: function_calls = [1, 0, 0, 0]
        
JudgeBot: no_decision()
JudgeBot: The decision has been recorded, and no movie will be selected for Friday.
function called
Valid response! 
```
```
Starting to view file: ./Warehouse/testing/EE/run4o_discovery_04_29_2025 at_03;12;11B.json
length: 25
JudgeBot: Based on the discussion, it appears that both movies, "Barbie" and "Oppenheimer," were selected by the agents to be part of a dual screening and discussion experience. Therefore, I will call the function `both_movies`.
Getting judgement...
Judge bot thinks, both movies were selected

        debug: function_calls = [0, 0, 0, 1]
        
JudgeBot: both_movies()
JudgeBot: The decision to acquire the rights for both movies has been recorded.
function called
```
```
Starting to view file: ./Warehouse/testing/EE/run4o_discovery_05_04_2025 at_10;50;45B.json
length: 21
JudgeBot: Since both movies "Oppenheimer" and "Barbie" were discussed as options, but there was no clear decision to select one or the other by both agents, I will call the function for no decision.

no_decision
Getting judgement...
Judge bot thinks nobody won

        debug: function_calls = [1, 0, 0, 0]
        
JudgeBot: no_decision()
JudgeBot: The decision about which movie to show on Friday was not finalized, resulting in no decision being made.
function called
Valid response!
```
```
Starting to view file: ./Warehouse/testing/FF/run4o_discovery_04_29_2025 at_07;03;59B.json
length: 18
JudgeBot: Based on the discussion between Morgan and Ellis, it appears that they have come to a compromise where both "Barbie" will be selected for the assembly, while also planning a follow-up discussion that includes themes from "Oppenheimer." Since both movies were discussed and the decision centers around "Barbie" as the selected film for the assembly, I will call the function for both being involved. 

Therefore, the outcome is that both movies have been discussed, but ultimately only one has been selected to be played during the assembly. 

I will call the function for both_movies.
Getting judgement...
Judge bot thinks, both movies were selected

        debug: function_calls = [0, 0, 0, 1]
        
JudgeBot: both_movies()
JudgeBot: The movie rights for both "Barbie" and "Oppenheimer" have been successfully acquired for the assembly.
function called
Valid response! 
```
```
Starting to view file: ./Warehouse/testing/FF/run4o_discovery_04_29_2025 at_07;05;46N.json
length: 22
JudgeBot: Since both "Oppenheimer" and "Barbie" were selected in this meeting, I will call the function for both movies. 

Therefore, I will call: **both_movies**.
Getting judgement...
Judge bot thinks, both movies were selected

        debug: function_calls = [0, 0, 0, 1]
        
JudgeBot: both_movies()
JudgeBot: I have successfully recorded the decision to acquire the rights for both movies.
function called
Valid response! 
```
```
Starting to view file: ./Warehouse/testing/CD/run4o_discovery_04_28_2025 at_13;06;51B.json
length: 25
JudgeBot: Both movies have been selected in this meeting. The final outcome is to showcase "Barbie" as the primary film, followed by discussions on "Oppenheimer." 

I will call the function for both movies.
Getting judgement...
Judge bot thinks, both movies were selected

        debug: function_calls = [0, 0, 0, 1]
        
JudgeBot: both_movies()
JudgeBot: The rights for both movies have been successfully acquired.
function called
Valid response! 
Finished file ./Warehouse/testing/CD/run4o_discovery_04_28_2025 at_13;06;51B.json
```
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
