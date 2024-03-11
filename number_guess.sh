#!/bin/bash

# sql query api
PSQL="psql --username=freecodecamp --dbname=number_guess -t --no-align -c"

# generate random number and store it in a variable
RANDOM_NUMBER=$(( RANDOM % 1000 + 1 ))

# ask for username
echo Enter your username: 
read USERNAME

USER_ID=$($PSQL "SELECT user_id FROM game_info WHERE username='$USERNAME';")

if [[ -z $USER_ID ]]
then
  # greet the new user
  echo "Welcome, $USERNAME! It looks like this is your first time here."
else
  # get username's info from database
  GAMES_PLAYED=$($PSQL "SELECT games_played FROM game_info WHERE user_id=$USER_ID;")
  BEST_GAME=$($PSQL "SELECT best_game FROM game_info WHERE user_id=$USER_ID;")
  USERNAME=$($PSQL "SELECT username FROM game_info WHERE user_id=$USER_ID;")
  # greet returning user
  echo "Welcome back, $USERNAME! You have played $GAMES_PLAYED games, and your best game took $BEST_GAME guesses."
fi
echo Guess the secret number between 1 and 1000: 
read NUMBER_GUESS

while [[ ! $NUMBER_GUESS =~ ^[0-9]+$ ]];
do
  echo That is not an integer, guess again: 
  read NUMBER_GUESS
done
# track number of guesses
GUESSES=1
if [[ $NUMBER_GUESS == $RANDOM_NUMBER ]]
then
  # got it on the first try!
  echo "You guessed it in $GUESSES tries. The secret number was $RANDOM_NUMBER. Nice job!"
else
  # is guess higher or lower than random number
  while [[ $NUMBER_GUESS != $RANDOM_NUMBER ]];
  do
    if [[ $NUMBER_GUESS -gt $RANDOM_NUMBER ]]
    then
      echo "It's lower than that, guess again: "
      read NUMBER_GUESS
    else
      echo "It's higher than that, guess again: "
      read NUMBER_GUESS
    fi
    # again, check to make sure the input was a number
    while [[ ! $NUMBER_GUESS =~ ^[0-9]+$ ]];
    do
      echo That is not an integer, guess again: 
      read NUMBER_GUESS
    done
    ((GUESSES++))
  done
fi
echo "You guessed it in $GUESSES tries. The secret number was $RANDOM_NUMBER. Nice job!"
# update the database with the user info:
if [[ -z $USER_ID ]]
then
  ENTER_INFO=$($PSQL "INSERT INTO game_info(username,games_played,best_game) VALUES('$USERNAME',1,$GUESSES);")
else
  UPDATE_GAMES_PLAYED=$($PSQL "UPDATE game_info SET games_played=$GAMES_PLAYED+1 WHERE user_id=$USER_ID;")
  if [[ $GUESSES -lt $BEST_GAME ]]
  then
    UPDATE=$($PSQL "UPDATE game_info SET best_game=$GUESSES WHERE user_id=$USER_ID;")
  fi
fi
