# For debugging
def show_result(f, *args):
    def showing_f(*args):
        result = f(*args)
        print(result, args)
        return result
    return showing_f
