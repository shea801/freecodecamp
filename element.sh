#!/bin/bash

# info collected from database is:
# (1) atomic_number, (2) name, (3) symbol, (4) type, (5) atomic_mass, 
# (6) melting_point_celsius, and (7) boiling_point_celsius
# output should be:
# "The element with atomic number (1) is (2) (3). It's a (4), with a mass of (5) amu. (2)
# has a melting point of (6) celsius and a boiling point of (7) celsius."

PSQL="psql --username=freecodecamp --dbname=periodic_table -t --no-align -c"
# see if the user input an argument along with the file execution
if [[ -z $1 ]]
then
  echo Please provide an element as an argument.
  # determine if the input is a number, a letter, or a word
else
  if [[ ! $1 =~ ^[0-9]+$ ]]
  then
    # if non-numeric input
    ATOMIC_NUMBER=$($PSQL "SELECT atomic_number FROM elements WHERE symbol='$1' OR name='$1';")
    ELEMENT_NAME=$($PSQL "SELECT name FROM elements WHERE symbol='$1' OR name='$1';")
    ELEMENT_SYMBOL=$($PSQL "SELECT symbol FROM elements WHERE symbol='$1' OR name='$1';")
  else
    ATOMIC_NUMBER=$($PSQL "SELECT atomic_number FROM elements WHERE atomic_number=$1;")
    ELEMENT_NAME=$($PSQL "SELECT name FROM elements WHERE atomic_number=$1;")
    ELEMENT_SYMBOL=$($PSQL "SELECT symbol FROM elements WHERE atomic_number=$1;")
  fi
  # Determine if the provided value is valid
  if [[ -z $ATOMIC_NUMBER || -z $ELEMENT_NAME || -z $ELEMENT_SYMBOL ]]
  then
    echo I could not find that element in the database.
  else
    TYPE=$($PSQL "SELECT types.type FROM properties INNER JOIN types USING(type_id) WHERE atomic_number=$ATOMIC_NUMBER;")
    ATOMIC_MASS=$($PSQL "SELECT atomic_mass FROM properties WHERE atomic_number=$ATOMIC_NUMBER;")
    MELTING_POINT=$($PSQL "SELECT melting_point_celsius FROM properties WHERE atomic_number=$ATOMIC_NUMBER;")
    BOILING_POINT=$($PSQL "SELECT boiling_point_celsius FROM properties WHERE atomic_number=$ATOMIC_NUMBER;")
    # print message
    echo -e "The element with atomic number $ATOMIC_NUMBER is $ELEMENT_NAME ($ELEMENT_SYMBOL). It's a $TYPE, with a mass of $ATOMIC_MASS amu. $ELEMENT_NAME has a melting point of $MELTING_POINT celsius and a boiling point of $BOILING_POINT celsius."
  fi
fi
