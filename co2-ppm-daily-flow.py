import urllib.request
from dataflows import PackageWrapper, ResourceWrapper, Flow, dump_to_path, printer


def get_data():
    # first source containing info from 01.01.1973 - 31.12.2017
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
                value = None if '-999.99' in parts[7] else parts[7]
                if value is not None:
                    yield dict(
                        date=date,
                        value=value
                    )

    # second source containing info until today
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
            if ("2017-" not in date) and (value is not ''):
                yield dict(
                    date=date,
                    value=value
                )


def change_path(package: PackageWrapper):

    package.pkg.descriptor['title'] = 'CO2 PPM - Trends in Atmospheric Carbon Dioxide'
    package.pkg.descriptor['name'] = 'co2-ppm-daily'

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
            "group": "date",
            "series": [
                "value"
            ]
        }
    }
    package.pkg.descriptor['views'].append(view)

    yield package.pkg
    res_iter = iter(package)
    first: ResourceWrapper = next(res_iter)
    yield first.it
    yield from package


co2_ppm_daily = Flow(get_data(), change_path, dump_to_path())


if __name__ == '__main__':
    co2_ppm_daily.process()
