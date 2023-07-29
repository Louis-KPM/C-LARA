import glob
import os

categories = {
    'Core': {
        'Python': '$CLARA/clara_app/clara_core/*.py',
        'HTML templates': '$CLARA/templates/*.html',
        'Prompt templates and examples': '$CLARA/prompt_templates/*/*_*_*.*',
        'CSS': '$CLARA/static/*.css',
        'JavaScript': '$CLARA/static/*.js',
        'Config': '$CLARA/clara_app/clara_core/*.ini',
    },
    'Django': {
        'Python': '$CLARA/clara_app/*.py',
        'HTML templates': '$CLARA/clara_app/templates/clara_app/*.html',
        'CSS': '$CLARA/clara_app/static/clara_app/*.css',
        'JavaScript': '$CLARA/clara_app/static/clara_app/scripts/*.js',
        'Settings': '$CLARA/clara_project/settings.py',
    },
    'Documentation': {
        'README': '$CLARA/README.txt',
        'FUNCTIONALITY': '$CLARA/FUNCTIONALITY.txt',
        'TODO': '$CLARA/TODO.txt',
    }
}

def count_lines(files_pattern):
    files_pattern = os.path.expandvars(files_pattern)
    files = glob.glob(files_pattern)
    return sum(1 for file in files for line in open(file, encoding='utf-8'))

def print_table():
    latex_table = "\\begin{tabular}{lr}\n\\toprule\n\\multicolumn{1}{c}{\\textbf{Type}} & \\multicolumn{1}{c}{\\textbf{Lines}} \\\\\n\\midrule"
    total = 0
    for category, types in categories.items():
        latex_table += "\n\\multicolumn{{2}}{{c}}{{\\textit{{{0}}}}} \\\\\n\\midrule".format(category)
        category_total = 0
        for type, pattern in types.items():
            lines = count_lines(pattern)
            latex_table += "\n{0} & {1} \\\\\n".format(type, lines)
            category_total += lines
        latex_table += "Total, {0} & {1} \\\\\n\\midrule".format(category, category_total)
        total += category_total

    latex_table += "\nTotal & {0} \\\\\n\\bottomrule\n\\end{{tabular}}".format(total)

    print(latex_table)

print_table()
