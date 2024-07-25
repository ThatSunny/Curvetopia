import read_csv
import visualization
import matplotlib.colors as color

def main():
    csv_file_path = "./problems/problems/frag0.csv"
    paths_xys = read_csv.read_csv(csv_file_path)

    colors = [color.to_rgba(c) for c in ['red', 'green', 'blue']]
    visualization.plot(paths_xys, colors=colors)


if __name__ == "__main__":
    main()