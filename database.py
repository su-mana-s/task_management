import psycopg
import bcrypt


# ============================================================
# POSTGRESQL CONFIGURATION
# ============================================================

DB_HOST = "10.84.109.145"
DB_PORT = 5432
DB_NAME = "taskm"
DB_USER = "taskapp"
DB_PASSWORD = "taskapp"

DB_NAME_DISPLAY = DB_NAME


# ============================================================
# CONNECTION
# ============================================================

def get_connection():

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ============================================================
# DATABASE RESET
#
# TESTING VERSION
#
# WARNING:
# This deletes all application data.
# Remove/comment reset_database(cursor) before production use.
# ============================================================

def reset_database(cursor):

    cursor.execute("""
        DROP TABLE IF EXISTS
            payment_receipt_sequences,
            bill_sequences,
            activity_log,
            payment_transactions,
            task_updates,
            documents,
            tasks,
            clients,
            bank_details,
            users
        CASCADE
    """)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ====================================================
        # RESET
        # ====================================================

        reset_database(cursor)


        # ====================================================
        # USERS
        # ====================================================

        cursor.execute("""
            CREATE TABLE users (

                id SERIAL PRIMARY KEY,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL,

                role TEXT NOT NULL
                    CHECK (
                        role IN (
                            'Admin',
                            'Employee',
                            'Accounts'
                        )
                    ),

                is_active BOOLEAN NOT NULL
                    DEFAULT TRUE,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)


        # ====================================================
        # BANK DETAILS
        # ====================================================

        cursor.execute("""
            CREATE TABLE bank_details (

                id SERIAL PRIMARY KEY,

                display_name TEXT UNIQUE NOT NULL,

                bank_name TEXT NOT NULL,

                ifsc TEXT NOT NULL,

                branch TEXT NOT NULL,

                account_number TEXT NOT NULL,

                account_holder_name TEXT NOT NULL,

                upi_id TEXT NOT NULL,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)


        # ====================================================
        # CLIENTS
        # ====================================================

        cursor.execute("""
            CREATE TABLE clients (

                id SERIAL PRIMARY KEY,

                name TEXT NOT NULL,

                mobile TEXT NOT NULL UNIQUE,

                email TEXT,

                address TEXT,

                pan TEXT,

                tan TEXT,

                gst TEXT,

                file_no TEXT,

                aadhar TEXT,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)


        # ====================================================
        # TASKS
        # ====================================================

        cursor.execute("""
            CREATE TABLE tasks (

                id SERIAL PRIMARY KEY,

                task_name TEXT NOT NULL,

                task_details TEXT,

                client_id INTEGER NOT NULL,

                department TEXT NOT NULL,

                miscellaneous_details TEXT,

                assigned_to INTEGER,

                created_by INTEGER NOT NULL,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                status INTEGER NOT NULL
                    DEFAULT 0,

                date_of_completion DATE,

                completed_by INTEGER,

                details_of_work_done TEXT,

                date_of_despatch DATE,

                dispatch_at TIMESTAMPTZ,

                dispatched_by INTEGER,

                how_despatched TEXT,



                bill_raised BOOLEAN NOT NULL
                    DEFAULT FALSE,

                bill_type TEXT,

                billed_under TEXT
                    CHECK (
                        billed_under IN ('S', 'V')
                    ),

                bill_number TEXT UNIQUE,

                bill_date DATE,

                bill_amount NUMERIC(15, 2)
                    NOT NULL DEFAULT 0
                    CHECK (bill_amount >= 0),

                actual_amount_received NUMERIC(15, 2)
                    NOT NULL DEFAULT 0
                    CHECK (actual_amount_received >= 0),

                amount_pending_receipt NUMERIC(15, 2)
                    NOT NULL DEFAULT 0
                    CHECK (amount_pending_receipt >= 0),

                billing_fin_year TEXT,

                billing_quarters TEXT[],

                billing_form_types TEXT[],

                billing_months TEXT[],

                loading_charges NUMERIC(15, 2)
                    NOT NULL DEFAULT 0
                    CHECK (loading_charges >= 0),

                gst_registration_fee NUMERIC(15, 2)
                    NOT NULL DEFAULT 0
                    CHECK (gst_registration_fee >= 0),

                application_type TEXT,

                billing_remarks TEXT,

                bill_raised_by INTEGER,

                bill_raised_at TIMESTAMPTZ,


                FOREIGN KEY (client_id)
                    REFERENCES clients(id),

                FOREIGN KEY (assigned_to)
                    REFERENCES users(id),

                FOREIGN KEY (created_by)
                    REFERENCES users(id),

                FOREIGN KEY (completed_by)
                    REFERENCES users(id),

                FOREIGN KEY (dispatched_by)
                    REFERENCES users(id),

                FOREIGN KEY (bill_raised_by)
                    REFERENCES users(id)
            )
        """)


        # ====================================================
        # DOCUMENTS
        # ====================================================

        cursor.execute("""
            CREATE TABLE documents (

                id SERIAL PRIMARY KEY,

                task_id INTEGER NOT NULL,

                nature_of_papers TEXT NOT NULL,

                document_details TEXT,

                how_received TEXT NOT NULL,

                received_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                received_by INTEGER NOT NULL,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (received_by)
                    REFERENCES users(id)
            )
        """)


        # ====================================================
        # TASK UPDATES
        # ====================================================

        cursor.execute("""
            CREATE TABLE task_updates (

                id SERIAL PRIMARY KEY,

                task_id INTEGER NOT NULL,

                updated_by INTEGER NOT NULL,

                update_date TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                description TEXT NOT NULL,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (updated_by)
                    REFERENCES users(id)
            )
        """)


        # ====================================================
        # PAYMENT TRANSACTIONS
        # ====================================================

        cursor.execute("""
            CREATE TABLE payment_transactions (

                id SERIAL PRIMARY KEY,

                task_id INTEGER NOT NULL,

                amount NUMERIC(15, 2) NOT NULL
                    CHECK (amount > 0),

                payment_mode TEXT NOT NULL,

                payment_date DATE NOT NULL,

                received_by INTEGER NOT NULL,

                notes TEXT,

                receipt_type TEXT,

                receipt_number TEXT,

                receipt_date DATE,

                upi_bank TEXT,

                bank_name TEXT,

                bank_transfer_mode TEXT,

                cheque_number TEXT,

                cheque_date DATE,

                created_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (received_by)
                    REFERENCES users(id)
            )
        """)


        # ====================================================
        # BILL SEQUENCES
        # ====================================================

        cursor.execute("""
            CREATE TABLE bill_sequences (

                department TEXT NOT NULL,

                billed_under TEXT NOT NULL
                    CHECK (
                        billed_under IN ('S', 'V')
                    ),

                last_number INTEGER NOT NULL DEFAULT 0,

                PRIMARY KEY (
                    department,
                    billed_under
                )
            )
        """)


        # ====================================================
        # PAYMENT RECEIPT SEQUENCES
        # ====================================================

        cursor.execute("""
            CREATE TABLE payment_receipt_sequences (

                department TEXT NOT NULL,

                billed_under TEXT NOT NULL
                    CHECK (
                        billed_under IN ('S', 'V')
                    ),

                last_number INTEGER NOT NULL DEFAULT 0,

                PRIMARY KEY (
                    department,
                    billed_under
                )
            )
        """)


        # ====================================================
        # ACTIVITY LOG
        # ====================================================

        cursor.execute("""
            CREATE TABLE activity_log (

                id SERIAL PRIMARY KEY,

                task_id INTEGER NOT NULL,

                action_type TEXT NOT NULL,

                performed_by INTEGER NOT NULL,

                action_date TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                amount NUMERIC(15, 2),

                payment_mode TEXT,

                description TEXT,

                FOREIGN KEY (task_id)
                    REFERENCES tasks(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (performed_by)
                    REFERENCES users(id)
            )
        """)


        # ====================================================
        # INDEXES
        # ====================================================

        cursor.execute("""
            CREATE INDEX idx_tasks_client
            ON tasks(client_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_tasks_status
            ON tasks(status)
        """)

        cursor.execute("""
            CREATE INDEX idx_tasks_assigned_to
            ON tasks(assigned_to)
        """)

        cursor.execute("""
            CREATE INDEX idx_tasks_created_by
            ON tasks(created_by)
        """)

        cursor.execute("""
            CREATE INDEX idx_tasks_department
            ON tasks(department)
        """)

        cursor.execute("""
            CREATE INDEX idx_tasks_created_at
            ON tasks(created_at DESC)
        """)

        cursor.execute("""
            CREATE INDEX idx_documents_task
            ON documents(task_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_documents_received_by
            ON documents(received_by)
        """)

        cursor.execute("""
            CREATE INDEX idx_documents_received_at
            ON documents(received_at DESC)
        """)

        cursor.execute("""
            CREATE INDEX idx_task_updates_task
            ON task_updates(task_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_task_updates_updated_by
            ON task_updates(updated_by)
        """)

        cursor.execute("""
            CREATE INDEX idx_task_updates_date
            ON task_updates(update_date DESC)
        """)

        cursor.execute("""
            CREATE INDEX idx_payment_transactions_task
            ON payment_transactions(task_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_activity_log_task
            ON activity_log(task_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_activity_log_date
            ON activity_log(action_date DESC)
        """)


        # ====================================================
        # DEFAULT ADMIN
        # ====================================================

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
                role,
                is_active
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                "admin",
                hashed_password,
                "Admin",
                True
            )
        )


        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()

        print(
            "PostgreSQL database initialized successfully."
        )

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    init_db()