# MDCR - Multi-Domain Citation Recommendation benchmark

Benchmark dataset for the evaluation of scientific article representations on the task of citation recommendation across various scientific fields, presented in the paper [Large-scale Evaluation of Transformer-based Article Encoders on the Task of Citation Recommendation](https://arxiv.org/abs/2209.05452)

Repository contains links for downloading the benchmark data splits (both validation and test splits), as well as the script for evaluating recommendation scores obtained by a recommendation model for the data in the splits. If you encounter any problems or errors feel free to raise an issue or send an email to <zoran.medic@fer.hr>.

## Data

JSON files containing validation and test splits of MDCR are available here:
* [val_split](https://takelab.fer.hr/data/mdcr/mdcr_val.json)
* [test_split](https://takelab.fer.hr/data/mdcr/mdcr_test.json)

These files have the following schema:
```
{
  <MAG_field>: {
    <query_paper_id>: {
        "bm25": [<candidate_paper_id>],  # candidates identified using model-based selection (BM25 as the model)
        "scincl": [<candidate_paper_id>],  # candidates identified using model-based selection (SciNCL as the model)
        "specter": [<candidate_paper_id>],  # candidates identified using model-based selection (SPECTER as the model)
        "graph": [<candidate_paper_id>],  # candidates identified using graph-based selection
        "most_cited": [<candidate_paper_id>],  # candidates identified using citation count as the method
        "random": [<candidate_paper_id>]   # candidates identified with random sampling
        },
    <query_paper_id>: {
        ...
        }
    ...
    },
  <MAG_field>: {
    ...
    }
  ...
}
```

In order to evaluate the model, recommendation scores for each combination of `query_paper_id` and `candidate_paper_id` must be calculated and stored in a JSON file (details below).

Files containing all the papers' titles and abstracts are stored in separate `.jsonl` files (around 250MB each), that can be found on the following links:
* [val_data](https://takelab.fer.hr/data/mdcr/mdcr_val_data.jsonl)
* [test_data](https://takelab.fer.hr/data/mdcr/mdcr_test_data.jsonl)

## Requirements

A few additional libraries are needed for running the evaluation script. Run the following commands to make sure the environment is ready for running the evaluation:

```
conda create -n mdcr python=3.8

conda activate mdcr

conda install -c conda-forge numpy jsonlines

pip install pytrec_eval

```

## Evaluating models on the benchmark

In order to evaluate a custom model on the benchmark, you should produce a JSON file containing recommendation scores for each query-candidate pair in the data split (val or test).  
JSON file should contain a single dictionary in which keys are formatted as `queryid_candidateid` strings, i.e., query and candidate article IDs are separated with an underscore. Values for each such key represent recommendation scores, where **a higher score indicates a higher relevance**.

We provide an example of such JSON file for the scores obtained with the `SciNCL` model on the test set split (`scincl_scores.json`). Running the evaluation on this file should output the results reported in our paper for SciNCL. To obtain those results, run the following command (assuming that JSON files are in the `data/` folder):

```eval
python evaluate.py --benchmark_file data/mdcr_test.json --scores_file data/scincl_scores.json
```

The output should look like this:
```
Results on the benchmark file data/mdcr_test.json using the scores from the file data/scincl_scores.json
Art     map: 34.7136    ndcg: 60.3739   recall_5: 29.15
Biology map: 36.8358    ndcg: 62.7903   recall_5: 32.3
Business        map: 28.4669    ndcg: 55.5329   recall_5: 24.6
Chemistry       map: 36.5293    ndcg: 61.951    recall_5: 31.5
Computer Science        map: 37.2056    ndcg: 62.7272   recall_5: 32.2
Economics       map: 28.3171    ndcg: 55.395    recall_5: 23.2
Engineering     map: 34.1759    ndcg: 60.4889   recall_5: 28.0
Environmental Science   map: 31.4845    ndcg: 58.1616   recall_5: 25.5
Geography       map: 29.4518    ndcg: 56.4011   recall_5: 23.8
Geology map: 25.72      ndcg: 52.8014   recall_5: 19.9
History map: 30.9442    ndcg: 57.1201   recall_5: 23.85
Materials Science       map: 35.7855    ndcg: 61.9001   recall_5: 29.6
Mathematics     map: 34.9152    ndcg: 60.9257   recall_5: 30.1
Medicine        map: 42.6579    ndcg: 67.0481   recall_5: 36.5
Philosophy      map: 29.8966    ndcg: 56.9015   recall_5: 23.45
Physics map: 34.499     ndcg: 60.3763   recall_5: 30.3
Political Science       map: 26.3834    ndcg: 53.9156   recall_5: 21.7333
Psychology      map: 34.1724    ndcg: 60.8867   recall_5: 30.5
Sociology       map: 26.6838    ndcg: 54.0052   recall_5: 21.9

AVG     map: 32.5704    ndcg: 58.9317   recall_5: 27.2675
```
