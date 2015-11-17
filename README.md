# BlackBox2015
Code from the Black Box project in I501 Fall 2015

__Team members__: Leif Christiansen, Moses Stamboulian, Kyle Overton, Derrick Whitley

The Black Box may be found here: http://www.informatics.indiana.edu/rocha/blackbox/BlackBox_N.php

File Descriptions
---------------------------------------------------
___Model___
*****************************************************
A partially functional model Black Box. Can be viewed here: http://cgi.soic.indiana.edu/~leifchri/WebGL/Class/blackBoxModel.html

___Scripts___
******************************************************

__scraperByQuad__: Opens a firefox window and automatically steps through the Black Box. The states of the Black Box are recorded in .txt files

__hypTest.py__: An earlier version of scraperByQuad. Performs various tests on Q4 while gathering data.

__mutations.py__: Reads files created by scraperByQuad performs. Has functions for performing a variety of tests, printing states of the Black Box, and creating networks visualizing the Black Box's changes.

Dependencies
--------------------------------------------------
__Mozilla Firefox__

__Python Libraries__:
Numpy, Selenuim, Pandas, NetworkX, BeautifulSoup, Matplotlib

If you are missing any of these libraries, in the terminal type:

    pip install (name_of_dependecy)
