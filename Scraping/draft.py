import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", type=str, default="./configs/deep_sort.yaml")
    # parser.add_argument("--path", type=str)
    parser.add_argument('--codes', nargs='+', type=int, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args.data_path)
    # for i in args.codes:
    #     print(i)