************************************************************************************************
Author:	Al Timofeyev
Date:	2/19/2019
Desc:	A Genetic Algorithm used to maximize a function
	f(x,y) = sin(pi*10*x+10/(1+y^2)) + ln (x^2+y^2)
	For class CS 457 Machine Learning.
************************************************************************************************

This program just maximize the function and plots the history of the fitness for each generation.
To change the population size and when the program should terminate, open the code in appropriate
IDE and scroll to the MAIN CODE SECTiON.
Change the population size and the limit to the while loop.
Some examples are:
popSize = 100
while fitnessCounter < 30

popSize = 1500
while fitnessCounter < 20

There is a limit thought.
The maximum this program can go without taking forever to end is:
popSize = 2000
while fitnessCounter < 2

Anything higher and the program will take a long time to finish.