import ftplib
import time
import sys
import os
import re
import subprocess
import getopt
import datetime
import tarfile


def parsing_wpconfig(wp_location):
    try:
        config_path = os.path.normpath(wp_location+'/wp-config.php')
        with open(config_path, encoding="utf-8") as fh:
            content = fh.read()

        return parsing_wpconfig_content(content)

    except FileNotFoundError:
        print('Error: \n' + 'wp-config.php file not found: ,', config_path)
        sys.exit(1)

    except PermissionError:
        print('Missing read permission: ', config_path)
        sys.exit(1)

    except AttributeError:
        print('Error while parsing wp-config.php')
        sys.exit(1)


def parsing_wpconfig_content(wp_config_content):
    if not wp_config_content:
        return {}
    regex_db_name = r"(?<=DB_NAME', ')(.*?)(?='\);)"
    regex_db_user = r"(?<=DB_USER', ')(.*?)(?='\);)"
    regex_db_pass = r"(?<=DB_PASSWORD', ')(.*?)(?='\);)"
    regex_db_host = r"(?<=DB_HOST', ')(.*?)(?='\);)"
    databse = re.search(regex_db_name, wp_config_content).group(1)
    user = re.search(regex_db_user, wp_config_content).group(1)
    password = re.search(regex_db_pass, wp_config_content).group(1)
    host = re.search(regex_db_host, wp_config_content).group(1)
    return {'database': databse,
            'user': user,
            'password': password,
            'host': host
            }


def make_archive(wordpress_path, dumpfile_path, backup_directory):
    try:
        time_tag = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        dir_name = os.path.basename(wordpress_path.rstrip('/'))
        backup_directory_path = os.path.normpath(backup_directory)
        dir_path = os.path.join(backup_directory_path,dir_name)
        make_dir(dir_path)

        archive_name = os.path.join(
            dir_path, time_tag+'.tar.gz')

        with tarfile.open(archive_name, "w:gz") as tar:
            tar.add(wordpress_path)
            if dumpfile_path:
                tar.add(dumpfile_path, arcname="sql.dump")
        return archive_name

    except FileNotFoundError:
        print('Error - File Not Found: ,', archive_name)

    except PermissionError:
        print('Error: Missing write permission.')

    except:
        print('Error: Unknown error occurred while dumping file into directory :', dumpfile_path)


def make_sqldump(db_details, backup_directory):
    try:
        USER = db_details['user']
        PASSWORD = db_details['password']
        HOST = db_details['host']
        DATABASE = db_details['database']
        DUMPNAME = os.path.normpath(os.path.join(
            backup_directory, db_details['database']+'.sql'))
        cmd = f"mysqldump -u {USER} -p{PASSWORD} -h {HOST} {DATABASE} > {DUMPNAME} 2> /dev/null"
        subprocess.call(cmd, None, timeout=None, shell=True)
        print('Finished')
        return DUMPNAME
    except subprocess.TimeoutExpired:
        print('Error: MysqlDump failed with timeout.')
        sys.exit(1)

    except:
        print('Error: Unknown error while dumping mysql.')
        sys.exit(1)


def make_dir(location):
    if not os.path.exists(location):
        os.makedirs(location)


def main(argv):
    wp_dir = ''
    backup_directory = ''
    try:
        opts, _ = getopt.getopt(argv, 'hw:b', ['wordpress_directory=', 'backup_directory='])
    except getopt.GetoptError as err:
        print(str(err)) 
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('WPBackup.py -wordpress_directory <wordpress_directory> --backup_directory <backup_directory>')
            usage()
            sys.exit()
        elif opt in ("-w", "--wordpress_directory"):
            wp_dir = arg
        elif opt in ("-b", "--backup_directory"):
            backup_directory = arg
    if len(wp_dir) < 1:
        print("wordpress directory is missing")
        usage()
        sys.exit()
    if len(backup_directory) < 1:
        print("backup directory is missing")
        usage()
        sys.exit()

    if os.path.exists(wp_dir):
        print('Start Backup Process on :', wp_dir)
        print('')
        backup_directory = ""
        database_info = parsing_wpconfig(wp_dir)
        dump_location = make_sqldump(database_info, backup_directory)
        archive_path = make_archive(wp_dir, dump_location, backup_directory)
        print(f"Finished backup with {archive_path}")

def usage():
    print("\n\nDescription:\n\nA script to backup wordpress website onto local folder.")
    print("This backup will include file and database information related to Wordpress folder.\n")
    print('\nUSAGE: ./WPBackup.py -wordpress_directory <wordpress_directory> -backup_directory <backup_directory>')

if __name__ == '__main__':
    main(sys.argv[1:])
