import argparse
import shutil

import zeal


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    install_command = subparsers.add_parser(
        "install", help="Install one or more docsets. See `zeal-cli install --help`"
    )
    install_command.add_argument(
        "docsets", nargs="*", help="A list of docset names, separated by a space."
    )

    subparsers.add_parser("list", help="Prints a list of installed docsets")

    remove_command = subparsers.add_parser(
        "remove", help="Delete one or more docsets. See `zeal-cli remove --help`"
    )
    remove_command.add_argument(
        "docsets", nargs="*", help="A list of docset names, separated by a space."
    )

    config_command = subparsers.add_parser(
        "config", help="View or edit zeal-cli's configuration. See `zeal-cli config --help`"
    )
    config_command_subparsers = config_command.add_subparsers(dest="config_action")
    config_find_command = config_command_subparsers.add_parser(  # NOQA: F841
        "locate", help="Print the path to the config file."
    )
    config_view_command = config_command_subparsers.add_parser(
        "view", help="Print the current config."
    )
    config_view_command.add_argument(
        "name",
        help="The name of the config value you're looking for. If not specified, prints all config values.",
        nargs="?",
    )
    config_reset_command = config_command_subparsers.add_parser(  # NOQA: F841
        "reset", help="Reset the config to default."
    )

    args = parser.parse_args()

    if args.action == "install":
        if args.docsets:
            print("Getting list of available docsets")
            feeds = zeal.downloads.get_feeds()
            for docset in args.docsets:
                print(f"Installing docset: {docset}")
                zeal.docset.download(docset, feeds)
                print(f"Successfully installed docset: {docset}")
            print("Cleaning up")
            shutil.rmtree(feeds)
            print("Done")
        else:
            install_command.print_help()

    elif args.action == "list":
        print(*zeal.docset.list_all(), sep="\n")

    elif args.action == "remove":
        if args.docsets:
            for docset in args.docsets:
                print(f"Removing docset: {docset}")
                zeal.docset.remove(docset)
                print(f"Successfully removed docset: {docset}")
        else:
            remove_command.print_help()

    elif args.action == "config":
        if args.config_action == "locate":
            print(zeal.config.cli_config_path)
        elif args.config_action == "view":
            if args.name:
                print(zeal.config.cli_config[args.name])
            else:
                print(zeal.config.cli_config)
        elif args.config_action == "reset":
            zeal.config.set_default_config(zeal.config.cli_config_path)
        else:
            config_command.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
