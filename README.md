# OpenClassrooms Project 12

Project created as part of my OpenClassrooms Python Application Developer training.

This is a web application built with  CLI commands for a fictional company, Epic Events.

The Epic Events CRM application aims to help B2B companies efficiently track and manage customer events.

# Features

* Create customer events.
* Assign events to teams or support agents.
* Track the status of events.
* Add comments and updates in real time.
* Manage users and permissions.

# Installation

1. **Install Python:** [Download Python](https://www.python.org/downloads/)

2. **Clone the Repository:**
    - Install Python: [Download Python](https://www.python.org/downloads/)
    - Open a terminal, navigate to the directory of your choice, and clone this repository:
        ```
        git clone https://github.com/th3x4v/Projet_P12.git
        ```

3. **Set Up Virtual Environment:**
    - Navigate to the cloned "Projet_P12" directory and create a new virtual environment:
        ```
        python3 -m venv venv
        ```
    - Activate the virtual environment:
        - Windows:
            ```
            venv\Scripts\activate.bat
            ```
        - Linux/Mac:
            ```
            source venv/bin/activate
            ```

4. **Install Required Packages:**
    ```
    pip install -r requirements.txt
    ```

# CLI Commands in Epic Application

The following CLI commands are available in the Epic application:

## Initialization of the project CLI
- [python -m epic init initialize]: Creates the database and a super-admin user (name:"admin", email:"admin@epic.com",password:"password")

## User login CLI
- [python -m epic auth login]: Login user with password
- [python -m epic auth logout]: Logout user

## User CLI
- [python -m epic user create]: Creates a new user.
- [python -m epic user list]: Lists all users.
- [python -m epic user delete]: Deletes a user.
- [python -m epic user update]: Updates a user's information.
- [python -m epic user password]: Updates a user's password.

## Role CLI
- [python -m epic role create]: Creates a new role.
- [python -m epic role list]: Lists all roles.
- [python -m epic role delete]: Deletes a role.

## Event CLI
- [python -m epic event create]: Creates a new event.
- [python -m epic event list]: Lists all events.
- [python -m epic event delete]: Deletes an event.
- [python -m epic event update]: Updates an event.
- [python -m epic event read]: Lists events associated with the user.

## Client CLI
- [python -m epic client create]: Creates a new client.
- [python -m epic client list]: Lists all clients.
- [python -m epic client delete]: Deletes a client.
- [python -m epic client update]: Updates a client.
- [python -m epic client read]: Lists clients associated with the user.

## Contract CLI
- [python -m epic contract create]: Creates a new contract.
- [python -m epic contract list]: Lists all contracts.
- [python -m epic contract delete]: Deletes a contract.
- [python -m epic contract update]: Updates a contract.
- [python -m epic contract read]: Lists contracts associated with the user.
