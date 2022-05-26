from QB.cli.main_cli import Cli
import fire

if __name__ == '__main__':
    c = Cli()
    fire.Fire(Cli)
    # c.migrate()
