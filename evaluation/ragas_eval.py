# from ragas import evaluate
# from datasets import Dataset
# from ragas.metrics import (
#     faithfulness,
#     answer_relevancy,
#     context_precision,
#     context_recall
# )


# def evaluate_single(query, answer, context):

#     data = {
#             "question": [query],
#             "answer": [answer],
#             "contexts": [[context]],
#             "reference": ["correct expected answer"]
#     }

#     dataset = Dataset.from_dict(data)

#     result = evaluate(
#         dataset,
#         metrics=[
#             faithfulness,
#             answer_relevancy,
#             context_precision,
#             context_recall
#         ]
#     )

#     return result