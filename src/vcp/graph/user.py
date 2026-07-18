def user_topic():
    while True:
        topic = input("Enter Video Topic: ")
        if topic.strip() != "":
            return topic
        print("Topic cannot be empty. Please enter a valid topic.")
