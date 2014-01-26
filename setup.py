#!/usr/bin/env python

import sys
import os
import os.path


DAEMON_CONFIG_FILE = "Library/LaunchAgents/org.virtualbox.custom.vboxd.plist"

APP_SUPPORT_DIR = "Library/Application Support/org.virtualbox.custom.vboxd"
EXECUTABLE_FILE = APP_SUPPORT_DIR + "/bin/vboxd"
START_CONFIG_FILE = APP_SUPPORT_DIR + "/etc/vboxd-start.conf"
LOG_DIR = APP_SUPPORT_DIR + "/var/log"


def mkdirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def cp(source_file, target_file, filters=None):
    mkdirs(os.path.dirname(target_file))
    with open(source_file, "r") as sf:
        content = sf.read()
    if filters:
        content = content % filters
    with open(target_file, "w") as tf:
        tf.write(content)


def install():
    source_root = os.getcwd()
    target_root = os.path.expanduser("~")

    executable_file = os.path.join(target_root, EXECUTABLE_FILE)
    cp(os.path.join(source_root, EXECUTABLE_FILE), executable_file)

    start_config_file = os.path.join(target_root, START_CONFIG_FILE)
    if not os.path.exists(start_config_file):
        cp(os.path.join(source_root, START_CONFIG_FILE), start_config_file)

    daemon_config_file = os.path.join(target_root, DAEMON_CONFIG_FILE)
    cp(os.path.join(source_root, DAEMON_CONFIG_FILE), daemon_config_file, {
        "HOME": os.path.expanduser("~")
    })

    mkdirs(os.path.join(target_root, LOG_DIR))

    os.system("chmod 755 \"%s\"" % executable_file.replace("\"", "\\\""))
    os.system("chmod 644 \"%s\"" % daemon_config_file.replace("\"", "\\\""))

    os.system("launchctl unload \"%s\" > /dev/null 2>&1" % daemon_config_file.replace("\"", "\\\""))
    os.system("launchctl load \"%s\"" % daemon_config_file.replace("\"", "\\\""))


def uninstall(delete_all):
    target_root = os.path.expanduser("~")

    daemon_config_file = os.path.join(target_root, DAEMON_CONFIG_FILE)
    if os.path.exists(daemon_config_file):
        os.system("launchctl unload \"%s\" > /dev/null 2>&1" % daemon_config_file.replace("\"", "\\\""))
    os.remove(daemon_config_file)

    if delete_all:
        os.system("rm -rf \"%s\"" % os.path.join(target_root, APP_SUPPORT_DIR))
    else:
        os.remove(os.path.join(target_root, EXECUTABLE_FILE))


def main():
    args = sys.argv[1:]
    if len(args) > 0 and args[0].lower() == "install":
        install()
        sys.exit(0)
    elif len(args) > 0 and args[0].lower() == "uninstall":
        uninstall(len(args) > 1 and (args[1].lower() == "-a" or args[1].lower() == "--all"))
        sys.exit(0)
    else:
        print "Usage:"
        print "   python %s install       - Install vboxd" % sys.argv[0]
        print "   python %s uninstall     - Uninstall vboxd (keep config and log files)" % sys.argv[0]
        print "   python %s uninstall -a  - Uninstall vboxd (delete all related files)" % sys.argv[0]
        sys.exit(1)


if __name__ == "__main__":
    main()

