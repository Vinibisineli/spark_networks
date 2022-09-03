#!/usr/bin/env python3

from tokenize import String
from datetime import datetime
import json, sys

class CreateInsertData():

    global path 
    path = '/opt/airflow/dags/data/'

    def create_user_insert_data(json_file: String, sql_file: String) -> None:

        with open(path+json_file) as json_data:
            record_list = json.load(json_data)
            #print(record_list)

        the_insert = ("INSERT INTO raw.users (user_id,createdAt,updatedAt,firstName,lastName,address,city," +
        "country,zipCode,email,birthDate,gender,isSmoking,profession,income) VALUES \n")

        for idx,d in enumerate(record_list):
            row = ("("+
                d["id"]+","
                "'"+none_to_null(d["createdAt"])+"',"+
                "'"+none_to_null(d["updatedAt"])+"',"+
                "'"+none_to_null(d["firstName"])+"',"+
                "'"+none_to_null(d["lastName"])+"',"+
                "'"+none_to_null(d["address"])+"',"+
                "'"+none_to_null(d["city"])+"',"+
                "'"+none_to_null(d["country"])+"',"+
                "'"+none_to_null(d["zipCode"])+"',"+
                "'"+none_to_null(d["email"])+"',"+
                "'"+none_to_null(d["birthDate"])+"',"+
                "'"+none_to_null(d["profile"]["gender"])+"',"+
                none_to_null(str(d["profile"]["isSmoking"]))+","+
                "'"+none_to_null(d["profile"]["profession"])+"',"+
                none_to_null(d["profile"]["income"])+")"
            )
            
            if idx == len(record_list)-1:
                the_insert +=  row + " on conflict do nothing"
            else:
                the_insert +=  row + ",\n"

        with open(f"/opt/airflow/plugins/sql/{sql_file}", "w+") as sql_str:
            sql_str.write(the_insert)

# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------

    def create_subscription_insert_data(json_file: String, sql_file: String) -> None:

        with open(path+json_file) as json_data:
            record_list = json.load(json_data)
            #print(record_list)

        the_insert = ("INSERT INTO raw.subscription (user_id,createdAt,updatedAt,endDate,status,amount) VALUES \n")

        for idx,d in enumerate(record_list):
            for sub in d["subscription"]:
                row = ("("+
                    d["id"]+","
                    "'"+none_to_null(sub["createdAt"])+"',"+
                    "'"+none_to_null(sub["startDate"])+"',"+
                    "'"+none_to_null(sub["endDate"])+"',"+
                    "'"+none_to_null(sub["status"])+"',"+
                    none_to_null(sub["amount"])+")"
                )
            
            if idx == len(record_list)-1:
                the_insert +=  row + " on conflict do nothing"
            else:
                the_insert +=  row + ",\n"

        with open(f"/opt/airflow/plugins/sql/{sql_file}", "w+") as sql_str:
            sql_str.write(the_insert)

# --------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------

    def create_messages_insert_data(json_file: String, sql_file: String) -> None:

        with open(path+json_file) as json_data:
            record_list = json.load(json_data)
            #print(record_list)

        the_insert = ("INSERT INTO raw.messages (message_id,createdAt,message,reciverId,senderId) VALUES \n")

        for idx,d in enumerate(record_list):
            row = ("("+
                d["id"]+","
                "'"+none_to_null(d["createdAt"])+"',"+
                "'"+none_to_null(d["message"])+"',"+
                none_to_null(str(d["receiverId"]))+","+
                none_to_null(str(d["senderId"]))+")"
            )
            
            if idx == len(record_list)-1:
                the_insert +=  row + " on conflict do nothing"
            else:
                the_insert +=  row + ",\n"

        with open(f"/opt/airflow/plugins/sql/{sql_file}", "w+") as sql_str:
            sql_str.write(the_insert)

def none_to_null(data:String) -> String:

    if data is None or data == "None":
            data = "NULL"
    
    return data

