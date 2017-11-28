import argparse
import requests
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-host",
        "--host",
        help="flume hostname or IP (default: \"127.0.0.1\")",
        type=str,
        default='127.0.0.1')
    parser.add_argument(
        "-port", "--port", help="flume metrics port", type=str, required=True)
    parser.add_argument(
        "-config",
        "--config",
        help="config file with monitoring parameters",
        type=str,
        required=True)
    parser.add_argument(
        "-measurement",
        "--measurement",
        help="measurement name",
        type=str,
        required=True)
    return parser.parse_args()


def parse_metric_response(measurement, resp, conf_data):
    for s in ['SOURCE', 'CHANNEL', 'SINK']:
        if conf_data.get(s):
            process_group(measurement, resp, s, conf_data.get(s))


def process_group(measurement, resp, group_type, group_metrics):
    # get fields to process from config
    fields = group_metrics.get('FIELDS')
    if fields is None:
        return
    fields = [f.strip() for f in fields.split(',')]
    group_keys = [k for k in resp.keys() if k.startswith('%s.' % group_type)]
    for gk in group_keys:
        group_name = gk.split('%s.' % group_type)[1]
        group_data = resp.get(gk)
        tag_set = []
        tag_set.append('='.join(['type', str(group_type)]))
        tag_set.append('='.join(['name', str(group_name)]))

        field_set = []
        for f in fields:
            field_set.append('='.join([f, group_data.get(f)]))
        # print one line per group (source, channel, sink)
        s = '{measurement},{tag_set} {field_set}'.format(
            measurement=measurement,
            tag_set=','.join(tag_set),
            field_set=','.join(field_set))

        print(s)


if __name__ == '__main__':
    args = parse_args()
    conf_data = yaml.safe_load(open(args.config))
    metrics_url = 'http://%s:%s/metrics' % (args.host, args.port)
    resp = requests.get(metrics_url)
    measurement = args.measurement
    parse_metric_response(measurement, resp.json(), conf_data)
