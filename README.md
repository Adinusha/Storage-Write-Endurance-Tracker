# Storage Write-Endurance Tracker: Monitor TBW (Total Bytes Written) for SD cards in IoT devices.
This is the Project for the Operating Systems 2 course at UNSTPB.

## Write-Endurance
Depending on how much you erase or add data, the SD cards and SSD's loose from their write endurance.

## Total Bytes Written - Formula 
To calculate the theoretical lifespan we will use the following formula:

Lifespan = (Capacity x P/E Cycles)/(Write Amplification Factor)

## How it works

This software will be able to monitor in real time the health of the card and it will show :
 * How many much of it's storage has been written
 * How much of it's health is gone
 * A prediction on when should the card be changed



