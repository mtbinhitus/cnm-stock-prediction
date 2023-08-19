from dotenv import load_dotenv
import os
from pathlib import Path
import time

# function that returns the value of the environment variable
# input - key_name: the name of the enviroment variable that you want to get.
# output - the value of the environment. if the value is not available the fn will return "None"
def get_env_variable(key_name):
    dotenv_path = Path('../.env')
    print(dotenv_path)
    is_done= load_dotenv(dotenv_path=dotenv_path)
    if(is_done is True):
        print("Environment Variables file .env loaded Successfully!")
    else:
        print("Environment Variables file .env loaded Failed! Check your .env file path.")
        print("The environment variables defined in the host environment will be used instead.")
        # if load_dotenv fail the environment variables defined in the host environment will be used instead.
    return os.getenv(key_name)

# t: seconds
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('Fire in the hole!!')


def df_to_csv(df, filename='btc_bars'):
    # export DataFrame to csv
    res = df.to_csv(f'{filename}.csv')
    print("df_to_csv")
    print(res)
    return res