import logging
import json
import requests


def add_trainee(data, api_key):
    """
    {
        "discord_id": "",
        "discord_pfp": "",
        "discord_name": ""
    }
    """

    headers = {
        'authorization': f'Api-Key {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post("http://127.0.0.1:8000/trainees/", data=json.dumps(data), headers=headers)
    response_data = response.json()
    if response.status_code != 201:
        logging.debug(f"Add Trainee Response: {response_data}")

        print(response)


def add_record(data, api_key):
    """
    {
        "discord_id": "",
        "post_date":, in tz_info
        "message": "",
        "streak": None,
        "today_problems": None
    }
    """

    headers = {
        'authorization': f'Api-Key {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post("http://127.0.0.1:8000/records/", data=json.dumps(data), headers=headers)
    response_data = response.json()
    if response.status_code != 201:
        logging.debug(f"Add Record Response: {response_data}")
        print(response)

# def add_record(record_info):
#     """
#     Add a record to the trainee_records table.
#
#     Args:
#         record_info (list): A list containing the record information in the following order:
#                             [discord_id, discord_name,post_date, message, streak, today_problems]
#
#     Returns:
#         bool: True if the record is successfully added, False otherwise.
#     """
#     # Unpack record information
#     discord_id, discord_name, post_date, message, streak, today_problems = record_info
#
#     # Connect to the database
#     conn = sqlite3.connect("trainee.db")
#     cur = conn.cursor()
#
#     try:
#         # Check if discord_id is associated with a trainee, if not, add it
#         cur.execute("SELECT COUNT(*) FROM trainees WHERE discord_id = ?", (discord_id,))
#         if cur.fetchone()[0] == 0:
#             # If discord_id is not associated with a trainee, add it with default values
#             cur.execute(
#                            VALUES (?, ?, 0, 0, 0, 0)""",
#                 (discord_id, discord_name),
#             )
#             print(f"added {discord_name} to the database")
#
#         # Get the current date
#         if not post_date:
#             cur.execute(
#                 "SELECT MAX(post_date) FROM trainee_records WHERE discord_id = ?",
#                 (discord_id,),
#             )
#             post_date = cur.fetchone()[0]
#         # Insert the record into trainee_records table
#         cur.execute(
#             """
#         INSERT INTO trainee_records
#         (discord_id, discord_name, post_date, message, streak, today_problems)
#          VALUES (?, ?, ?, ?, ?, ?)""",
#             (discord_id, discord_name, post_date, message, streak, today_problems),
#         )
#         # print((discord_id, discord_name, post_date,
#         # message, streak, today_problems))
#
#         # Commit the transaction
#         conn.commit()
#
#         return True
#     except Exception as e:
#         print("Error adding record:", e)
#         conn.rollback()
#         return False
#     finally:
#         conn.close()
#
#
# class Stats:
#
#     @staticmethod
#     def highest_streaker() -> tuple | None:
#         # Connect to the database
#         conn = sqlite3.connect("trainee.db")
#         cur = conn.cursor()
#
#         # get the highest streaker
#         cur.execute(
#             """SELECT discord_id,discord_name,highest_streak
#                 from trainees
#                 ORDER BY
#                 highest_streak DESC
#                 LIMIT 1"""
#         )
#
#         return cur.fetchone()
#
#     @staticmethod
#     def highest_current_streaker() -> tuple | None:
#         # Connect to the database
#         conn = sqlite3.connect("trainee.db")
#         cur = conn.cursor()
#
#         # get the highest streaker
#         cur.execute(
#             """SELECT discord_id,discord_name,current_streak
#                 from trainees
#                 ORDER BY
#                 current_streak DESC
#                 LIMIT 1"""
#         )
#
#         return cur.fetchone()
#
#     @staticmethod
#     def highest_problems_solver():
#         # Connect to the database
#         conn = sqlite3.connect("trainee.db")
#         cur = conn.cursor()
#
#         # get the highest streaker
#         cur.execute(
#             """SELECT discord_id,discord_name,total_problems
#                 from trainees
#                 ORDER BY
#                 total_problems DESC
#                 LIMIT 1
#             """
#         )
#
#         return cur.fetchone()
#
#     @staticmethod
#     def top_ten(amount=10):
#         # Connect to the database
#         conn = sqlite3.connect("trainee.db")
#         cur = conn.cursor()
#
#         # get the highest streaker
#
#         cur.execute(
#             """
#             SELECT ROW_NUMBER() OVER(ORDER BY highest_streak DESC, total_problems DESC) AS row_number,
#               discord_name,
#               total_problems,
#               highest_streak
#             FROM trainees
#             ORDER BY highest_streak DESC, total_problems DESC
#             LIMIT ?
#             """, (str(amount),))
#         return cur.fetchall()
