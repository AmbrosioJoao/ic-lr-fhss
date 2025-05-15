# LR-FHSS-sim

Event-driven simulator for LR-FHSS (Long Range - Frequency Hopping Spread Spectrum), developed in Python.
---

## About the Project

This simulator is part of a study developed with the guidance of **Professor Jamil Farhat** and **Professor Glauber Gomes de Oliveira Brante**.

Based on and extended from the work of:

- Jean Michel de Souza Sant’Ana  
- Arliones Hoeller Jr.  
- Hirley Alves  
- Richard Demo Souza
---

## Installation Guide

### Requirements

```sh
pip install -r requirements.txt
```

### Install the package

```sh
pip install .
```

### Install in editable mode (for development)

```sh
pip install -e .
```

---

## How to Use

## Core Files

- `lrfhss_core.py`: core classes and logic used to build simulation scenarios.
- `settings.py`: configuration file for simulation parameters.
- `run.py`: example simulation that sets up a network and outputs performance metrics.

---

## Extensions

- `traffic.py`: defines various traffic generators for `Node` objects.
- `acrda.py`: alternative `Base` class implementing ACRDA receiver/decoder.

--
