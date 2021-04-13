# pyCheckMyInternet
# © 2021 Reischl Franz
# Regularly checks internet connectivity

from time import sleep

from nslookup import Nslookup
from datetime import datetime, timedelta
import os

if __name__ == '__main__':
    DOMAIN_TO_CHECK = 'orf.at'
    DNS_LIWEST = '192.168.0.1'  # Router gateway, has ISP DNS entries
    DNS_GOOGLE = '8.8.8.8'
    LOG_FILE = 'internet.log'

    dns_query_liwest = Nslookup(dns_servers=[DNS_LIWEST])
    dns_query_google = Nslookup(dns_servers=[DNS_GOOGLE])

    if not os.path.exists(LOG_FILE):
        # Create log file
        file = open(LOG_FILE, 'w')
        file.write('status\tfrom\tduration\n')
        file.close()

    print('status\tfrom\tduration')
    last_change = datetime.now()
    last_status = 'none'

    while True:
        ips_record = dns_query_liwest.dns_lookup(DOMAIN_TO_CHECK)
        internet_connection = len(ips_record.answer) > 0

        file = open(LOG_FILE, 'a')

        if internet_connection:
            # Normal internet is OK - status='good'
            last_time_internet_good = datetime.now()
            print('Internet connection is good :)')

            if last_status != 'good':
                # Now good again
                print(f'good\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min')
                file.write(f'good\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min\n')

                last_change = datetime.now()
                last_status = 'good'
        else:
            # Liwest connection failed, test Google DNS
            ips_record = dns_query_google.dns_lookup(DOMAIN_TO_CHECK)
            internet_connection = len(ips_record.answer) > 0

            if internet_connection:
                # Bad DNS - status='dns'
                if last_status != 'dns':
                    # Now dns is bad :(
                    print(f'dns\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min')
                    file.write(f'dns\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min\n')

                    last_change = datetime.now()
                    last_status = 'dns'
            else:
                # No internet - status='dead'
                if last_status != 'dead':
                    # Now internet is dead :(
                    print(f'dead\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min')
                    file.write(f'dead\t{last_status}\t{(datetime.now() - last_change).total_seconds() / 60}min\n')

                    last_change = datetime.now()
                    last_status = 'dead'
        file.close()
        sleep(5*60)  # check all 5 mins
