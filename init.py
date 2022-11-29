from dotenv import load_dotenv
import os


load_dotenv()
def get_env_var(key: str) -> str:
    data: str = os.environ.get(key)
    if not data:
        raise KeyError("[ERROR]Key {} not found".format(
            key
            ))

    return data