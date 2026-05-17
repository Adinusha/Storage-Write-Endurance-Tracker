
## Storage Write-Endurance Tracker: Monitor TBW (Total Bytes Written) for SD cards in IoT devices.
This is the Project for the Operating Systems 2 course at UNSTPB. It is a web application developed to monitor the Total Bytes Written (TBW) for SD cards used in IoT devices, providing real-time health tracking, lifespan prediction, and automated alerting when a card approaches its endurance limit.

## Write-Endurance
Depending on how much you erase or add data, the SD cards and SSD's loose from their write endurance.

## Total Bytes Written - Formula 
To calculate the theoretical lifespan we will use the following formula:

Lifespan = (Capacity x P/E Cycles)/(Write Amplification Factor)

# Capacity
It is the raw, advertised storage size of the flash memory device (e.g., 32 GB, 64 GB, 256 GB).

# P/E Cycles - Program/Erase Cycles
Flash memory cannot simply overwrite existing data like an old magnetic hard drive can. To write new data, the old data must first be completely wiped and then the new data can be written. One complete round of this is a P/E Cycle.

# Write Amplification Factor (WAF)

Write Amplification is an undesirable but unavoidable phenomenon where the amount of physical data written to the flash memory is a multiple of the logical data that your operating system thinks it is writing.

# Example 
Card: Samsung EVO Plus 64 GB (MLC)
P/E Cycles: 3,000
WAF: 1.5

Lifespan = (64 GB × 3,000) / 1.5 = 128,000 GB = 128 TB

This means the card can sustain approximately 128 TB of total writes before the flash cells begin to fail.

## How it works

This software will be able to monitor in real time the health of the card and it will show :
 * How many much of it's storage has been written
 * How much of it's health is gone
 * A prediction on when should the card be changed

## System Architecture

* IoT Devices — send write events to the REST API endpoint via HTTP POST
* REST API — receives, validates, and stores write events; triggers alert checks
* Django Backend — handles business logic, health calculations, and alert generation
* SQLite Database — stores all devices, SD cards, write events, and alerts
* Web Dashboard — presents health status, charts, and alerts to administrators


## How To Run?

# First you need to install the required dependecies

```bash
pip install -r requirements.txt
```

# Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
# Create an admin user
```bash
python manage.py createsuperuser
```
# Start the development server
```bash
python manage.py runserver
```
Once you start it you need to connect to the following address

Dashboard URL: [http://127.0.0.1:8000/](ttp://127.0.0.1:8000/)

Admin Panel URL: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

