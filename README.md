# QR Transfer
Python script for file transfer over QR for [Bug Koops][1] android application.

## Dependencies
You need to have both Python2.x and Python3.x installed with following packages installed:

 - qrcode, numpy, PIL and six (pip3)
 - wx and zlib (pip)

## Strategies

 - Naive: circular iterating over packets with one pointer and with fixed time slice for every packet
 - Tortoise and Rabbit: circular iterating over packets with 2 pointers in parallel (one twice as fast as the other)


Performance metrics on Note 3:

|   Strategies   | 3 packets     |  9 packets     |  24 packets      |  72 packets |
| -------------- | -------------:| --------------:| ----------------:| -----------:|
| Naive best     |   598 ms      |   2360 ms      |   11.2 s         |   Undefined |
| Naive average  |   985 ms      |   4285 ms      |   24.9 s         |   Undefined |
| Naive worst    |  3751 ms      |   6750 ms      |   50.2 s         |   Undefined |
| TaR best       |   540 ms      |   3430 ms      |   21.1 s         |   2 minutes |
| TaR average    |  1130 ms      |   4760 ms      |   26.2 s         |   9 minutes |
| TaR worst      |  2430 ms      |   7130 ms      |   40.2 s         |   Undefined |

> Undefined means over 10 minutes

## License

[Apache License 2.0][2]

[1]: https://github.com/links234/BugKoops
[2]: http://www.apache.org/licenses/LICENSE-2.0
