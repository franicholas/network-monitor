import socket
import time
import csv
import datetime
import os
import sys
import argparse


def check_port(host, port, timeout=2):
    
    start = time.perf_counter()
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    
    socket_0 = socket.socket() 
    socket_0.settimeout(timeout)
    
    try:

        socket_0.connect((host, port))
        status = "OPEN"
        

    
    except ConnectionRefusedError: 
        status = "CLOSED"

    except OSError as error:
        status = "ERROR"

    
    finally:
        socket_0.close()
    
    end = time.perf_counter()
    elapsed = end - start

    return (status, elapsed, timestamp)


def main():

    parser = argparse.ArgumentParser(description="a network monitor")
    parser.add_argument("--endpoint", nargs= "+", type=str, required =True) #1.1.1.1:11
    parser.add_argument("--interval", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=2)
    args = parser.parse_args()

    if args.interval < 1:
        print("--interval must be an integer greater than 0")
        sys.exit()

    if args.timeout < 1:
        print("--timeout must be an integer greater than 0")
        sys.exit()


    stats = {}
    targets = []

    for endpoint in args.endpoint:
        if len(endpoint.split(":")) == 2:
            host, port = endpoint.split(":")

            if not host:
                print("INVALID ENDPOINT: host cannot be empty.\n")
                continue
        
            try:           
                port = int(port)
            
            except ValueError:
                print(f"INVALID PORT: {port} is not integer.\n")
                continue
            
            if not 1 <= port <= 65535:
                print(f"INVALID PORT: {port} is not between 1 and 65535.\n")
                continue
            
            targets.append((host,port))
            stats[(host, port)] = {"successful_checks" : 0, "failed_checks": 0, "total_checks": 0}

        else:
            print("INVALID ENDPOINT: expected HOST:PORT")
            
    if not targets:
        print("Error: no valid endpoints provided. Expected HOST:PORT.\n")
        sys.exit()
        
    try:
        while True:
            
            open_count = 0
            failed_count = 0
            
            with open("results.csv", "a", newline="") as file:
                writer = csv.writer(file)

                file_size = os.path.getsize("results.csv")

                if file_size == 0:
                    writer.writerow(["Timestamp", "Host", "Port", "Status", "Elapsed_ms"])


                for host, port in targets: 
                    
                    status, elapsed, timestamp = check_port(host, port, args.timeout)

                    if status == "OPEN":
                        stats[(host,port)]["successful_checks"] += 1
                        open_count += 1

                    else:
                        stats[(host,port)]["failed_checks"] += 1
                        failed_count += 1

                    stats[(host,port)]["total_checks"] += 1

                    writer.writerow([timestamp, host, port, status,  round(elapsed * 1000, 2)])

                    
            
            print(f"\nSUCCESSFUL CHECKS THIS CYCLE: {open_count}")
            print(f"FAILED CHECKS THIS CYCLE: {failed_count}\n")

            for host, port in targets:
                availability =  (100 * stats[(host,port)]["successful_checks"] / 
                                            stats[(host,port)]["total_checks"])
                                
            
                print(f"{host}:{port}\n")
                print(f"Total checks: {stats[(host,port)]["total_checks"]}")
                print(f"Successful checks: {stats[(host,port)]["successful_checks"]}")
                print(f"Availability: {availability:.1f}%")
                print(f"Failed checks: {stats[(host,port)]["failed_checks"]}\n")



            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("Closing program...")

if __name__ == "__main__":
    main()





