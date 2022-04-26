import argparse

# Define the arguments dictionary
arguments = {
    "interface": "Interface to display",
    "family": "Family to display (inet, inet6)"
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in arguments:
        # Add all arguments to parser
        parser.add_argument('-' + key, required=True, help=arguments[key])
    args = parser.parse_args()
    print(args)
