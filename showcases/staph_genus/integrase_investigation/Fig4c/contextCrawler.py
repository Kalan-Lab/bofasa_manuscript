import os
import sys
from collections import defaultdict
from operator import itemgetter
import statistics
from typing import Any, Dict, List, Set, Tuple
import argparse
from rich_argparse import RawTextRichHelpFormatter
from ete3 import Tree

def create_parser():
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        description="""
Program: contextCrawler
Author: Rauf Salamzade
Affiliation: University of Wisconsin - Madison
""",
        formatter_class=RawTextRichHelpFormatter,
    )

    parser.add_argument(
        '-g',
        '--gene-tree',
        help='Gene tree file in Newick format where labels of leafs correspond to locus_tag of genes as they appear in the bofasa results.',
        required=True,
    )
    parser.add_argument(
        '-m',
        '--og-matrix',
        help='Sample - protein ortholog matrix produced as a final result by bofasa run.',
        required=True,
    )
    parser.add_argument(
        '-c',
        '--con-tsv',
        help='Conservation score file from bofasa run results.',
        required=True,
    )
    parser.add_argument(
        '-p',
        '--prep-dir', 
        help='Path to the bofasa prep results directory.',
        required=True,
    )
    parser.add_argument(
        '-o',
        '--output-file',
        help='Output file of decorated phylogeny in Newick format.',
        required=True,
    )

    args = parser.parse_args()
    return args


def compute_custom_gene_set_context_conservation(
    focal_genes: Set[str],
    bofasa_prep_dir: str,
    og_tsv_file: str,
    surrounding_bp: int = 10000,
) -> Dict[str, Any]:
    """
    Compute context conservation for a custom set of genes.

    Treats the provided gene set as a single focal group regardless of which OGs
    they belong to or whether they are a subset of a larger OG. Neighbor OG labels
    are resolved via og_tsv_file.

    Score formula (identical to the per-OG computation):
        context_conservation_score = avg_nog / total_nog
    where total_nog = distinct neighbor OGs seen across all instances,
    and avg_nog = mean number of distinct neighbor OGs per instance.

    Parameters
    ----------
    focal_genes : Set[str]
        Protein IDs to compute context conservation for.
    bofasa_prep_dir : str
        Directory from "bofasa prep".
    og_tsv_file : str
        Path to Protein_Ortholog_Groups.tsv.
    surrounding_bp : int
        Context window in base pairs.

    Returns
    -------
    Dict with keys:
        context_conservation_score          -- avg_nog / total_nog (or 'NA')
        context_conservation_score_complete -- same, complete contexts only (or 'NA')
        total_distinct_neighbor_ogs
        total_distinct_neighbor_ogs_complete
        avg_distinct_neighbor_ogs
        avg_distinct_neighbor_ogs_complete
        num_instances                       -- focal genes found and processed
        num_complete_instances
        instances                           -- list of processed protein IDs
        contexts                            -- list of context strings (C:/I: prefix)
        genes_not_found                     -- focal genes absent from og_tsv_file
    """
    # Build gene->OG and gene->sample from the ortholog TSV
    gene_to_og: Dict[str, str] = {}
    gene_to_sample: Dict[str, str] = {}
    with open(og_tsv_file) as f:
        samples_list: List[str] = []
        for i, line in enumerate(f):
            line = line.strip('\n')
            ls = line.split('\t')
            if i == 0:
                samples_list = ls[1:]
            else:
                og = ls[0]
                for j, gs in enumerate(ls[1:]):
                    sample = samples_list[j]
                    for g in gs.split(','):
                        g = g.strip()
                        if g:
                            gene_to_og[g] = og
                            gene_to_sample[g] = sample

    # Map each sample to its coordinate BED file
    listing_file = os.path.join(bofasa_prep_dir, 'Info_on_Input_Genome_Files.txt')
    sample_to_coords_file: Dict[str, str] = {}
    with open(listing_file) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            line = line.strip()
            sample, _, _, coords_file, _ = line.split('\t')
            sample_to_coords_file[sample] = os.path.join(bofasa_prep_dir, coords_file)

    # Group focal genes by sample; track any that cannot be located
    genes_not_found: Set[str] = set()
    sample_focal_genes: Dict[str, List[str]] = defaultdict(list)
    for gene in focal_genes:
        sample = gene_to_sample.get(gene)
        if sample is None:
            genes_not_found.add(gene)
        else:
            sample_focal_genes[sample].append(gene)

    # Accumulators (mirrors determine_ortholog_group_contexts logic)
    surrounding_nogs: Dict[str, int] = defaultdict(int)
    completed_surrounding_nogs: Dict[str, int] = defaultdict(int)
    context_nogs: List[int] = []
    context_nogs_complete: List[int] = []
    instances: List[str] = []
    contexts: List[str] = []

    for sample, s_focal_genes in sample_focal_genes.items():
        coords_file = sample_to_coords_file.get(sample)
        if not coords_file or not os.path.isfile(coords_file):
            genes_not_found.update(s_focal_genes)
            continue

        # BED format: scaffold  start  end  name  score  strand
        # score: '1' = OK, '0' = within 1 kb of scaffold edge
        scaffold_features: Dict[str, List] = defaultdict(list)
        with open(coords_file) as f:
            for line in f:
                line = line.strip()
                scaffold, start, end, name, score, strand = line.split('\t')
                scaffold_features[scaffold].append([int(start), int(end), name, score, strand])

        s_focal_genes_set = set(s_focal_genes)
        for scaffold in scaffold_features:
            scaffold_features_sorted = sorted(scaffold_features[scaffold], key=itemgetter(0))
            max_features = len(scaffold_features_sorted)

            for cds_index, cds in enumerate(scaffold_features_sorted):
                # cds: [start, end, name, score, strand]
                cds_name = cds[2]
                if cds_name not in s_focal_genes_set:
                    continue

                left_boundary = cds[0] - surrounding_bp
                right_boundary = cds[1] + surrounding_bp
                left_side_genes_and_ogs: Set[Tuple] = set()
                right_side_genes_and_ogs: Set[Tuple] = set()
                near_scaffold_edge = cds[3] == '0'  # cds[3] = score/edge flag

                # Walk left
                cds_iter_index = cds_index - 1
                limit_reached = False
                while not limit_reached:
                    try:
                        if cds_iter_index < 0:
                            near_scaffold_edge = True
                            limit_reached = True
                        else:
                            cds_iter = scaffold_features_sorted[cds_iter_index]
                            if cds_iter[1] < left_boundary:
                                if cds_iter[3] == '0':
                                    near_scaffold_edge = True
                                limit_reached = True
                            elif cds_iter[0] < left_boundary:
                                if cds_iter[3] == '0':
                                    near_scaffold_edge = True
                                left_side_genes_and_ogs.add(
                                    (cds_iter[2], gene_to_og[cds_iter[2]], cds_iter[0])
                                )
                                limit_reached = True
                            else:
                                left_side_genes_and_ogs.add(
                                    (cds_iter[2], gene_to_og[cds_iter[2]], cds_iter[0])
                                )
                    except Exception:
                        # KeyError for neighbor not in any OG → treat as scaffold edge
                        near_scaffold_edge = True
                        limit_reached = True
                    cds_iter_index -= 1

                # Walk right
                cds_iter_index = cds_index + 1
                limit_reached = False
                while not limit_reached:
                    try:
                        if cds_iter_index > max_features - 1:
                            near_scaffold_edge = True
                            limit_reached = True
                        else:
                            cds_iter = scaffold_features_sorted[cds_iter_index]
                            if cds_iter[0] > right_boundary:
                                if cds_iter[3] == '0':
                                    near_scaffold_edge = True
                                limit_reached = True
                            elif cds_iter[1] > right_boundary:
                                if cds_iter[3] == '0':
                                    near_scaffold_edge = True
                                right_side_genes_and_ogs.add(
                                    (cds_iter[2], gene_to_og[cds_iter[2]], cds_iter[0])
                                )
                                limit_reached = True
                            else:
                                right_side_genes_and_ogs.add(
                                    (cds_iter[2], gene_to_og[cds_iter[2]], cds_iter[0])
                                )
                    except Exception:
                        near_scaffold_edge = True
                        limit_reached = True
                    cds_iter_index += 1

                # Orient upstream/downstream by strand; cds[4] = '+'/'-'
                upstream_ogs: List[str] = []
                downstream_ogs: List[str] = []
                if cds[4] == '+':
                    for go in sorted(left_side_genes_and_ogs, key=itemgetter(2)):
                        upstream_ogs.append(go[1])
                    for go in sorted(right_side_genes_and_ogs, key=itemgetter(2)):
                        downstream_ogs.append(go[1])
                else:
                    for go in sorted(right_side_genes_and_ogs, key=itemgetter(2)):
                        upstream_ogs.append(go[1])
                    for go in sorted(left_side_genes_and_ogs, key=itemgetter(2)):
                        downstream_ogs.append(go[1])

                cds_og = gene_to_og.get(cds_name, 'NA')
                complete_status = 'I:' if near_scaffold_edge else 'C:'
                context = complete_status
                if upstream_ogs:
                    context += ', '.join(upstream_ogs) + ', '
                context += cds_og
                if downstream_ogs:
                    context += ', ' + ', '.join(downstream_ogs)

                context_ogs_seen: Set[str] = set()
                complete_context_ogs: Set[str] = set()
                for ogc in upstream_ogs + downstream_ogs:
                    if not near_scaffold_edge:
                        complete_context_ogs.add(ogc)
                    if ogc not in context_ogs_seen:
                        surrounding_nogs[ogc] += 1
                        if not near_scaffold_edge:
                            completed_surrounding_nogs[ogc] += 1
                    context_ogs_seen.add(ogc)

                context_nogs.append(len(context_ogs_seen))
                context_nogs_complete.append(len(complete_context_ogs))
                instances.append(cds_name)
                contexts.append(context)

    total_nog = len(surrounding_nogs)
    total_nog_complete = len(completed_surrounding_nogs)
    avg_nog = round(statistics.mean(context_nogs), 2) if context_nogs else 0.0
    avg_nog_complete = round(statistics.mean(context_nogs_complete), 2) if context_nogs_complete else 0.0

    context_var_score: Any = 'NA'
    context_var_score_complete: Any = 'NA'
    if total_nog > 0:
        context_var_score = round(avg_nog / total_nog, 2)
    if total_nog_complete > 0:
        context_var_score_complete = round(avg_nog_complete / total_nog_complete, 2)

    return {
        'context_conservation_score': context_var_score,
        'context_conservation_score_complete': context_var_score_complete,
        'total_distinct_neighbor_ogs': total_nog,
        'total_distinct_neighbor_ogs_complete': total_nog_complete,
        'avg_distinct_neighbor_ogs': avg_nog,
        'avg_distinct_neighbor_ogs_complete': avg_nog_complete,
        'num_instances': len(instances),
        'num_complete_instances': sum(1 for c in contexts if c.startswith('C:')),
        'instances': instances,
        'contexts': contexts,
        'genes_not_found': genes_not_found,
    }


def get_children(intree: Tree) -> List[Tree]:
    try:
        children = set([])
        for n in intree.traverse("postorder"):
            if n.is_leaf():
                if n.name.strip() != "":
                    children.add(n.name)
        return children
    except Exception:
        msg = "Issue getting children leaves from input tree."
        sys.stderr.write(msg + "\n")
        sys.stderr.write(traceback.format_exc() + "\n")
        sys.exit(1)


def main():
    myargs = create_parser()
    
    gene_tree_file = myargs.gene_tree
    bofasa_prep_dir = myargs.prep_dir
    og_matrix_file = myargs.og_matrix
    con_tsv_file = myargs.con_tsv
    output_file = myargs.output_file

    if os.path.isfile(og_matrix_file):
        og_matrix_file = os.path.abspath(og_matrix_file)
    else:
        sys.stderr.write('Issues with validating the file ' + og_matrix_file + ' exists!\n')
        sys.exit(1)

    if os.path.isfile(con_tsv_file):
        con_tsv_file = os.path.abspath(con_tsv_file)
    else:
        sys.stderr.write('Issues with validating the file ' + con_tsv_file + ' exists!\n')
        sys.exit(1)

    if os.path.isfile(gene_tree_file):
        gene_tree_file = os.path.abspath(gene_tree_file)
    else:
        sys.stderr.write('Issues with validating the file ' + gene_tree_file + ' exists!\n')
        sys.exit(1)

    if os.path.isdir(bofasa_prep_dir):
        bofasa_prep_dir = os.path.abspath(bofasa_prep_dir) + '/'
    else:
        sys.stderr.write('Issues with validating the directory ' + bofasa_prep_dir + ' exists!\n')
        sys.exit(1)

    prot_num_ccs = defaultdict(list)
    with open('../Bofasa_Run_Emg_RS1000_Results/Surrounding_Context_Information/OrthoGroup_Contexts.tsv') as of:
        for i, line in enumerate(of):
            if i == 0: continue
            line = line.strip()
            ls = line.split('\t')
            prots = int(ls[4])
            #if prots in prot_ranges_of_interest:
            ccs = float(ls[6])
            prot_num_ccs[prots].append(ccs)

    prot_num_ccs_map = {}
    for p in prot_num_ccs:
        ccss = prot_num_ccs[p]
        if len(ccss) >= 20:
            prot_num_ccs_map[p] = statistics.median(ccss)

    gt = Tree(gene_tree_file)
    
    for n in gt.traverse('postorder'):
        if n.is_leaf(): continue
        cns = list(get_children(n))
        num_children = len(cns)
        results = compute_custom_gene_set_context_conservation(cns, bofasa_prep_dir, og_matrix_file)
        if num_children in prot_num_ccs_map:
            median_expected = float(results['context_conservation_score'])/float(prot_num_ccs_map[num_children])
            n.add_feature('context_conservation_score_standardized', median_expected)
        n.add_feature('context_conservation_score', results['context_conservation_score'])
        n.add_feature('context_conservation_score_complete', results['context_conservation_score_complete'])
        n.add_feature('total_distinct_neighbor_ogs', results['total_distinct_neighbor_ogs'])
        n.add_feature('total_distinct_neighbor_ogs_complete', results['total_distinct_neighbor_ogs_complete'])
        n.add_feature('avg_distinct_neighbor_ogs', results['avg_distinct_neighbor_ogs'])
        n.add_feature('avg_distinct_neighbor_ogs_complete', results['avg_distinct_neighbor_ogs_complete'])
        n.add_feature('num_instances', results['num_instances'])
        n.add_feature('num_complete_instances', results['num_complete_instances'])


    gt.write(format=1, outfile=output_file, features=['context_conservation_score_standardized'])

if __name__ == "__main__":
    main()
