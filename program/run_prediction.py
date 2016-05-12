import sys
import transform_data
import markov_hill_climbing_model as markov


def main(argv=None):
    if argv is not None:
        dom, path = transform_data.parse_url(argv)
        if dom[:-1] == "/":
            dom = dom[:-1]
        if path[:-1] == "/":
            path = path[:-1]
        if path[1:] == "/":
            path = path[1:]
        url = dom + "/" + path

        mark = markov.load_model()
        pred = mark.get_prediction(dom, url)
        f = open('../actual_run_data/prediction.txt', 'wb')
        f.write(pred)
        f.close()


if __name__ == "__main__":
    main(sys.argv)
