# 1-batch_processing.py
import seed

def stream_users_in_batches(batch_size):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)  # gets `batch_size` rows
        if not rows:
            break
        yield rows  # yield the whole batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # loop over batches
        for user in batch:  # loop over users in each batch
            if user['age'] > 25:
                print(user)
