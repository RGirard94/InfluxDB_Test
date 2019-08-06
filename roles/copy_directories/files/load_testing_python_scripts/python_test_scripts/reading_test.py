import datetime
import configparser
from influxdb import InfluxDBClient
import logging


logging.basicConfig(
    filename='/opt/docker-data/tests/personal_logs/reading_logs.log',
    filemode='a',
    format='%(message)s',
    level=logging.INFO
)


def get_rrinterval_for_sing_patient_during_last_6_months(client):
    r = client.query("SELECT * FROM RrInterval WHERE \"user\" = 'vse7ha1n-7njp-mppv-db8w-qcwdbma0hnma' and time > now() - 24w")
    return list(r.get_points(measurement='RrInterval'))[0]


def get_rrinterval_mean_for_each_15min_interval_for_sing_patient(client):
    r = client.query("SELECT mean(RrInterval) FROM RrInterval WHERE \"user\" = 'vse7ha1n-7njp-mppv-db8w-qcwdbma0hnma' GROUP BY time(15m)")
    return list(r.get_points(measurement='RrInterval'))[0]


def get_number_rrinterval_for_each_1min_interval_for_sing_patient(client):
    r = client.query("SELECT count(RrInterval) FROM RrInterval WHERE \"user\" = 'vse7ha1n-7njp-mppv-db8w-qcwdbma0hnma' GROUP BY time(1m)")
    return list(r.get_points(measurement='RrInterval'))[0]


def get_total_rrinterval_by_user(client):
    r = client.query("SELECT sum(rr_interval_count_by_min) from RrInterval group by \"user\"")
    return list(r.get_points(measurement='RrInterval'))[0]


def get_motionacc_for_sing_patient_during_last_day(client):
    r = client.query("SELECT x_acm, y_acm, z_acm FROM MotionAccelerometer WHERE \"user\" = 'vse7ha1n-7njp-mppv-db8w-qcwdbma0hnma' and time > now() - 24w")
    return list(r.get_points(measurement='MotionAccelerometer'))[0]


def get_motiongyr_for_sing_patient_during_last_day(client):
    r = client.query("SELECT x_gyro, y_gyro, z_gyro FROM MotionGyroscope WHERE \"user\" = 'vse7ha1n-7njp-mppv-db8w-qcwdbma0hnma' and time > now() - 24w")
    return list(r.get_points(measurement='MotionGyroscope'))[0]


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('/opt/docker-data/tests/load_testing_python_scripts/output_requests/config.conf')

    influxdb_client_constants = config["Influxdb Client"]

    DB_NAME = influxdb_client_constants["database_name"]
    HOST = influxdb_client_constants["host"]
    PORT = int(influxdb_client_constants["port"])
    USER = influxdb_client_constants["user"]
    PASSWORD = influxdb_client_constants["password"]

    CLIENT = InfluxDBClient(host=HOST, port=PORT, username=USER, password=PASSWORD,
                            database=DB_NAME)

    t1 = datetime.datetime.now()

    logging.info('RrInterval during last 6 months reading begins at : {}'.format(t1))

    get_rrinterval_for_sing_patient_during_last_6_months(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('RrInterval during last 6 months duration : {}'.format(t2-t1))

    t1 = datetime.datetime.now()

    logging.info('rrinterval mean 15 min interval reading begins at : {}'.format(t1))

    get_rrinterval_mean_for_each_15min_interval_for_sing_patient(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('rrinterval mean 15 min interval reading duration : {}'.format(t2-t1))

    t1 = datetime.datetime.now()

    logging.info('rrinterval number 1 min interval reading begins at : {}'.format(t1))

    get_number_rrinterval_for_each_1min_interval_for_sing_patient(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('rrinterval number 1 min interval reading duration : {}'.format(t2-t1))

    t1 = datetime.datetime.now()

    logging.info('total rrinterval by user reading begins at : {}'.format(t1))

    get_total_rrinterval_by_user(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('total rrinterval by user reading duration : {}'.format(t2 - t1))

    t1 = datetime.datetime.now()

    logging.info('motion acc during last day reading begins at : {}'.format(t1))

    get_motionacc_for_sing_patient_during_last_day(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('motion acc during last day reading duration : {}'.format(t2 - t1))

    t1 = datetime.datetime.now()

    logging.info('motion gyr during last day reading begins at : {}'.format(t1))

    get_motiongyr_for_sing_patient_during_last_day(CLIENT)

    t2 = datetime.datetime.now()

    logging.info('motion gyr during last day reading duration : {}'.format(t2 - t1))

    logging.info('--------------------------------------------')
