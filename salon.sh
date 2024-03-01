#!/bin/bash
# salon appoinment application

PSQL="psql -X --username=freecodecamp --dbname=salon --tuples-only -c"

echo -e "\n~~~ Salon Appointment Application ~~~\n"

MAIN_MENU() {

if [[ $1 ]]
then
  echo -e "\n$1"
fi

echo Welcome! What can we do for you?

SERVICES_MENU=$($PSQL "SELECT * FROM services ORDER BY service_id;")

echo "$SERVICES_MENU" | while read SERVICE_MENU_ID BAR SERVICE
do
  ID=$(echo -e $SERVICE_MENU_ID | sed 's/ //g')
  NAME=$(echo -e $SERVICE | sed 's/ //g')
  echo "$ID) $NAME"
done
read SERVICE_ID_SELECTED

case $SERVICE_ID_SELECTED in
  [1-5]) APPOINTMENT_MENU ;;
  2) EXIT ;;
  *) MAIN_MENU "Please enter a valid option." ;;
esac
}

APPOINTMENT_MENU() {
# schedule appointment
# get customers phone number
echo -e "\nPlease enter your phone number:"
read CUSTOMER_PHONE

CUSTOMER_ID=$($PSQL "SELECT customer_id FROM customers WHERE phone='$CUSTOMER_PHONE';")
# if no phone number listed
if [[ -z $CUSTOMER_ID ]]
then
  # get customer name
  echo -e "\nPlease enter your name:"
  read CUSTOMER_NAME
  # insert the phone number and name to create a customer entry
  INSERT_CUSTOMER=$($PSQL "INSERT INTO customers(name,phone) VALUES('$CUSTOMER_NAME','$CUSTOMER_PHONE');")
  # get customer_id
  CUSTOMER_ID=$($PSQL "SELECT customer_id FROM customers WHERE phone='$CUSTOMER_PHONE';")
fi

# schedule an appointment time
echo -e "\nWhat time would you like to schedule?"
read SERVICE_TIME
CUSTOMER_APPOINTMENT=$($PSQL "INSERT INTO appointments(customer_id,service_id,time) VALUES($CUSTOMER_ID,$SERVICE_ID_SELECTED,'$SERVICE_TIME');")

# collect customer appointment information
CUSTOMER_TIME=$($PSQL "SELECT time FROM appointments WHERE customer_id=$CUSTOMER_ID AND service_id=$SERVICE_ID_SELECTED;")
CUSTOMER_SERVICE=$($PSQL "SELECT name FROM services WHERE service_id=$SERVICE_ID_SELECTED;")
CUSTOMER_APPOINTMENT_NAME=$($PSQL "SELECT name FROM customers WHERE customer_id=$CUSTOMER_ID;")

# print customer appointment inormation
TIME=$(echo $CUSTOMER_TIME | sed 's/ //g')
SERVICE=$(echo $CUSTOMER_SERVICE | sed 's/ //g')
NAME=$(echo $CUSTOMER_APPOINTMENT_NAME | sed 's/ //g')
echo -e "\nI have put you down for a $SERVICE at $TIME, $NAME."
}

EXIT() {
# exit function
echo -e "\nThank you for visting!\n"
}

MAIN_MENU
