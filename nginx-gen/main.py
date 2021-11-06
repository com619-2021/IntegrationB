import crossplane
import yaml
import json
import argparse

denylist: [str] = []


def services(compose_path: str):
    """
    Generator that contains each service in compose file, other than those in the denylist
    :param compose_path: path to compose file
    :return: service name and json object
    """
    with open(compose_path, 'r') as f:
        compose = yaml.load(f, Loader=yaml.CLoader)
        allowed_items = {k: v for k, v in compose["services"].items() if k not in denylist}
        for service_name, service in allowed_items.items():
            yield service_name, service


def gen_location(service_name: str, service: dict, line_num: int):
    """
    Create a location directive from the service info and the sample
    :param service_name: name of the service (i.e. port)
    :param service: service json
    :param line_num: line num to start generation
    :return: finished location directive
    """
    with open("./sample_directive.json", 'r') as f:
        sample = json.load(f)
        try:
            sample["line"] = line_num
            sample["args"] = ["/" + service_name]
            port: str = service["expose"][0]
            sample["block"][0]["line"] = line_num + 1
            sample["block"][0]["args"] = ["http://" + service_name + ":" + port + "/"]
            return sample
        except KeyError:
            raise Exception("Expected value was missing from " + service_name + " service")

def nginx_gen(compose_path: str, nginx_in: str, nginx_out: str):
    """
    Main generation function.
    :param compose_path: Path to compose file
    :param nginx_in: Path to nginx file to edit
    :param nginx_out: Output path for new nginx file
    :return:
    """
    parsed: dict = crossplane.parse(nginx_in)
    directives = parsed["config"][0]["parsed"]
    server: [dict] = []
    for directive in directives:
        if directive["directive"] == "http":
            server = directive["block"][0]["block"]
    if server[-1]["directive"] == "location":
        line_num = int(server[-1]["line"]) + 2
    else:
        line_num = int(server[-1]["line"]) + 1
    for service_name, service in services(compose_path):
        location = gen_location(service_name, service, line_num)
        line_num += 3
        server.append(location)
    with open(nginx_out, 'w') as f:
        f.write(crossplane.build(directives))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Generate nginx config for hosting docker containers")
    parser.add_argument('-c', '--compose', help='Path to compose file', required=True)
    parser.add_argument('-n', '--nginx', help='Path to nginx file', required=True)
    parser.add_argument('-o', '--out', help='Path to output', required=True)
    parser.add_argument('-d', '--deny', nargs='*', help="List of services to not include")
    args = vars(parser.parse_args())
    if args["deny"] is not None:
        denylist = args["deny"]
    nginx_gen(args["compose"], args["nginx"], args["out"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
