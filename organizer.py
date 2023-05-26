from numpy import arange
from os import listdir, makedirs, path
from shutil import move


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")
    # TDP
    # prefixes = [str(round(p, 2)).replace('.', 'p') for p in arange(0.63, 0.73, 0.01)]
    # prefixes = [str(p).replace('.', 'p') for p in [0.5, 0.505, 0.51, 0.515, 0.52, 0.525, 0.53, 0.535, 0.54, 0.545, 0.55, 0.555, 0.56]]
    # prefixes = ['0p7', '0p72']
    prefixes = ['0p56', '500', '700', '850']

    # prefixes = ['0p65', '0p7', '0p72', '0p74']
    # prefixes = ['0p62', '0p63', '0p64', '0p66', '0p67', '0p68', '0p69', '0p71']

    # prefixes = ['0p6', '0p62', '0p65', '0p67']
    # prefixes = ['0p57', '0p58', '0p59', '0p61', '0p63', '0p64', '0p66']

    # prefixes = ['0p5', '0p53', '0p55', '0p57']
    # prefixes = ['0p405', '0p41', '0p42', '0p44']
    # prefixes = ['0p282', '0p283', '0p285', '0p29']

    # Scanlon
    # prefixes = ['300', '500', '700', '900']
    
    # Null stochastic
    # prefixes = ['0p27', '0p48', '0p54', '0p61']
    # prefixes = ['0p35', '0p45', '0p55', '0p61']
    # prefixes = ['0p06', '0p43', '0p53', '0p6']
    # prefixes = ['0p23', '0p38', '0p52', '0p64']
    # prefixes = ['0p09', '0p17', '0p4', '0p7']
    # prefixes = [str(round(p, 2)).replace('.', 'p') for p in arange(0.4, 0.58, 0.01)]

    # prefixes = ['0p64', '0p66']
    # prefixes = ['0p51', '0p52', '0p54', '0p56']
    # prefixes = ['0p73']

    # prefixes = ['0p76', '0p78', '0p8']

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