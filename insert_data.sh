#! /bin/bash

if [[ $1 == "test" ]]
then
  PSQL="psql --username=postgres --dbname=worldcuptest -t --no-align -c"
else
  PSQL="psql --username=freecodecamp --dbname=worldcup -t --no-align -c"
fi

# Do not change code above this line. Use the PSQL variable above to query your database.
echo "$($PSQL "TRUNCATE teams,games;")"

cat games.csv | while IFS="," read YEAR ROUND WINNER OPPONENT WINNER_GOALS OPPONENT_GOALS
do
  if [[ $YEAR != year ]]
  then
    WIN="$($PSQL "SELECT name FROM teams WHERE name='$WINNER';")"
    if [[ -z $WIN ]]
    then
      INSERT_WIN_TEAM= "$($PSQL "INSERT INTO teams(name) VALUES('$WINNER');")"
      if [[ $INSERT_WIN_TEAM == 'INSERT O 1' ]]
      then
        echo $INSERT_WIN_TEAM added to teams table
      fi
    fi

    LOSE="$($PSQL "SELECT name FROM teams WHERE name='$OPPONENT';")"
    if [[ -z $LOSE ]]
    then
      INSERT_LOSE_TEAM="$($PSQL "INSERT INTO teams(name) VALUES('$OPPONENT');")"
      if [[ $INSERT_LOSE_TEAM == 'INSERT O 1' ]]
      then
        echo $INSERT_LOSE_TEAM added to teams table
      fi
    fi
    WINNER_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$WINNER';")"
    OPPONENT_ID="$($PSQL "SELECT team_id FROM teams WHERE name='$OPPONENT';")"
    INSERT_GAME_DATA="$($PSQL "INSERT INTO games(year,round,winner_id,opponent_id,winner_goals,opponent_goals) VALUES($YEAR,'$ROUND',$WINNER_ID,$OPPONENT_ID,$WINNER_GOALS,$OPPONENT_GOALS);")"
    if [[ $INSERT_GAME_DATA == "INSERT 0 1" ]]
    then
      echo Game Data entered
    fi
  fi
done
