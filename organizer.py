from os import listdir, makedirs, path
from shutil import move


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")
    # TDP
    # prefixes = ['0p65', '0p7', '0p72', '0p74']
    # prefixes = ['0p6', '0p62', '0p65', '0p67']
    # prefixes = ['0p5', '0p53', '0p55', '0p57']
    prefixes = ['0p405', '0p41', '0p42']
    # prefixes = ['0p28', '0p285', '0p29', '0p31']

    # Scanlong
    # prefixes = ['300', '500', '700', '900']
    
    # Null stochastic
    # prefixes = ['0p48', '0p51', '0p54', '0p57', '0p6']

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