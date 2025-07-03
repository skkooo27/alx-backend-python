# 4-stream_ages.py
import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row[0]  # Yield the age only

    cursor.close()
    connection.close()


# Use the generator to calculate average
if __name__ == "__main__":
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count else 0
    print(f"Average age of users: {average_age}")
