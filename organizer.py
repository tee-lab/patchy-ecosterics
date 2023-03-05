from os import listdir, makedirs, path
from shutil import move


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")
    prefixes = ['0p7', '0p71', '0p72', '0p73', '0p74']

    for prefix in prefixes:
        makedirs(path.join(output_path, prefix), exist_ok=True)

    for output_file in listdir(output_path):
        if path.isdir(path.join(output_path, output_file)):
            continue

        for prefix in prefixes:
            if output_file.startswith(prefix + "_"):
                source = path.join(output_path, output_file)
                dest = path.join(output_path, prefix, output_file)
                move(source, dest)
                break