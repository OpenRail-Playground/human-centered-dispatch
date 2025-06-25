# Human-Centered Dispatch

*Short description what the project is about*

## Background

<p align="center">
  <img alt="Hack4Rail Logo" src="img/hack4rail-logo.jpg" width="220"/>
</p>

This project has been initiated during the [Hack4Rail 2025](https://hack4rail.event.sbb.ch/en/), a joint hackathon organised by the railway companies SBB, ÖBB, and DB in partnership with the OpenRail Association.

## Install

Install uv first:
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:
```shell
uv sync
```

## Running

**Small example:**

```shell
uv run src/dispatch_small.py
```

**Bigger two week example:**

```shell
uv run src/dispatch_two_weeks.py
```
(You can abort after about 2 minutes and get a good but not quite optimal solution.)

Here is an example output: [example_run_two_weeks.txt](./example_run_two_weeks.txt)

## License

<!-- If you decide for another license, please change it here, and exchange the LICENSE file -->

The content of this repository is licensed under the [Apache 2.0 license](LICENSE).
