# MDES
> MDES is a Modular Discrete Event Simulator written in Python.

![MIT Licence](https://img.shields.io/badge/Licence-MIT_Licence-red.svg?style=plastic)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-yellow.svg?style=plastic)](https://www.python.org/)
![v0.1.0](https://img.shields.io/badge/Release-v0.1.0-orange.svg?style=plastic)
![Maintained](https://img.shields.io/badge/Maintained-Yes-green.svg?style=plastic)
[![Twitter](https://img.shields.io/badge/Twitter-@Panagiks-blue.svg?style=plastic)](https://twitter.com/panagiks)

## Features

* Simulates an M/M/c/FIFO queuing system.
* Object-Oriented and fully modular
* Each component is easily swappable/replaceable
* Logging system
* Simulation progress tracking

## Instalation

```sh
pip install mdes
```

## Execution

```sh
mdes -c config.json
```

## Configuration

The Simulator is configurable via `config.json`. The following options are available:

* processesNum    : The number of processes that the Simulator will execute for.
* processesLambda : Theoretical mean inter-arrival time (1/λ).
* processorsNum   : Number of Processors in the Simulator.
* processorLambda : Theoretical mean proccess time (1/μ) of each processor.
* logging         : Setting regarding logging. Follows `logging` package's stracture.

## Todo

- [ ] Simulate more Queuing models (besides M/M/c/FIFO)
- [ ] Provide the ability to simulate complex/elaborate systems descriptively through config (long-term goal)

## License

MIT
