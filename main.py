import argparse
from comparison import Comparison

def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--right_answer',  type=str, required=True)
    parser.add_argument('--user_answer',   type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    r_a  = args.right_answer
    u_a  = args.user_answer
    c = Comparison(r_a, u_a)
    result = c.get_result()
    print(result)

if __name__ == '__main__':
    main()
