import urllib.request
from dataflows import PackageWrapper, ResourceWrapper, Flow, dump_to_path, printer


def get_data():
    header = True
    resource = urllib.request.urlopen(
        "ftp://aftp.cmdl.noaa.gov/data/trace_gases/co2/in-situ/surface/mlo/co2_mlo_surface-insitu_1_ccgg_DailyData.txt")
    for row in resource.readlines():
        usable_row = row.decode('utf-8').replace('\n', '')
        if not usable_row.startswith('#'):
            parts = usable_row.split(' ')
            if header:
                header = False
            else:
                date = parts[1] + '-' + f"{int(parts[2]):02d}" + '-' + f"{int(parts[3]):02d}"
                value = '' if '-999.99' in parts[7] else parts[7]
                yield dict(
                    date=date,
                    value=value
                )

    header = True
    resource = urllib.request.urlopen('https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2_mlo_weekly.csv')
    for row in resource.readlines():
        usable_row = row.decode('utf-8').replace('\n', '')
        parts = usable_row.split(',')
        if header:
            header = False
        else:
            date = parts[0]
            value = parts[1]
            if "2017-" not in date:
                yield dict(
                    date=date,
                    value=value
                )


def change_path(package: PackageWrapper):
    # Add 'name' in descriptor:
    package.pkg.descriptor['name'] = 'co2-ppm-daily'
    # Change path and name for the resource:
    package.pkg.descriptor['resources'][0]['path'] = 'data/co2-ppm-daily.csv'
    package.pkg.descriptor['resources'][0]['name'] = 'co2-ppm-daily'

    package.pkg.descriptor['views'] = []
    view = {
        "name": "graph",
        "title": "Trends in Atmospheric Carbon Dioxide",
        "resources": ["co2-ppm-daily"],
        "specType": "simple",
        "spec": {
            "type": "lines-and-points",
            "group": "Date",
            "series": [
                "Interpolated",
                "Trend"
            ]
        }
    }
    package.pkg.descriptor['views'].append(view)

    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    yield first.it
    yield from package


Flow(get_data(),
     change_path,
     dump_to_path(),
     printer()).process()
