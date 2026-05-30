"""
Google PageRank implementation — modular source package.

Modules:
    data_loader  : Download and parse Stanford SNAP edge-list datasets.
    graph        : WebGraph class (synthetic and real edge-list construction).
    matrix       : Build link matrix P and Google matrix G.
    algorithms   : Core PageRank algorithms (Power Iteration: dense / sparse).
    variants     : Personalized, Topic-Sensitive, Weighted PageRank.
    analysis     : Spearman rank correlation, ranking-table printer.
    visualization: Save 4 separate result figures per dataset.
"""
