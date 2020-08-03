# Questionary
Python version: 3.6.8
<br> Dlib version: 19.8.1
<br>
<br>This project has two parts:-
1) creating a database
2) creating question with appropriate options, and a single correct answer
3) populating the question, options into GUI, and providing messages on selection of an option.
<br>
<br> <b> Part 1 </b>
<br>A list of player with details is required, with name of the players under the column 'Player'.
<br>The file format must be in .csv
<br>Using the list of names from the column 'Player'. Images of the players are downloaded.(Note: one can set the 'Usage Rights' for the images to be downloaded.)
<br>There are two image repository that is created: 
1) with only the faces of players, which is pickled 
2) with players(not specified for face images)
<br>All the images in the <u> second repository </u> are screened for the presence of a single player and then screened to recognise the faces using the respective pickle file.
<br>This forms the database of images for all the players.
<br>
<br><b> Part 2 </b>
<br>Questions are generated using question.csv(.csv file format is mandatory). The question.csv has mandatory columns: question, tag, not_flag.
Using the combination, questions are generated.
<br>
<br>Using <u> tag </u>, appropriate columns are populated, and corresponding image for each option is selected.(Note: Only one option is a correct answer.)
<br>
<br><b> Part 3 </b>
<br>Using tkinter, quesion and the corresponding options are populated on the screen. On selection of an option, a pop-up box with message appears.
<br>
<br>
<img src = 'result/image1.jpg'>
<br>
<img src = 'result/popup.jpg'>
