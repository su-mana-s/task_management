
import sqlite3
import bcrypt


DB_NAME = "inward_outward.db"


# ============================================================
# CONNECTION
# ============================================================

def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# ============================================================
# COLUMN HELPERS
# ============================================================

def column_exists(
    cursor,
    table_name,
    column_name
):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    return any(
        row[1] == column_name
        for row in columns
    )


def add_column_if_missing(
    cursor,
    table_name,
    column_name,
    definition
):

    if not column_exists(
        cursor,
        table_name,
        column_name
    ):

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {definition}
            """
        )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ========================================================
        # USERS
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                role TEXT NOT NULL
                    CHECK(
                        role IN (
                            'Admin',
                            'Employee',
                            'Accounts'
                        )
                    ),

                is_active INTEGER DEFAULT 1
            )
        """)


        # ========================================================
        # CLIENTS
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT UNIQUE NOT NULL,

                mobile TEXT,

                email TEXT,

                address TEXT,

                pan TEXT,

                tan TEXT,

                gst TEXT,

                file_no TEXT,

                aadhar TEXT
            )
        """)


        # ========================================================
        # CLIENT MIGRATIONS
        # ========================================================

        add_column_if_missing(
            cursor,
            "clients",
            "mobile",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "email",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "address",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "pan",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "tan",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "gst",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "file_no",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "clients",
            "aadhar",
            "TEXT"
        )


        # ========================================================
        # MAIN RECORDS
        #
        # IMPORTANT STATUS VALUES
        #
        # 0  = Not Started / Pending
        # 10 = In Progress
        # 1  = Completed / Work Done
        # 2  = Dispatched
        #
        # records.status is the ONLY current status.
        #
        # There is deliberately no separate work_status column.
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (

                inward_id INTEGER PRIMARY KEY AUTOINCREMENT,

                date_of_entry DATE NOT NULL,

                date_of_receipt DATE NOT NULL,

                client_id INTEGER,

                department TEXT NOT NULL,

                miscellaneous_details TEXT,

                nature_of_papers TEXT NOT NULL,

                entered_by INTEGER,

                assigned_to INTEGER,

                how_received TEXT NOT NULL,

                status INTEGER DEFAULT 0,

                date_of_completion DATE,

                details_of_work_done TEXT,

                date_of_despatch DATE,

                how_despatched TEXT,

                bill_raised TEXT
                    CHECK(
                        bill_raised IN ('Y', 'N')
                    ),

                bill_number TEXT,

                bill_date DATE,

                bill_amount REAL DEFAULT 0,

                actual_amount_received REAL DEFAULT 0,

                amount_pending_receipt REAL DEFAULT 0,

                FOREIGN KEY(client_id)
                    REFERENCES clients(id),

                FOREIGN KEY(entered_by)
                    REFERENCES users(id),

                FOREIGN KEY(assigned_to)
                    REFERENCES users(id)
            )
        """)


        # ========================================================
        # RECORD MIGRATIONS
        # ========================================================

        add_column_if_missing(
            cursor,
            "records",
            "completed_by",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "records",
            "dispatched_by",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "records",
            "billed_by",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "records",
            "bill_raised_at",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "records",
            "dispatch_at",
            "TEXT"
        )

        add_column_if_missing(
            cursor,
            "records",
            "how_despatched",
            "TEXT"
        )


        # ========================================================
        # NORMALIZE RECORD STATUS
        #
        # If an old database has NULL status values,
        # treat them as Not Started.
        # ========================================================

        cursor.execute("""
            UPDATE records
            SET status = 0
            WHERE status IS NULL
        """)


        # ========================================================
        # PAYMENT TRANSACTIONS
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                record_id INTEGER NOT NULL,

                amount REAL NOT NULL
                    CHECK(amount > 0),

                payment_mode TEXT NOT NULL,

                payment_date DATE NOT NULL,

                received_by INTEGER NOT NULL,

                notes TEXT,

                created_at TEXT
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(record_id)
                    REFERENCES records(inward_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(received_by)
                    REFERENCES users(id)
            )
        """)


        # ========================================================
        # ACTIVITY / AUDIT LOG
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                record_id INTEGER NOT NULL,

                action_type TEXT NOT NULL,

                performed_by INTEGER NOT NULL,

                action_date TEXT
                    DEFAULT CURRENT_TIMESTAMP,

                amount REAL,

                payment_mode TEXT,

                description TEXT,

                FOREIGN KEY(record_id)
                    REFERENCES records(inward_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(performed_by)
                    REFERENCES users(id)
            )
        """)


        # ========================================================
        # TASK UPDATES / WORK HISTORY
        #
        # IMPORTANT:
        #
        # The CURRENT status is stored ONLY in:
        #
        #     records.status
        #
        # task_updates is only a history table.
        #
        # It does NOT contain:
        #
        #     status
        #     work_status
        #
        # It stores:
        #
        #     record_id
        #     updated_by
        #     update_date
        #     description
        #     created_at
        # ========================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_updates (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                record_id INTEGER NOT NULL,

                updated_by INTEGER NOT NULL,

                update_date DATE NOT NULL
                    DEFAULT CURRENT_DATE,

                description TEXT NOT NULL,

                created_at TEXT
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(record_id)
                    REFERENCES records(inward_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(updated_by)
                    REFERENCES users(id)
            )
        """)


        # ========================================================
        # TASK UPDATES MIGRATION
        #
        # Older versions of the application may have created:
        #
        #     task_updates.work_status
        #
        # or:
        #
        #     task_updates.status
        #
        # Sometimes those columns were also NOT NULL.
        #
        # Since SQLite does not reliably support removing columns
        # across all SQLite versions, rebuild the table when one
        # of these obsolete columns exists.
        # ========================================================

        cursor.execute(
            "PRAGMA table_info(task_updates)"
        )

        task_update_columns = cursor.fetchall()

        task_update_column_names = [
            row[1]
            for row in task_update_columns
        ]

        legacy_work_status_exists = (
            "work_status"
            in task_update_column_names
        )

        legacy_status_exists = (
            "status"
            in task_update_column_names
        )


        if (
            legacy_work_status_exists
            or legacy_status_exists
        ):

            # ====================================================
            # RENAME OLD TABLE
            # ====================================================

            cursor.execute("""
                ALTER TABLE task_updates
                RENAME TO task_updates_old
            """)


            # ====================================================
            # CREATE NEW TABLE
            # ====================================================

            cursor.execute("""
                CREATE TABLE task_updates (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    record_id INTEGER NOT NULL,

                    updated_by INTEGER NOT NULL,

                    update_date DATE NOT NULL
                        DEFAULT CURRENT_DATE,

                    description TEXT NOT NULL,

                    created_at TEXT
                        DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY(record_id)
                        REFERENCES records(inward_id)
                        ON DELETE CASCADE,

                    FOREIGN KEY(updated_by)
                        REFERENCES users(id)
                )
            """)


            # ====================================================
            # COPY OLD HISTORY
            #
            # Do NOT copy:
            #
            #     status
            #     work_status
            #
            # because current status is now stored in
            # records.status.
            #
            # Existing history is otherwise preserved.
            # ====================================================

            old_columns = [
                row[1]
                for row in task_update_columns
            ]

            # ----------------------------------------------------
            # Determine which old columns actually exist.
            # ----------------------------------------------------

            has_id = "id" in old_columns
            has_record_id = "record_id" in old_columns
            has_updated_by = "updated_by" in old_columns
            has_update_date = "update_date" in old_columns
            has_description = "description" in old_columns
            has_created_at = "created_at" in old_columns


            # ----------------------------------------------------
            # The old schema should normally contain all of these.
            #
            # This migration is defensive so that partially
            # migrated databases do not immediately crash.
            # ----------------------------------------------------

            if (
                has_id
                and has_record_id
                and has_updated_by
            ):

                # ------------------------------------------------
                # Build safe expressions for optional old columns.
                # ------------------------------------------------

                if has_update_date:

                    old_update_date = """
                        COALESCE(
                            update_date,
                            CURRENT_DATE
                        )
                    """

                else:

                    old_update_date = """
                        CURRENT_DATE
                    """


                if has_description:

                    old_description = """
                        COALESCE(
                            description,
                            'Previous task update'
                        )
                    """

                else:

                    old_description = """
                        'Previous task update'
                    """


                if has_created_at:

                    old_created_at = """
                        COALESCE(
                            created_at,
                            CURRENT_TIMESTAMP
                        )
                    """

                else:

                    old_created_at = """
                        CURRENT_TIMESTAMP
                    """


                cursor.execute(f"""
                    INSERT INTO task_updates
                    (
                        id,
                        record_id,
                        updated_by,
                        update_date,
                        description,
                        created_at
                    )

                    SELECT
                        id,
                        record_id,
                        updated_by,
                        {old_update_date},
                        {old_description},
                        {old_created_at}

                    FROM task_updates_old
                """)


            # ====================================================
            # REMOVE OLD TABLE
            # ====================================================

            cursor.execute("""
                DROP TABLE task_updates_old
            """)


        else:

            # ====================================================
            # CURRENT TABLE MIGRATIONS
            #
            # If the table is already the new design, make sure
            # the expected columns exist.
            # ====================================================

            add_column_if_missing(
                cursor,
                "task_updates",
                "updated_by",
                "INTEGER"
            )

            add_column_if_missing(
                cursor,
                "task_updates",
                "update_date",
                "DATE"
            )

            add_column_if_missing(
                cursor,
                "task_updates",
                "description",
                "TEXT"
            )

            add_column_if_missing(
                cursor,
                "task_updates",
                "created_at",
                "TEXT"
            )


        # ========================================================
        # INDEXES
        # ========================================================

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_records_status
            ON records(status)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_records_assigned_to
            ON records(assigned_to)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_updates_record
            ON task_updates(record_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_updates_updated_by
            ON task_updates(updated_by)
        """)


        # ========================================================
        # DEFAULT ADMIN
        # ========================================================

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        if cursor.fetchone()[0] == 0:

            salt = bcrypt.gensalt()

            hashed_password = bcrypt.hashpw(
                "admin123".encode("utf-8"),
                salt
            ).decode("utf-8")

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?)
                """,
                (
                    "admin",
                    hashed_password,
                    "Admin"
                )
            )


        # ========================================================
        # COMMIT
        # ========================================================

        conn.commit()


    except Exception:

        conn.rollback()

        raise


    finally:

        conn.close()


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    init_db()

    print(
        "Database initialized successfully."
    )
