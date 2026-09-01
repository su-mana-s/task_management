
import psycopg

from database import get_connection


# ============================================================
# CONSTANTS
# ============================================================
BUSINESS_DETAILS = (
            "<b>Sridharan & CO.</b><br/>"
            "<i>Chartered Accountants</i><br/>"
            "5/F1, VRS Complex,<br/>"
            "Pattamangala St. Mayiladuthurai<br/>"
            "Tamil Nadu - 609001<br/>"
        )


BILL_TYPES = [
    "Manual",
    "Tally",
    "Software"
]

BILLED_UNDER = [
    "Sridharan",
    "Vijayalakshmi"
]


# ============================================================
# PAYMENT MODES
# ============================================================

PAYMENT_MODES = [
    "Cash",
    "UPI",
    "Bank Transfer",
    "Cheque"
]


# ============================================================
# BANK DETAILS
# ============================================================

BANK_DETAILS = {}


# ============================================================
# DROPDOWN VALUES
# ============================================================

NARRATIVE_VALUES = []

FINANCIAL_YEARS = []

TDS_FORM_TYPES = []


# ============================================================
# OTHER STATIC VALUES
# ============================================================

BANK_TRANSFER_MODES = [
    "NEFT",
    "RTGS",
    "Cash Deposit"
]


MONTHS = [
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March"
]


QUARTERS = [
    "1",
    "2",
    "3",
    "4"
]


# ============================================================
# LOAD BANK DETAILS
# ============================================================

def load_bank_details():
    """
    Load all bank details from the database.

    Returns:
        dict:
            {
                "Display Name": {
                    "bank_name": ...,
                    "ifsc": ...,
                    "branch": ...,
                    "account_number": ...,
                    "account_holder_name": ...,
                    "upi_id": ...
                }
            }
    """

    bank_details = {}

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                display_name,
                bank_name,
                ifsc,
                branch,
                account_number,
                account_holder_name,
                upi_id
            FROM bank_details
            ORDER BY display_name
            """
        )

        rows = cursor.fetchall()

        for row in rows:

            (
                display_name,
                bank_name,
                ifsc,
                branch,
                account_number,
                account_holder_name,
                upi_id
            ) = row

            bank_details[display_name] = {

                "bank_name": bank_name,

                "ifsc": ifsc,

                "branch": branch,

                "account_number": account_number,

                "account_holder_name": account_holder_name,

                "upi_id": upi_id,

            }

    except psycopg.Error as e:

        print(
            f"Unable to load bank details: {e}"
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return bank_details


# ============================================================
# LOAD DROPDOWN VALUES
# ============================================================

def load_dropdown_values(category):
    """
    Load values for a particular dropdown category.

    Categories:
        narrative
        financial_year
        tds_form_type
    """

    values = []

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT value
            FROM app_dropdown_values
            WHERE category = %s
            ORDER BY sort_order, value
            """,
            (
                category,
            )
        )

        rows = cursor.fetchall()

        values = [
            row[0]
            for row in rows
        ]

    except psycopg.Error as e:

        print(
            f"Unable to load dropdown values "
            f"for '{category}': {e}"
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return values


# ============================================================
# LOAD ALL DROPDOWN VALUES
# ============================================================

def load_all_dropdown_values():

    return {

        "narrative":
            load_dropdown_values("narrative"),

        "financial_year":
            load_dropdown_values("financial_year"),

        "tds_form_type":
            load_dropdown_values("tds_form_type"),

    }


# ============================================================
# REFRESH BANK DETAILS
# ============================================================

def refresh_bank_details():
    """
    Reload the global BANK_DETAILS dictionary
    and rebuild UPI_BANKS.
    """

    global BANK_DETAILS
    global UPI_BANKS

    BANK_DETAILS = load_bank_details()
    UPI_BANKS = get_upi_banks()

    return BANK_DETAILS

# ============================================================
# REFRESH DROPDOWN VALUES
# ============================================================

def refresh_dropdown_values():
    """
    Reload all database-backed dropdown values.

    Updates:
        NARRATIVE_VALUES
        FINANCIAL_YEARS
        TDS_FORM_TYPES
    """

    global NARRATIVE_VALUES
    global FINANCIAL_YEARS
    global TDS_FORM_TYPES

    dropdown_values = load_all_dropdown_values()

    NARRATIVE_VALUES = dropdown_values["narrative"]

    FINANCIAL_YEARS = dropdown_values["financial_year"]

    TDS_FORM_TYPES = dropdown_values["tds_form_type"]

    return dropdown_values


# ============================================================
# UPI BANKS
# ============================================================

def get_upi_banks():
    """
    Return bank display names for UPI/bank selection.

    'None' is always the first option.
    """

    banks = ["None"]

    for display_name in BANK_DETAILS.keys():

        banks.append(display_name)

    return banks


# ============================================================
# INITIAL LOAD
# ============================================================

refresh_bank_details()

refresh_dropdown_values()

# UPI_BANKS = get_upi_banks()


# ============================================================
# DEBUG
# ============================================================

if __name__ == "__main__":

    print("UPI BANKS:")
    print(UPI_BANKS)

    print("\nNARRATIVE VALUES:")
    print(NARRATIVE_VALUES)

    print("\nFINANCIAL YEARS:")
    print(FINANCIAL_YEARS)

    print("\nTDS FORM TYPES:")
    print(TDS_FORM_TYPES)

