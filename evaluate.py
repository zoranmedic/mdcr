import argparse
import json
from collections import defaultdict

import pytrec_eval
import numpy as np

FIELDS = [
    'Art',
    'Biology',
    'Business',
    'Chemistry',
    'Computer Science',
    'Economics',
    'Engineering',
    'Environmental Science',
    'Geography',
    'Geology',
    'History',
    'Materials Science',
    'Mathematics',
    'Medicine',
    'Philosophy',
    'Physics',
    'Political Science',
    'Psychology',
    'Sociology'
]

NEG_TYPES = [
    'bm25',
    'graph',
    'most_cited',
    'random',
    'scincl',
    'specter',
    'true'
]

def calculate_metrics_over_fields(benchmark, scores):
    field_metrics = {}
    
    for f in FIELDS:
        # qrel dict: labels for relevance of each candidate
        qrel = {}
        for qid in benchmark[f]:
            qrel[qid] = {}
            for cand_type in NEG_TYPES:
                for cand in benchmark[f][qid][cand_type]:
                    qrel[qid][cand] = 1 if cand_type == 'true' else 0

        # run dict: scores for relevance obtained by the model
        run = {}
        for qid in qrel:
            run[qid] = {}
            for cid in qrel[qid]:
                run[qid][cid] = scores[f'{qid}_{cid}']
        
        # evaluate run                
        evaluator = pytrec_eval.RelevanceEvaluator(qrel, {'map', 'ndcg', 'recall'})
        results = evaluator.evaluate(run)

        metric_values = {}
        metrics = ['map', 'ndcg', 'recall_5']
        for measure in metrics:
            res = pytrec_eval.compute_aggregated_measure(
                    measure, 
                    [query_measures[measure] for query_measures in results.values()]
                )
            metric_values[measure] = np.round(100 * res, 4)
        field_metrics[f] = metric_values
    
    # average over all fields
    avg_metric_values = defaultdict(list)
    for measure in metrics:
        for f in field_metrics:
            avg_metric_values[measure].append(field_metrics[f][measure])
    for measure in avg_metric_values:
        avg_metric_values[measure] = np.round(np.mean(avg_metric_values[measure]), 4)
    
    return field_metrics, avg_metric_values


def evaluate(args):
    benchmark = json.load(open(args.benchmark_file))
    scores = json.load(open(args.scores_file))

    field_metrics, avg_metrics = calculate_metrics_over_fields(benchmark, scores)

    print(f'Results on the benchmark file {args.benchmark_file} using the scores from the file {args.scores_file}')
    for f in field_metrics:
        print('\t'.join([f] + [f'{m}: {field_metrics[f][m]}' for m in field_metrics[f]]))
    print()
    print('\t'.join(['AVG'] + [f'{m}: {avg_metrics[m]}' for m in avg_metrics]))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--benchmark_file', 
        help='Path to a json file containing query-candidate labels (mdcr_val.json or mdcr_test.json)'
    )
    parser.add_argument(
        '--scores_file',
        help='Path to a json file containing recommendation scores for each query-candidate pair.'
    )
    args = parser.parse_args()

    evaluate(args)
