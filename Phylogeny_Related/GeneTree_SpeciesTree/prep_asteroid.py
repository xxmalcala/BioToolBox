import glob, os, sys

from ete3 import Tree
from pathlib import Path

def prep_dir(proj_name: str) -> str:
    rename_dir = f'{proj_name}/Renamed_Trees/'
    Path(rename_dir).mkdir(parents = True, exist_ok = True)
    return rename_dir


def rename_tips(tree):
    for leaf in tree.get_leaves():
        if '_XX_' in leaf.name:
            leaf.name = leaf.name.split("_XX_")[0]
    return tree

def rename_trees(tree_dir: str, rename_dir: str) -> None:
    tree_files = glob.glob(f'{tree_dir}*tre*')
    if not tree_files:
        tree_files = glob.glob(f'{tree_dir}*nwk*')
    for tree in tree_files:
        fixed_tree = rename_tips(Tree(tree))
        fixed_tree.write(format = 1, outfile = f'{rename_dir}{tree.split("/")[-1].split(".tre")[0]}.nwk')


def concat_tree_files(tree_dir: str, proj_name: str) -> str:
    tree_files = glob.glob(f'{tree_dir}*.nwk')
    merged_tree_file = f'{proj_name}.MergedTrees.nwk'
    trees = []
    for t in tree_files:
        trees.append(open(t).readlines()[0].rstrip())
    with open(merged_tree_file, 'w+') as w:
        w.write('\n'.join(trees))
    # os.system(f'cat {tree_dir}*nwk > {merged_tree_file}')
    return merged_tree_file

def asteroid_suggestion(mtf: str) -> None:
     print(f'Suggested ASTEROID call:\n    asteroid -i {mtf} -p {mtf.replace("nwk","ASTEROID")}')

if __name__ == "__main__":
    try:
        tree_dir = sys.argv[1]
        proj_name = sys.argv[2]
    except:
        print('Usage:\n    python something.py [TREE-FILE-DIRECTORY] [PROJECT-NAME]\n')
        sys.exit()

    rnm_dir = prep_dir(proj_name)

    rename_trees(tree_dir, rnm_dir)

    mtf = concat_tree_files(rnm_dir, proj_name)

    asteroid_suggestion(mtf)
