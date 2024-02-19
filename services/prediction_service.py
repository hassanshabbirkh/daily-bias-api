from database.db_connection import DatabaseConnection
import sqlite3

def format_data_for_telegram_message(rows):
    # Group by market
    market_data = {}
    for row in rows:
        market, date, symbol, prediction, confidence = row
        if market not in market_data:
            market_data[market] = []
        market_data[market].append((symbol, prediction, confidence))

    # Build the result string
    result_str = ""
    for market, predictions in market_data.items():
        result_str += f"[{market}] - {date}\n"
        for symbol, prediction, confidence in predictions:
            result_str += f"{symbol} : {prediction} ({confidence})\n"
        result_str += "\n"  # Add a newline to separate each market group
    return result_str

def format_data_in_json(rows):
    results = []

    for row in rows:
        # Creating a dictionary for each row
        result = {
            "date": row[1],
            "symbol": row[2],
            "market": row[0],#row[2],
            "prediction": row[3],
            "confidence": row[4]
        }
        results.append(result)
    return results


def get_predictions_by_date(date, result_format="text"):
    try:
        conn = DatabaseConnection().get_connection()
        cur = conn.cursor()
        cur.execute("SELECT dp.market, dp.date, dp.symbol, dp.prediction, dp.confidence \
                             FROM daily_predictions dp \
                             WHERE date=?", (date,))

        rows = cur.fetchall()
        print(rows)

        results = []

        if result_format == "json":
            return format_data_in_json(rows)
        if result_format == "text":
            return format_data_for_telegram_message(rows)



        return results


    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {}

def get_latest_predictions(result_format="text"):
    try:
        conn = DatabaseConnection().get_connection()
        cur = conn.cursor()
        # Query to select all rows from the latest date available in the table
        cur.execute("""
            SELECT dp.market, dp.date, dp.symbol, dp.prediction, dp.confidence
            FROM daily_predictions dp
            WHERE dp.date = (SELECT MAX(date) FROM daily_predictions)
        """)

        rows = cur.fetchall()
        print(rows)

        if not rows:
            return "No data available for the most recent date."

        if result_format == "json":
            return format_data_in_json(rows)
        elif result_format == "text":
            return format_data_for_telegram_message(rows)
        else:
            return rows

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {}


def get_predictions_by_symbol_and_date(symbols, start_date, end_date):
    try:
        placeholders = ', '.join('?' for _ in symbols)  # Create placeholders for symbols
        conn = DatabaseConnection().get_connection()
        cur = conn.cursor()
        query = f"""SELECT dp.market, dp.date, dp.symbol, dp.prediction, dp.confidence
                            FROM daily_predictions dp
                            WHERE dp.symbol IN ({placeholders}) AND dp.date BETWEEN ? AND ?"""
        cur.execute(query, symbols + [start_date, end_date])

        rows = cur.fetchall()

        return format_data_in_json(rows)
        return []  # or any default case you'd like to handle

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {}