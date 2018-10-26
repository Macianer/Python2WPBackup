from __future__ import with_statement
from __future__ import absolute_import
import ftplib
import time
import sys
import os
import re
import subprocess
import getopt
import datetime
import tarfile
from io import open


def parsing_wpconfig(wp_location):
    try:
        config_path = os.path.normpath(wp_location+u'/wp-config.php')
        with open(config_path, encoding=u"utf-8") as fh:
            content = fh.read()

        return parsing_wpconfig_content(content)

    except FileNotFoundError:
        print u'Error: \n' + u'wp-config.php file not found: ,', config_path
        sys.exit(1)

    except PermissionError:
        print u'Missing read permission: ', config_path
        sys.exit(1)

    except AttributeError:
        print u'Error while parsing wp-config.php'
        sys.exit(1)


def parsing_wpconfig_content(wp_config_content):
    if not wp_config_content:
        return {}
    regex_db_name = ur"(?<=DB_NAME', ')(.*?)(?='\);)"
    regex_db_user = ur"(?<=DB_USER', ')(.*?)(?='\);)"
    regex_db_pass = ur"(?<=DB_PASSWORD', ')(.*?)(?='\);)"
    regex_db_host = ur"(?<=DB_HOST', ')(.*?)(?='\);)"
    databse = re.search(regex_db_name, wp_config_content).group(1)
    user = re.search(regex_db_user, wp_config_content).group(1)
    password = re.search(regex_db_pass, wp_config_content).group(1)
    host = re.search(regex_db_host, wp_config_content).group(1)

    return {u'database': databse,
            u'user': user,
            u'password': password,
            u'host': host
            }


def make_archive(wordpress_path, dumpfile_path, backup_directory):
    if not wordpress_path or not dumpfile_path or not backup_directory:
        return None
    try:
        time_tag = datetime.datetime.now().strftime(u'%Y-%m-%d-%H-%M-%S')
        dir_name = os.path.basename(wordpress_path.rstrip(u'/'))
        backup_directory_path = os.path.normpath(backup_directory)
        dir_path = os.path.join(backup_directory_path,dir_name)
        make_dir(dir_path)

        archive_name = os.path.join(
            dir_path, time_tag+u'.tar.gz')

        with tarfile.open(archive_name, u"w:gz") as tar:
            tar.add(wordpress_path)
            if dumpfile_path:
                tar.add(dumpfile_path, arcname=u"sql.dump")
        return archive_name

    except FileNotFoundError:
        print u'Error - File Not Found: ,', archive_name

    except PermissionError:
        print u'Error: Missing write permission.'

    except:
        print u'Error: Unknown error occurred while dumping file into directory :', dumpfile_path


def make_sqldump(db_details, backup_directory):
    try:
        USER = db_details[u'user']
        PASSWORD = db_details[u'password']
        HOST = db_details[u'host']
        DATABASE = db_details[u'database']
        DUMPNAME = os.path.normpath(os.path.join(
            backup_directory, db_details[u'database']+u'.sql'))
        cmd = ("mysqldump -u {0} -p{1} -h {2} {3} > {4} 2> /dev/null").format(User,PASSWORD,HOST,DATABASE,DUMPNAME)
        subprocess.call(cmd, None, timeout=None, shell=True)
        print u'Finished'
        return DUMPNAME
    except subprocess.TimeoutExpired:
        print u'Error: MysqlDump failed with timeout.'
        sys.exit(1)

    except:
        print u'Error: Unknown error while dumping mysql.'
        sys.exit(1)


def make_dir(location):
    if not os.path.exists(location):
        os.makedirs(location)


def main(argv):
    wp_dir = u''
    backup_directory = u''
    try:
        opts, _ = getopt.getopt(argv, 'w:b', ['wordpress_directory=', 'backup_directory='])
    except getopt.GetoptError as err:
        print(str(err)) 
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('WPBackup.py -w <wordpress_directory> -b <backup_directory>')
            usage()
            sys.exit()
        elif opt in ("-w", "--wordpress_directory"):
            wp_dir = arg
        elif opt in (u"-b", u"--backup_directory"):
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
        print u'Start Backup Process on :', wp_dir
        print u''
        backup_directory = u""
        database_info = parsing_wpconfig(wp_dir)
        dump_location = make_sqldump(database_info, backup_directory)
        archive_path = make_archive(wp_dir, dump_location, backup_directory)
        print ("Finished backup with {0}").format(archive_path)

def usage():
    print("\n\nDescription:\n\nA script to backup wordpress website onto local folder.")
    print("This backup will include file and database information related to Wordpress folder.\n")
    print('\nUSAGE: ./WPBackup.py -w <wordpress_directory> -b <backup_directory>')

if __name__ == u'__main__':
    main(sys.argv[1:])
