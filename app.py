import helpers.ffmpeg as f
import json


def grab_user_input():
    """
    Get the user input
    """

    def filter_input(message, default):
        user_input = input(message)

        if user_input == "":
            user_input = default
        return user_input

    print("Hit enter for default value\n")
    return filter_input("Enter the config filepath: ", "./config.json")


def read_config(file_path='./config.json'):
    """
    Read the config file
    Args:
        file_path:  The filepath for the config to use
    Returns: The retrieved config
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    filepath = grab_user_input()
    config = read_config(filepath)
    f.generate_streams(config)
