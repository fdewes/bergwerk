from tools import tools
import mariadb
import datetime
import requests

if __name__ == '__main__': 
    print("Running conversation cleanup cron!")

    config = tools.Config()
    dbs = tools.DatabaseSession()

    keep_conversation_days = int(config.get_value("keep_conversation_days"))
    print(f"Keep days: {keep_conversation_days}")

    # Delete old conversations from the MYSQL database

    cur, conn = dbs.get_cursor_conn()
    if conn:
        print("Database connection successful.")
    else:
        print("Failed to establish database connection.")

    cutoff_ts = int((datetime.datetime.now() - datetime.timedelta(days=keep_conversation_days)).timestamp())

    delete_query = """
    DELETE FROM tracker_db.tracker
    WHERE ts < ?;
    """

    try:
        preview_query = """
        SELECT * FROM tracker_db.tracker
        WHERE ts < ?;
        """
        cur.execute(preview_query, (cutoff_ts,))
        rows_to_delete = cur.fetchall()
        print(f"Rows to be deleted: {len(rows_to_delete)}.")

        cur.execute(delete_query, (cutoff_ts,))
        conn.commit()
        cutoff_date = datetime.datetime.fromtimestamp(cutoff_ts).strftime('%Y-%m-%d')
        print(f"Deleted conversations older than {keep_conversation_days} days (cutoff date: {cutoff_date}).")
    except mariadb.Error as err:
        print(f"Error deleting old data from the table: {err}")
    finally:
        cur.close()
        conn.close()

    # Delete old conversations from the Mediawiki pages in [[Category:Tracker]]

    session = tools.session

    api_url = "http://wiki/w/api.php"

    # Parameters to fetch pages in the [[Category:Tracker]]
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:Tracker",
        "cmprop": "title|timestamp",
        "cmlimit": "max",
        "format": "json"
    }

    try:
        with session.get(api_url, params=params) as response:
            response.raise_for_status()
            data = response.json()

            if "query" in data and "categorymembers" in data["query"]:
                print("Pages in [[Category:Tracker]] older than the cutoff date:")
                for page in data["query"]["categorymembers"]:
                    page_ts = datetime.datetime.fromisoformat(page["timestamp"].replace("Z", "+00:00"))
                    try:
                        page_ts = datetime.datetime.fromisoformat(page["timestamp"].replace("Z", "+00:00"))
                        cutoff_dt = datetime.datetime.fromtimestamp(cutoff_ts, datetime.timezone.utc)
                        if page_ts < cutoff_dt:
                            print(f"DELETE: Title: {page['title']}, Timestamp: {page['timestamp']}")
                            delete_params = {
                                "action": "delete",
                                "title": page["title"],
                                "reason": f"Deleting old tracker page older than {keep_conversation_days} days",
                                "format": "json",
                                "token": tools.get_csrf_token(session) 
                            }

                            try:
                                delete_response = session.post(api_url, data=delete_params)
                                delete_response.raise_for_status()
                                delete_result = delete_response.json()
                                if "error" in delete_result:
                                    print(f"Error deleting page {page['title']}: {delete_result['error']}")
                                else:
                                    print(f"Successfully deleted page: {page['title']}")
                            except requests.RequestException as e:
                                print(f"Error deleting page {page['title']}: {e}")

                    except ValueError as e:
                        print(f"Error parsing timestamp for page {page['title']}: {e}")
            else:
                print("No pages found in [[Category:Tracker]].")
    except requests.RequestException as e:
        print(f"Error fetching data from MediaWiki API: {e}")

