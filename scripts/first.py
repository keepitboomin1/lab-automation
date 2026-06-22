import subprocess

# Define both machines
hosts = ["rhcsa1.example.com", "rhcsa2.example.com"]

def get_system_report(host):
    print("--- System Report: " + host + " ---")

    # Run commands remotely via SSH
    # For rhcsa1 we run locally, for rhcsa2 we SSH in
    if host == "rhcsa1.example.com":
        prefix = []
    else:
        prefix = ["ssh", host]

    # Get uptime
    uptime = subprocess.run(
        prefix + ["uptime"],
        capture_output=True, text=True
    )

    # Get hostname
    hostname = subprocess.run(
        prefix + ["hostname"],
        capture_output=True, text=True
    )

    # Get logged in users
    who = subprocess.run(
        prefix + ["who"],
        capture_output=True, text=True
    )

    user_count = len(who.stdout.strip().splitlines())

    # Print report
    print("Hostname   : " + hostname.stdout.strip())
    print("Users      : " + str(user_count))
    print("Uptime     : " + uptime.stdout.strip())

    # Check load average
    load = float(uptime.stdout.strip().split("load average:")[1].split(",")[0].strip())
    if load > 1.0:
        print("WARNING    : High load average detected - " + str(load))
    else:
        print("Load       : OK (" + str(load) + ")")

    print("")

# Run report for each host
for host in hosts:
    get_system_report(host)
