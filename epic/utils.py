def display_list(title: str, items: list):
    "Display a list of records"

    # Voir https://rich.readthedocs.io/en/stable/protocol.html?highlight=__rich__#console-customization

    table = Table(
        title=title,
        padding=(0, 1),
        header_style="blue bold",
        title_style="purple bold",
        title_justify="center",
        width=50,
    )

    try:
        headers = items[0].keys()

    except IndexError:
        headers = ["Liste vide"]

    for title in headers:
        table.add_column(title, style="cyan", justify="center")

    for item in items:
        # rich render only str
        values = [str(value) for value in item.values()]
        table.add_row(*values)

    console = Console()
    print("")
    console.print(table)
