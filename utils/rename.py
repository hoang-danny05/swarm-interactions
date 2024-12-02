
#renames the meta information of functions
# changes the meta information that chatgpt sees programmaticly
def rename(newname: str):
    def decorator(f):
        f.__name__ = newname.replace(" ", "_")
        return f
    return decorator

