# NMweb

A webinterface for NetworkManager

The goal of this project is to provide webinterface to [NetworkManager](https://networkmanager.dev/) to conveniently configure networking on headless devices.

It consists of two parts.

1. the backend `nmweb.py`, a [Flask](https://flask.palletsprojects.com/en/stable/) based JSON api that connects to NM via DBUS.
2. the frontend, a simple [Svelte](https://svelte.dev/) based SPA

There is a makefile containing the necessary commands to build and run the code.
