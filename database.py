import sqlite3


def create_triggers(cur):
    # Create trigger to update highest_streak
    cur.execute(
        """CREATE TRIGGER IF NOT EXISTS update_highest_streak
                    AFTER INSERT ON trainee_records
                    BEGIN
                        UPDATE trainees
                        SET highest_streak = (
                            SELECT MAX(streak) FROM trainee_records
                            WHERE trainee_records.discord_id = trainees.discord_id
                        )
                        WHERE trainees.discord_id = NEW.discord_id;
                    END
                """
    )

    # Create trigger to update current_streak
    cur.execute(
        """CREATE TRIGGER IF NOT EXISTS update_current_streak
                    AFTER INSERT ON trainee_records
                    BEGIN
                        UPDATE trainees
                        SET current_streak = NEW.current_streak
                        WHERE trainees.discord_id = NEW.discord_id
                        AND NEW.streak >= 0;
                    END
                """
    )



    # Create trigger to update total_days
    cur.execute(
        """CREATE TRIGGER IF NOT EXISTS update_total_days
                    AFTER INSERT ON trainee_records
                    BEGIN
                        UPDATE trainees
                        SET total_days = total_days + 1
                        WHERE trainees.discord_id = NEW.discord_id;
                    END
                """
    )

    # Create trigger to update total_problems
    cur.execute(
        """CREATE TRIGGER IF NOT EXISTS update_total_problems
                    AFTER INSERT ON trainee_records
                    BEGIN
                        UPDATE trainees
                        SET total_problems = total_problems + NEW.today_problems
                        WHERE trainees.discord_id = NEW.discord_id;
                    END
                """
    )


def create_tables_if_not_exist():
    # Connect to the database
    conn = sqlite3.connect("trainee.db")
    cur = conn.cursor()

    # Check if the tables exist
    cur.execute(
        """SELECT count(name) FROM sqlite_master
        WHERE type='table' AND name='trainees' """
    )
    trainees_exists = cur.fetchone()[0]

    cur.execute(
        """SELECT count(name) FROM sqlite_master
        WHERE type='table' AND name='trainee_records' """
    )
    trainee_records_exists = cur.fetchone()[0]

    # If the tables don't exist, create them
    if not trainees_exists:
        cur.execute(
            """CREATE TABLE trainees (
                    discord_id TEXT PRIMARY KEY,
                    discord_name TEXT,
                    highest_streak INTEGER,
                    current_streak INTEGER,
                    total_days INTEGER,
                    total_problems INTEGER,
                    UNIQUE (discord_id)

        )"""
        )

    if not trainee_records_exists:
        cur.execute(
            """CREATE TABLE trainee_records (
                    discord_id TEXT ,
                    discord_name TEXT,
                    post_date TEXT,
                    message TEXT,
                    streak INTEGER,
                    today_problems INTEGER,
                    FOREIGN KEY (discord_id) REFERENCES trainees (discord_id),
                    UNIQUE (discord_id, post_date)
        )"""
        )

    if not (trainees_exists and trainee_records_exists):
        create_triggers(cur)

    conn.commit()
    conn.close()


def add_record(record_info):
    """
    Add a record to the trainee_records table.

    Args:
        record_info (list): A list containing the record information in the following order:
                            [discord_id, discord_name,post_date, message, streak, today_problems]

    Returns:
        bool: True if the record is successfully added, False otherwise.
    """
    # Unpack record information
    discord_id, discord_name, post_date, message, streak, today_problems = record_info

    # Connect to the database
    conn = sqlite3.connect("trainee.db")
    cur = conn.cursor()

    try:
        # Check if discord_id is associated with a trainee, if not, add it
        cur.execute("SELECT COUNT(*) FROM trainees WHERE discord_id = ?", (discord_id,))
        if cur.fetchone()[0] == 0:
            # If discord_id is not associated with a trainee, add it with default values
            cur.execute(
                """INSERT INTO trainees (discord_id, discord_name, highest_streak, current_streak, total_days, total_problems)
                           VALUES (?, ?, 0, 0, 0, 0)""",
                (discord_id, discord_name),
            )
            print(f"added {discord_name} to the database")

        # Get the current date
        if not post_date:
            cur.execute(
                "SELECT MAX(post_date) FROM trainee_records WHERE discord_id = ?",
                (discord_id,),
            )
            post_date = cur.fetchone()[0]
        # Insert the record into trainee_records table
        cur.execute(
            """
        INSERT INTO trainee_records
        (discord_id, discord_name, post_date, message, streak, today_problems)
         VALUES (?, ?, ?, ?, ?, ?)""",
            (discord_id, discord_name, post_date, message, streak, today_problems),
        )
        # print((discord_id, discord_name, post_date,
        # message, streak, today_problems))

        # Commit the transaction
        conn.commit()

        return True
    except Exception as e:
        print("Error adding record:", e)
        conn.rollback()
        return False
    finally:
        conn.close()


class Stats:

    @staticmethod
    def highest_streaker() -> tuple | None:
        # Connect to the database
        conn = sqlite3.connect("trainee.db")
        cur = conn.cursor()

        # get the highest streaker
        cur.execute(
            """SELECT discord_id,discord_name,highest_streak
                from trainees 
                ORDER BY 
                highest_streak DESC 
                LIMIT 1"""
        )

        return cur.fetchone()

    @staticmethod
    def highest_current_streaker() -> tuple | None:
        # Connect to the database
        conn = sqlite3.connect("trainee.db")
        cur = conn.cursor()

        # get the highest streaker
        cur.execute(
            """SELECT discord_id,discord_name,current_streak
                from trainees 
                ORDER BY 
                current_streak DESC 
                LIMIT 1"""
        )

        return cur.fetchone()

    @staticmethod
    def highest_problems_solver():
        # Connect to the database
        conn = sqlite3.connect("trainee.db")
        cur = conn.cursor()

        # get the highest streaker
        cur.execute(
            """SELECT discord_id,discord_name,total_problems
                from trainees 
                ORDER BY 
                total_problems DESC 
                LIMIT 1
            """
        )

        return cur.fetchone()

    @staticmethod
    def top_ten(amount=10):
        # Connect to the database
        conn = sqlite3.connect("trainee.db")
        cur = conn.cursor()

        # get the highest streaker

        cur.execute(
            """
            SELECT ROW_NUMBER() OVER(ORDER BY highest_streak DESC, total_problems DESC) AS row_number,
              discord_name,
              total_problems,
              highest_streak
            FROM trainees
            ORDER BY highest_streak DESC, total_problems DESC
            LIMIT ?
            """
        ,(str(amount),))
        return cur.fetchall()
