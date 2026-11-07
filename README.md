# NMweb

A webinterface for NetworkManager

The goal of this project is to provide webinterface to [NetworkManager](https://networkmanager.dev/) to conveniently configure networking on headless devices.

It consists of two parts.

1. the backend `nmweb.py`, a [Flask](https://flask.palletsprojects.com/en/stable/) based JSON api that connects to NM via DBUS.
2. the frontend, a simple [Svelte](https://svelte.dev/) based SPA

There is a makefile containing the necessary commands to build and run the code.

## Dependencies

- `flask` install via `pip`
- `pydbus` install via `pip` or with `apt install python3-pydbus`
- `pygobject` might be needed, too
- `nodejs` with `npm` for building the UI

## Running

1. build the UI once with `make build`
2. run the server with `make run`
3. go to http://localhost:5005
