import argparse

from firebase.connector import FireBaseConnector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse private key json file.')
    parser.add_argument('credential', type=str,
                        help='The path to the private key json file for Firebase')
    parser.add_argument('--databaseURL', type=str, nargs='?',
                        const=sum, default="https://ledypie.firebaseio.com/",
                        help='The Firebase database url')

    args = parser.parse_args()
    print(args)
    fbc = FireBaseConnector(credential_path=args.credential, database_url=args.databaseURL)
