import datetime
import time
import pandas as pd
import pymysql.cursors

# Database connection parameters
db_params = {
    'host': '13.234.176.50',
    'user': 'rbdbusr',
    'password': 'Agl360UdmnB34Tz',
    'port': 2499,
    'db': 'ebux_tata',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Initialize a dictionary to store the cached results for each table
cached_results = {}

# Function to fetch data from the database
def data_fetch():
    start_time = time.time()  # Record the start time

    # List of tables to fetch data from
    tables = [
        'flipkart_crawl_pdp',
        'amazon_crawl_pdp',
        'flipkart_supermart_crawl_pdp',
        'bigbasket_crawl_pdp',
        'grofers_crawl_pdp',
        'amazon_fresh_crawl_pdp',
        'swiggy_instamart_crawl_pdp',
        'zepto_crawl_pdp'
    ]

    # Initialize an empty DataFrame to store the results
    df_list = []

    try:
        with pymysql.connect(**db_params) as connection:
            # Loop through each table
            for table in tables:
                # Get the cached result for the current table
                cached_result = cached_results.get(table)

                # If cached result is not available or if it's been more than 1 hour since last fetch
                if cached_result is None or time.time() - cached_result['timestamp'] > 3600:
                    # Execute the SQL query
                    sql = f"""
                        SELECT CAST(pf_id AS CHAR) AS pf_id, COUNT(*) AS count
                        FROM {table}
                        WHERE DATE(created_on) = DATE(NOW())
                        GROUP BY pf_id;
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(sql)

                        # Fetch the results and append to the DataFrame list
                        df_list.append(pd.DataFrame(cursor.fetchall()))

                    # Update the cached result for the current table
                    cached_results[table] = {
                        'data': df_list[-1],  # Store the fetched DataFrame
                        'timestamp': time.time()  # Update the timestamp
                    }
                    print(f"Data fetched from table '{table}' at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print(f"No changes in table '{table}' since last fetch, skipping...")
                    # Append the cached DataFrame to the list
                    df_list.append(cached_result['data'])
    except Exception as e:
        print("Error:", e)

    end_time = time.time()  # Record the end time
    duration = (end_time - start_time)/60  # Calculate the duration
    print(f"Data fetching took {duration:.2f} min")

    # Concatenate the DataFrames into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)

    # Return the DataFrame
    return df

# Function to create a DataFrame with static values
def static_values():
    static_data = {'pf_id': ['1', '2', '3', '4', '6','7','17','29'],
                   'static_count': [1184, 5957, 5040, 25009, 8526, 5984, 34037, 22000]}
    return pd.DataFrame(static_data)

if __name__ == '__main__':
    print('Data Fetching started')
    data = data_fetch()
    print("Fetched Data:")
    print(data)
    print(f'Data fetch completed')
